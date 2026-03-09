/*
  Plant Moisture Monitor - ESP32
  ==============================
  מערכת ניטור לחות קרקע לצמחים

  חיבורים:
  - Capacitive Soil Moisture Sensor:
    - VCC → 3.3V
    - GND → GND
    - AOUT → GPIO 34 (ADC1_CH6)

  המערכת:
  - קוראת נתוני לחות מהחיישן
  - שולחת את הנתונים לשרת דרך WiFi (מקומי או ענן)
  - נכנסת למצב שינה עמוקה (Deep Sleep)
  - מתעוררת כל X דקות למדידה חדשה
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// ===================== הגדרות רשת =====================
const char* WIFI_SSID     = "Barhum 2.4_EXT";
const char* WIFI_PASSWORD = "19741974";

// ===================== הגדרות שרת =====================
// ---- שרת מקומי (לבדיקות): ----
// const char* SERVER_URL = "http://192.168.1.100:5000/api/data";

// ---- שרת בענן (Render): ----
// החלף YOUR-APP-NAME בשם שבחרת ב-Render
const char* SERVER_URL = "https://YOUR-APP-NAME.onrender.com/api/data";

// ---- API Key - חייב להתאים למה שמוגדר בשרת ----
const char* API_KEY = "plant-monitor-secret-123";

// ===================== הגדרות חיישן =====================
const int SENSOR_PIN = 34;          // GPIO 34 - ADC1_CH6
const int AIR_VALUE = 3500;         // ערך בעת אוויר (יבש) - כייל בהתאם לחיישן שלך
const int WATER_VALUE = 1500;       // ערך בעת מים (רטוב) - כייל בהתאם לחיישן שלך

// ===================== הגדרות מערכת =====================
const int DEVICE_ID = 1;                        // מזהה הבקר (שנה לכל בקר)
const char* DEVICE_NAME = "סלון - פיקוס";       // שם הצמח
const int SLEEP_MINUTES = 30;                    // זמן שינה בדקות
const int WIFI_TIMEOUT_SEC = 20;                 // זמן המתנה מקסימלי לחיבור WiFi

// ===================== משתנים גלובליים =====================
RTC_DATA_ATTR int bootCount = 0;  // נשמר גם במצב שינה

void setup() {
  Serial.begin(115200);
  delay(100);

  bootCount++;
  Serial.println("\n====================================");
  Serial.printf("  Plant Monitor - Boot #%d\n", bootCount);
  Serial.println("====================================");

  // קריאת חיישן
  int rawValue = readSensor();
  int moisturePercent = calculateMoisturePercent(rawValue);
  float voltage = (rawValue / 4095.0) * 3.3;

  Serial.printf("Raw: %d | Voltage: %.2fV | Moisture: %d%%\n",
                rawValue, voltage, moisturePercent);

  // חיבור WiFi ושליחת נתונים
  if (connectWiFi()) {
    sendData(rawValue, moisturePercent, voltage);
    WiFi.disconnect(true);
  } else {
    Serial.println("WiFi connection failed - data not sent");
  }

  // כניסה לשינה עמוקה
  goToSleep();
}

void loop() {
  // לא מגיעים לכאן - המערכת במצב Deep Sleep
}

// ===================== קריאת חיישן =====================
int readSensor() {
  // ממוצע של מספר קריאות לדיוק טוב יותר
  const int SAMPLES = 10;
  long total = 0;

  for (int i = 0; i < SAMPLES; i++) {
    total += analogRead(SENSOR_PIN);
    delay(10);
  }

  return total / SAMPLES;
}

// ===================== חישוב אחוזי לחות =====================
int calculateMoisturePercent(int rawValue) {
  // המרה לאחוזים: ערך גבוה = יבש, ערך נמוך = רטוב
  int percent = map(rawValue, AIR_VALUE, WATER_VALUE, 0, 100);
  return constrain(percent, 0, 100);
}

// ===================== חיבור WiFi =====================
bool connectWiFi() {
  Serial.printf("Connecting to WiFi: %s", WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < WIFI_TIMEOUT_SEC * 2) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("\nConnected! IP: %s\n", WiFi.localIP().toString().c_str());
    return true;
  }

  return false;
}

// ===================== שליחת נתונים לשרת =====================
void sendData(int rawValue, int moisturePercent, float voltage) {
  HTTPClient http;
  http.begin(SERVER_URL);
  http.addHeader("Content-Type", "application/json");
  http.addHeader("X-API-Key", API_KEY);

  // בניית JSON
  JsonDocument doc;
  doc["device_id"] = DEVICE_ID;
  doc["device_name"] = DEVICE_NAME;
  doc["moisture_percent"] = moisturePercent;
  doc["moisture_raw"] = rawValue;
  doc["voltage"] = voltage;
  doc["boot_count"] = bootCount;
  doc["sleep_minutes"] = SLEEP_MINUTES;

  String jsonString;
  serializeJson(doc, jsonString);

  Serial.printf("Sending data: %s\n", jsonString.c_str());

  int httpCode = http.POST(jsonString);

  if (httpCode > 0) {
    Serial.printf("Server response: %d\n", httpCode);
    String response = http.getString();
    Serial.println(response);
  } else {
    Serial.printf("HTTP Error: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();
}

// ===================== מצב שינה עמוקה =====================
void goToSleep() {
  uint64_t sleepTime = (uint64_t)SLEEP_MINUTES * 60 * 1000000;

  Serial.printf("\nGoing to deep sleep for %d minutes...\n", SLEEP_MINUTES);
  Serial.println("====================================\n");
  Serial.flush();

  esp_sleep_enable_timer_wakeup(sleepTime);
  esp_deep_sleep_start();
}
