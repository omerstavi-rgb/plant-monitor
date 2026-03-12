/*
  Plant Moisture Monitor - ESP32
  ==============================
  מערכת ניטור לחות קרקע לצמחים

  חיבורים:
  - Capacitive Soil Moisture Sensor:
    - VCC → 3.3V
    - GND → GND
    - AOUT → GPIO 34 (ADC1_CH6)

  - סוללה (מדידת מתח):
    - מחלק מתח: BAT+ → R1(100K) → GPIO 35 → R2(100K) → GND
    - או ישירות אם הסוללה עד 3.3V

  המערכת:
  - מודדת לחות ומתח סוללה ושולחת לשרת
  - בודקת בשרת כל כמה דקות למדוד (ניתן לשנות מהדשבורד)
  - נכנסת ל-Deep Sleep לחיסכון חשמל

  כיול:
  - שים את החיישן באוויר → רשום את הערך → זה AIR_VALUE
  - שים את החיישן במים → רשום את הערך → זה WATER_VALUE
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ===================== הגדרות רשת =====================
const char* WIFI_SSID     = "Barhum 2.4_EXT";
const char* WIFI_PASSWORD = "19741974";

// ===================== הגדרות שרת =====================
const char* SERVER_BASE = "https://plant-monitor-wg7r.onrender.com";
const char* API_KEY = "plant-monitor-secret-123";

// ===================== הגדרות חיישן =====================
const int SENSOR_PIN = 34;          // GPIO 34 - ADC1_CH6
const int AIR_VALUE = 3500;         // ערך באוויר (יבש) - כייל!
const int WATER_VALUE = 1500;       // ערך במים (רטוב) - כייל!

// ===================== הגדרות סוללה =====================
// אפשרות 1: סוללת ליתיום ישירות (בלי Power Bank)
//   → חבר: BAT+ → נגד 100K → GPIO 35 → נגד 100K → GND
//   → הגדר USE_BATTERY_PIN = true
//
// אפשרות 2: Power Bank (USB)
//   → אין צורך בחיבור נוסף
//   → הגדר USE_BATTERY_PIN = false (הסוללה תראה תמיד "מחובר לחשמל")

const bool USE_BATTERY_PIN = false;  // שנה ל-true אם חיברת מחלק מתח!
const int BATTERY_PIN = 35;          // GPIO 35 - רק אם USE_BATTERY_PIN = true
const float BATTERY_FULL = 4.2;      // מתח סוללה מלאה (ליתיום)
const float BATTERY_EMPTY = 3.0;     // מתח סוללה ריקה

// ===================== הגדרות מערכת =====================
const int DEVICE_ID = 1;
const char* DEVICE_NAME = "סלון - פיקוס";
const int DEFAULT_SLEEP_MINUTES = 5;   // ברירת מחדל - 5 דקות לבדיקה. שנה ל-30 אחרי הבדיקה
const int WIFI_TIMEOUT_SEC = 30;       // 30 שניות המתנה ל-WiFi

// ===================== משתנים גלובליים =====================
RTC_DATA_ATTR int bootCount = 0;
RTC_DATA_ATTR int sleepMinutes = DEFAULT_SLEEP_MINUTES;

void setup() {
  Serial.begin(115200);
  delay(1000);  // המתנה לייצוב אחרי הפעלה

  bootCount++;
  Serial.println("\n====================================");
  Serial.printf("  Plant Monitor - Boot #%d\n", bootCount);
  Serial.printf("  Sleep interval: %d minutes\n", sleepMinutes);
  Serial.println("====================================");

  if (connectWiFi()) {
    measureAndSend();
    checkSettings();
    WiFi.disconnect(true);
    WiFi.mode(WIFI_OFF);
  } else {
    Serial.println("WiFi connection failed!");
  }

  goToSleep();
}

void loop() {
  // לא מגיעים לכאן - Deep Sleep
}

// ===================== מדידה ושליחה =====================
void measureAndSend() {
  int rawValue = readSensor();
  int moisturePercent = calculateMoisturePercent(rawValue);
  int batteryPercent = readBattery();

  Serial.printf("Moisture: %d%% (raw: %d / 4095)\n", moisturePercent, rawValue);
  Serial.printf("Battery: %d%%\n", batteryPercent);
  sendData(rawValue, moisturePercent, batteryPercent);
}

// ===================== קריאת חיישן =====================
int readSensor() {
  const int SAMPLES = 10;
  long total = 0;

  for (int i = 0; i < SAMPLES; i++) {
    total += analogRead(SENSOR_PIN);
    delay(10);
  }

  return total / SAMPLES;
}

// ===================== קריאת סוללה =====================
int readBattery() {
  if (!USE_BATTERY_PIN) {
    // Power Bank - אי אפשר למדוד, מחזיר -1 (= "מחובר לחשמל")
    Serial.println("Battery: Power Bank mode (no measurement)");
    return -1;
  }

  // מחלק מתח: BAT+ → 100K → GPIO35 → 100K → GND
  const int SAMPLES = 10;
  long total = 0;

  for (int i = 0; i < SAMPLES; i++) {
    total += analogRead(BATTERY_PIN);
    delay(10);
  }

  int rawBattery = total / SAMPLES;

  // מחלק מתח חוצה ב-2, אז כופלים בחזרה
  float voltage = (rawBattery / 4095.0) * 3.3 * 2.0;

  // המרה לאחוזים
  int percent = (int)(((voltage - BATTERY_EMPTY) / (BATTERY_FULL - BATTERY_EMPTY)) * 100.0);
  percent = constrain(percent, 0, 100);

  Serial.printf("Battery raw: %d, voltage: %.2fV, percent: %d%%\n", rawBattery, voltage, percent);
  return percent;
}

// ===================== חישוב אחוזי לחות =====================
int calculateMoisturePercent(int rawValue) {
  int percent = map(rawValue, AIR_VALUE, WATER_VALUE, 0, 100);
  return constrain(percent, 0, 100);
}

// ===================== חיבור WiFi =====================
bool connectWiFi() {
  Serial.printf("Connecting to WiFi: %s ", WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.disconnect(true);   // ניקוי חיבורים ישנים
  delay(500);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  int maxAttempts = WIFI_TIMEOUT_SEC * 2;  // כל 500ms

  while (WiFi.status() != WL_CONNECTED && attempts < maxAttempts) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("\nConnected! IP: %s\n", WiFi.localIP().toString().c_str());
    return true;
  }

  Serial.printf("\nFailed after %d seconds\n", WIFI_TIMEOUT_SEC);
  return false;
}

// ===================== שליחת נתונים =====================
void sendData(int rawValue, int moisturePercent, int batteryPercent) {
  HTTPClient http;
  String url = String(SERVER_BASE) + "/api/data";
  http.begin(url);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-API-Key", API_KEY);
  http.setTimeout(15000);

  JsonDocument doc;
  doc["device_id"] = DEVICE_ID;
  doc["device_name"] = DEVICE_NAME;
  doc["moisture_percent"] = moisturePercent;
  doc["moisture_raw"] = rawValue;
  doc["battery_percent"] = batteryPercent;
  doc["sleep_minutes"] = sleepMinutes;

  String jsonString;
  serializeJson(doc, jsonString);

  Serial.printf("Sending: %s\n", jsonString.c_str());

  int httpCode = http.POST(jsonString);
  if (httpCode > 0) {
    Serial.printf("Server: %d OK\n", httpCode);
  } else {
    Serial.printf("Error: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();
}

// ===================== בדיקת הגדרות מהשרת =====================
void checkSettings() {
  HTTPClient http;
  String url = String(SERVER_BASE) + "/api/device/" + String(DEVICE_ID) + "/settings";
  http.begin(url);
  http.addHeader("X-API-Key", API_KEY);
  http.setTimeout(10000);

  int httpCode = http.GET();

  if (httpCode == 200) {
    String response = http.getString();
    Serial.printf("Settings: %s\n", response.c_str());

    JsonDocument doc;
    deserializeJson(doc, response);

    int newInterval = doc["interval_minutes"] | DEFAULT_SLEEP_MINUTES;

    if (newInterval != sleepMinutes && newInterval >= 1 && newInterval <= 1440) {
      Serial.printf("Interval changed: %d -> %d minutes\n", sleepMinutes, newInterval);
      sleepMinutes = newInterval;
    }
  } else {
    Serial.printf("Settings error: %d\n", httpCode);
  }

  http.end();
}

// ===================== Deep Sleep =====================
void goToSleep() {
  uint64_t sleepTime = (uint64_t)sleepMinutes * 60ULL * 1000000ULL;

  Serial.printf("\nSleeping for %d minutes...\n", sleepMinutes);
  Serial.println("====================================\n");
  Serial.flush();

  esp_sleep_enable_timer_wakeup(sleepTime);
  esp_deep_sleep_start();
}
