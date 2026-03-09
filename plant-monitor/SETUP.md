# Plant Monitor - מדריך התקנה

## מבנה הפרויקט

```
plant-monitor/
├── esp32/
│   └── plant_monitor.ino    ← קוד ה-ESP32 (Arduino IDE)
├── server/
│   ├── server.py            ← שרת Python
│   └── requirements.txt     ← תלויות Python
├── web/
│   └── index.html           ← דשבורד אינטרנטי
├── render.yaml              ← הגדרות Render (ענן)
├── requirements.txt         ← תלויות Python (ענן)
└── SETUP.md                 ← המדריך הזה
```

---

## חלק א': חיבור החומרה וכיול

### חיבור חיישן לחות ל-ESP32:

| חיישן | ESP32 |
|--------|-------|
| VCC    | 3.3V  |
| GND    | GND   |
| AOUT   | GPIO 34 |

> **חשוב:** השתמש ב-3.3V ולא ב-5V כדי לא לפגוע ב-ADC של ה-ESP32

### כיול החיישן:
1. פתח את `plant_monitor.ino` ב-Arduino IDE
2. שנה זמנית את `SLEEP_MINUTES` ל-`0`
3. העלה ופתח Serial Monitor (115200 baud)
4. רשום ערך באוויר (יבש) → עדכן `AIR_VALUE`
5. רשום ערך במים (רטוב) → עדכן `WATER_VALUE`

---

## חלק ב': הגדרת Arduino IDE

### התקנת ESP32 Board:
1. פתח Arduino IDE
2. לך ל: `File → Preferences`
3. ב-"Additional Board Manager URLs" הוסף:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. לך ל: `Tools → Board → Boards Manager`
5. חפש "esp32" והתקן **esp32 by Espressif Systems**

### התקנת ספריות:
- לך ל: `Tools → Manage Libraries`
- חפש והתקן: **ArduinoJson** (by Benoit Blanchon)

### הגדרות Board:
- Board: **ESP32 Dev Module**
- Upload Speed: **921600**
- Flash Frequency: **80MHz**

---

## חלק ג': העלאה לענן (Render.com) - חינם!

### שלב 1: יצירת חשבון GitHub
אם אין לך חשבון, צור אחד ב-https://github.com

### שלב 2: העלאת הפרויקט ל-GitHub
1. צור Repository חדש ב-GitHub (שם: `plant-monitor`)
2. העלה את **כל** תיקיית `plant-monitor` ל-Repository

דרך Command Line:
```bash
cd plant-monitor
git init
git add .
git commit -m "Initial commit - plant monitor"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/plant-monitor.git
git push -u origin main
```

או פשוט גרור את הקבצים לממשק של GitHub.

### שלב 3: הרשמה ל-Render
1. לך ל: https://render.com
2. לחץ **Sign Up** → **Sign up with GitHub**
3. אשר גישה ל-GitHub

### שלב 4: יצירת שירות חדש
1. לחץ **New** → **Web Service**
2. בחר את ה-Repository: `plant-monitor`
3. הגדר:
   - **Name:** `plant-monitor` (או שם אחר שתבחר)
   - **Region:** Frankfurt (EU) - הכי קרוב לישראל
   - **Branch:** `main`
   - **Runtime:** Python
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn server.server:app --bind 0.0.0.0:$PORT`
   - **Instance Type:** **Free**

### שלב 5: הגדרת Environment Variables
ב-Render, לך ל-**Environment** והוסף:

| Key | Value |
|-----|-------|
| `RENDER` | `true` |
| `API_KEY` | `plant-monitor-secret-123` (או סיסמה שתבחר) |

### שלב 6: Deploy!
לחץ **Create Web Service** וחכה שה-Build יסתיים.
האתר שלך יהיה זמין בכתובת:
```
https://plant-monitor.onrender.com
```
(או השם שבחרת)

---

## חלק ד': חיבור ה-ESP32 לשרת בענן

פתח את `plant_monitor.ino` ועדכן:

```cpp
// כתובת השרת בענן - החלף את YOUR-APP-NAME
const char* SERVER_URL = "https://plant-monitor.onrender.com/api/data";

// API Key - חייב להתאים למה שהגדרת ב-Render
const char* API_KEY = "plant-monitor-secret-123";
```

העלה את הקוד ל-ESP32 ובדוק ב-Serial Monitor שהנתונים נשלחים.

---

## הוספת בקרים נוספים

לכל ESP32 חדש:
1. שנה את `DEVICE_ID` למספר ייחודי (2, 3, 4...)
2. שנה את `DEVICE_NAME` לשם הצמח
3. כייל את ערכי `AIR_VALUE` ו-`WATER_VALUE`
4. ודא שכתובת השרת ו-API_KEY נכונים
5. העלה את הקוד

---

## פתרון בעיות

| בעיה | פתרון |
|------|-------|
| WiFi לא מתחבר | ודא שהרשת 2.4GHz (לא 5GHz) |
| ערכי חיישן 0 או 4095 | בדוק חיבורים, ודא שהחיישן על GPIO 34 |
| השרת מחזיר 401 | ודא שה-API_KEY תואם בין ESP32 לשרת |
| Render מראה שגיאה | בדוק את הלוגים ב-Render Dashboard |
| Serial Monitor ריק | ודא baud rate 115200 |
| האתר מגיב לאט בפעם הראשונה | Render Free "מרדים" את השרת - ההתעוררות לוקחת ~30 שניות |

### הערה חשובה על Render Free:
בתוכנית החינמית, Render "מרדים" את השרת אחרי 15 דקות ללא פעילות.
כשה-ESP32 שולח נתונים, השרת מתעורר (לוקח ~30 שניות).
זה בסדר גמור לפרויקט הזה כי ה-ESP32 יכול לחכות.
