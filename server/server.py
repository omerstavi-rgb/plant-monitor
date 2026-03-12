"""
Plant Monitor Server
====================
שרת לקבלת נתוני לחות מבקרי ESP32 והצגתם בדשבורד
תומך בהרצה מקומית וב-Render (ענן)

הרצה מקומית:
    pip install -r requirements.txt
    python server.py

הרצה בענן (Render):
    מוגדר אוטומטית דרך render.yaml
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime
import sqlite3
import os
import json
import requests as http_requests
from server.plant_types import get_all_plants, get_plant_by_id, search_plants

# PlantNet API - חינמי, עד 500 זיהויים ביום
# הרשם ב-https://my.plantnet.org/ וקבל מפתח
PLANTNET_API_KEY = os.environ.get('PLANTNET_API_KEY', '2b10placeholder')
PLANTNET_API_URL = "https://my-api.plantnet.org/v2/identify/all"

# ===================== הגדרות =====================
app = Flask(__name__, static_folder='../web')
CORS(app)

# API Key פשוט לאבטחת הנתונים (שנה את הערך!)
API_KEY = os.environ.get('API_KEY', 'plant-monitor-secret-123')

# נתיב מסד נתונים - בענן נשמר ב-/tmp או בדיסק persistent
if os.environ.get('RENDER'):
    # Render - שימוש בדיסק persistent אם קיים, אחרת /tmp
    DB_PATH = os.environ.get('DB_PATH', '/tmp/plant_data.db')
else:
    DB_PATH = os.path.join(os.path.dirname(__file__), 'plant_data.db')


def get_db():
    """חיבור למסד הנתונים"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """יצירת טבלאות במסד הנתונים"""
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            device_name TEXT,
            moisture_percent INTEGER,
            moisture_raw INTEGER,
            voltage REAL,
            boot_count INTEGER,
            sleep_minutes INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id INTEGER NOT NULL,
            command TEXT DEFAULT 'measure',
            status TEXT DEFAULT 'pending',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS devices (
            device_id INTEGER PRIMARY KEY,
            device_name TEXT,
            last_seen DATETIME,
            moisture_threshold_low INTEGER DEFAULT 30,
            moisture_threshold_high INTEGER DEFAULT 70,
            interval_minutes INTEGER DEFAULT 30,
            plant_type TEXT DEFAULT 'ficus',
            battery_percent INTEGER DEFAULT NULL
        )
    ''')
    # טבלת צמחים מותאמים אישית (שנוספו ע"י המשתמש)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS custom_plants (
            id TEXT PRIMARY KEY,
            name_he TEXT NOT NULL,
            name_en TEXT NOT NULL,
            category TEXT DEFAULT 'medium',
            moisture_min INTEGER DEFAULT 30,
            moisture_max INTEGER DEFAULT 70,
            temp_min INTEGER DEFAULT 15,
            temp_max INTEGER DEFAULT 30,
            water_tip_he TEXT DEFAULT '',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def verify_api_key():
    """בדיקת API Key לבקשות POST"""
    key = request.headers.get('X-API-Key') or request.args.get('api_key')
    if key != API_KEY:
        return False
    return True


# ===================== API Endpoints =====================

@app.route('/api/data', methods=['POST'])
def receive_data():
    """קבלת נתונים מה-ESP32"""
    try:
        # בדיקת API Key
        if not verify_api_key():
            return jsonify({'error': 'Invalid API key'}), 401

        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data received'}), 400

        conn = get_db()

        # שמירת הקריאה
        conn.execute('''
            INSERT INTO readings
            (device_id, device_name, moisture_percent, moisture_raw, voltage, boot_count, sleep_minutes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('device_id'),
            data.get('device_name'),
            data.get('moisture_percent'),
            data.get('moisture_raw'),
            data.get('voltage'),
            data.get('boot_count'),
            data.get('sleep_minutes')
        ))

        # עדכון/יצירת מכשיר (כולל אחוז סוללה)
        battery = data.get('battery_percent')
        conn.execute('''
            INSERT INTO devices (device_id, device_name, last_seen, battery_percent)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(device_id) DO UPDATE SET
                device_name = excluded.device_name,
                last_seen = excluded.last_seen,
                battery_percent = excluded.battery_percent
        ''', (
            data.get('device_id'),
            data.get('device_name'),
            datetime.now().isoformat(),
            battery
        ))

        conn.commit()
        conn.close()

        print(f"Data from device {data.get('device_id')} "
              f"({data.get('device_name')}): {data.get('moisture_percent')}%")

        return jsonify({
            'status': 'ok',
            'message': 'Data received successfully'
        }), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/devices', methods=['GET'])
def get_devices():
    """רשימת כל המכשירים"""
    conn = get_db()
    devices = conn.execute('''
        SELECT d.*, d.interval_minutes,
               r.moisture_percent as last_moisture,
               r.moisture_raw as last_raw,
               r.voltage as last_voltage,
               r.timestamp as last_reading_time
        FROM devices d
        LEFT JOIN readings r ON r.id = (
            SELECT id FROM readings
            WHERE device_id = d.device_id
            ORDER BY timestamp DESC LIMIT 1
        )
        ORDER BY d.device_id
    ''').fetchall()
    conn.close()

    return jsonify([dict(d) for d in devices])


@app.route('/api/readings/<int:device_id>', methods=['GET'])
def get_readings(device_id):
    """קריאות של מכשיר ספציפי"""
    hours = request.args.get('hours', 24, type=int)
    limit = request.args.get('limit', 500, type=int)

    conn = get_db()
    readings = conn.execute('''
        SELECT * FROM readings
        WHERE device_id = ?
        AND timestamp >= datetime('now', ? || ' hours')
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (device_id, -hours, limit)).fetchall()
    conn.close()

    return jsonify([dict(r) for r in readings])


@app.route('/api/readings/all', methods=['GET'])
def get_all_readings():
    """כל הקריאות האחרונות"""
    hours = request.args.get('hours', 24, type=int)

    conn = get_db()
    readings = conn.execute('''
        SELECT * FROM readings
        WHERE timestamp >= datetime('now', ? || ' hours')
        ORDER BY timestamp DESC
    ''', (-hours,)).fetchall()
    conn.close()

    return jsonify([dict(r) for r in readings])


@app.route('/api/device/<int:device_id>/threshold', methods=['POST'])
def set_threshold(device_id):
    """הגדרת סף לחות להתראה"""
    if not verify_api_key():
        return jsonify({'error': 'Invalid API key'}), 401

    data = request.get_json()
    conn = get_db()
    conn.execute('''
        UPDATE devices SET
            moisture_threshold_low = ?,
            moisture_threshold_high = ?
        WHERE device_id = ?
    ''', (
        data.get('low', 30),
        data.get('high', 70),
        device_id
    ))
    conn.commit()
    conn.close()

    return jsonify({'status': 'ok'})


@app.route('/api/device/<int:device_id>/settings', methods=['GET'])
def get_settings(device_id):
    """ESP32 מקבל הגדרות (תדירות מדידה וכו')"""
    conn = get_db()
    device = conn.execute(
        'SELECT * FROM devices WHERE device_id = ?', (device_id,)
    ).fetchone()
    conn.close()

    if device:
        return jsonify({
            'interval_minutes': device['interval_minutes'] or 30,
            'threshold_low': device['moisture_threshold_low'] or 30,
            'threshold_high': device['moisture_threshold_high'] or 70
        })

    return jsonify({'interval_minutes': 30, 'threshold_low': 30, 'threshold_high': 70})


@app.route('/api/device/<int:device_id>/settings', methods=['POST'])
def update_settings(device_id):
    """עדכון הגדרות מהדשבורד"""
    data = request.get_json()
    conn = get_db()

    if 'interval_minutes' in data:
        interval = max(1, min(1440, int(data['interval_minutes'])))
        conn.execute('UPDATE devices SET interval_minutes = ? WHERE device_id = ?',
                      (interval, device_id))

    if 'threshold_low' in data:
        conn.execute('UPDATE devices SET moisture_threshold_low = ? WHERE device_id = ?',
                      (data['threshold_low'], device_id))

    if 'threshold_high' in data:
        conn.execute('UPDATE devices SET moisture_threshold_high = ? WHERE device_id = ?',
                      (data['threshold_high'], device_id))

    if 'plant_type' in data:
        conn.execute('UPDATE devices SET plant_type = ? WHERE device_id = ?',
                      (data['plant_type'], device_id))

    conn.commit()
    conn.close()
    return jsonify({'status': 'ok'})


@app.route('/api/command/<int:device_id>', methods=['GET'])
def get_command(device_id):
    """ESP32 בודק אם יש פקודות ממתינות"""
    if not verify_api_key():
        return jsonify({'error': 'Invalid API key'}), 401

    conn = get_db()
    cmd = conn.execute('''
        SELECT * FROM commands
        WHERE device_id = ? AND status = 'pending'
        ORDER BY created_at ASC LIMIT 1
    ''', (device_id,)).fetchone()

    if cmd:
        conn.execute('UPDATE commands SET status = ? WHERE id = ?',
                      ('done', cmd['id']))
        conn.commit()
        conn.close()
        return jsonify({'command': cmd['command'], 'id': cmd['id']})

    conn.close()
    return jsonify({'command': None})


@app.route('/api/command/<int:device_id>', methods=['POST'])
def send_command(device_id):
    """שליחת פקודה למכשיר (מהדשבורד)"""
    data = request.get_json()
    command = data.get('command', 'measure')

    conn = get_db()
    conn.execute('''
        INSERT INTO commands (device_id, command, status, created_at)
        VALUES (?, ?, 'pending', ?)
    ''', (device_id, command, datetime.now().isoformat()))
    conn.commit()
    conn.close()

    return jsonify({'status': 'ok', 'message': f'Command "{command}" queued'})


@app.route('/api/plants', methods=['GET'])
def get_plants():
    """רשימת כל סוגי הצמחים (מובנים + מותאמים אישית), עם אפשרות חיפוש"""
    query = request.args.get('q', '')

    # שליפת צמחים מותאמים אישית מה-DB
    conn = get_db()
    custom_rows = conn.execute('SELECT * FROM custom_plants ORDER BY name_he').fetchall()
    conn.close()
    custom_plants = [dict(r) for r in custom_rows]
    # הסר שדה created_at מהתוצאה
    for p in custom_plants:
        p.pop('created_at', None)
        p['custom'] = True  # סימון שזה צמח מותאם אישית

    if query:
        builtin = search_plants(query)
        # חיפוש גם בצמחים מותאמים
        q = query.lower().strip()
        custom_filtered = [p for p in custom_plants if
                           q in p.get('name_he', '').lower() or
                           q in p.get('name_en', '').lower() or
                           q in p.get('id', '').lower()]
        return jsonify(builtin + custom_filtered)

    return jsonify(get_all_plants() + custom_plants)


@app.route('/api/plants/custom', methods=['POST'])
def add_custom_plant():
    """הוספת צמח מותאם אישית למאגר"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data'}), 400

    name_he = data.get('name_he', '').strip()
    name_en = data.get('name_en', '').strip()
    if not name_he and not name_en:
        return jsonify({'error': 'Plant name required'}), 400

    # יצירת ID מהשם האנגלי או העברי
    base_name = name_en if name_en else name_he
    plant_id = data.get('id') or base_name.lower().replace(' ', '_').replace('-', '_')
    # הסר תווים לא חוקיים
    plant_id = ''.join(c for c in plant_id if c.isalnum() or c == '_')
    plant_id = f"custom_{plant_id}"

    # בדוק שלא קיים כבר
    existing = get_plant_by_id(plant_id)
    if existing:
        return jsonify({'error': 'Plant already exists', 'plant': existing}), 409

    moisture_min = max(0, min(100, int(data.get('moisture_min', 30))))
    moisture_max = max(moisture_min, min(100, int(data.get('moisture_max', 70))))

    # קביעת קטגוריה אוטומטית לפי טווח לחות
    avg_moisture = (moisture_min + moisture_max) / 2
    if avg_moisture < 35:
        category = 'low'
    elif avg_moisture < 55:
        category = 'medium'
    else:
        category = 'high'

    plant = {
        'id': plant_id,
        'name_he': name_he or name_en,
        'name_en': name_en or name_he,
        'category': data.get('category', category),
        'moisture_min': moisture_min,
        'moisture_max': moisture_max,
        'temp_min': int(data.get('temp_min', 15)),
        'temp_max': int(data.get('temp_max', 30)),
        'water_tip_he': data.get('water_tip_he', f'לחות מומלצת: {moisture_min}%-{moisture_max}%'),
    }

    conn = get_db()
    try:
        conn.execute('''
            INSERT INTO custom_plants (id, name_he, name_en, category, moisture_min, moisture_max, temp_min, temp_max, water_tip_he)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (plant['id'], plant['name_he'], plant['name_en'], plant['category'],
              plant['moisture_min'], plant['moisture_max'], plant['temp_min'], plant['temp_max'],
              plant['water_tip_he']))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Plant ID already exists'}), 409
    conn.close()

    plant['custom'] = True
    return jsonify({'status': 'ok', 'plant': plant}), 201


@app.route('/api/plants/custom/<plant_id>', methods=['DELETE'])
def delete_custom_plant(plant_id):
    """מחיקת צמח מותאם אישית"""
    conn = get_db()
    result = conn.execute('DELETE FROM custom_plants WHERE id = ?', (plant_id,))
    conn.commit()
    deleted = result.rowcount > 0
    conn.close()

    if deleted:
        return jsonify({'status': 'ok'})
    return jsonify({'error': 'Plant not found'}), 404


@app.route('/api/device/<int:device_id>/plant', methods=['POST'])
def set_plant_type(device_id):
    """עדכון סוג צמח למכשיר"""
    data = request.get_json()
    plant_id = data.get('plant_type', 'ficus')

    # חיפוש במאגר המובנה
    plant = get_plant_by_id(plant_id)

    # אם לא נמצא - חיפוש במאגר המותאם אישית
    if not plant:
        conn = get_db()
        row = conn.execute('SELECT * FROM custom_plants WHERE id = ?', (plant_id,)).fetchone()
        conn.close()
        if row:
            plant = dict(row)
            plant.pop('created_at', None)

    if not plant:
        return jsonify({'error': 'Unknown plant type'}), 400

    conn = get_db()
    conn.execute('''
        UPDATE devices SET
            plant_type = ?,
            moisture_threshold_low = ?,
            moisture_threshold_high = ?
        WHERE device_id = ?
    ''', (plant_id, plant['moisture_min'], plant['moisture_max'], device_id))
    conn.commit()
    conn.close()

    return jsonify({'status': 'ok', 'plant': plant})


@app.route('/api/identify', methods=['POST'])
def identify_plant():
    """זיהוי צמח מתמונה באמצעות PlantNet API"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400

        image = request.files['image']

        # שליחה ל-PlantNet API
        response = http_requests.post(
            PLANTNET_API_URL,
            files={'images': (image.filename, image.read(), image.content_type)},
            data={
                'organs': 'leaf',  # ברירת מחדל - זיהוי לפי עלה
            },
            params={
                'api-key': PLANTNET_API_KEY,
                'include-related-images': 'false',
                'no-reject': 'false',
                'lang': 'he',
            },
            timeout=30
        )

        if response.status_code != 200:
            return jsonify({
                'error': 'PlantNet API error',
                'status': response.status_code,
                'message': response.text
            }), 500

        result = response.json()
        results_list = result.get('results', [])

        if not results_list:
            return jsonify({'error': 'No plant identified', 'suggestions': []}), 200

        # עיבוד תוצאות - חיפוש במאגר המקומי
        suggestions = []
        for r in results_list[:5]:  # עד 5 תוצאות
            species = r.get('species', {})
            scientific_name = species.get('scientificNameWithoutAuthor', '')
            common_names = species.get('commonNames', [])
            score = r.get('score', 0)

            # חיפוש במאגר המקומי
            local_match = None
            search_terms = [scientific_name] + common_names
            for term in search_terms:
                if term:
                    matches = search_plants(term)
                    if matches:
                        local_match = matches[0]
                        break

            suggestions.append({
                'scientific_name': scientific_name,
                'common_names': common_names,
                'score': round(score * 100, 1),
                'local_match': local_match
            })

        return jsonify({
            'status': 'ok',
            'suggestions': suggestions,
            'best_match': suggestions[0] if suggestions else None
        })

    except Exception as e:
        print(f"Identify error: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """בדיקת תקינות השרת - Render משתמש בזה"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()})


# ===================== Web Dashboard =====================

@app.route('/')
def dashboard():
    """הצגת הדשבורד"""
    return send_from_directory('../web', 'index.html')


@app.route('/<path:filename>')
def static_files(filename):
    """קבצים סטטיים"""
    return send_from_directory('../web', filename)


# ===================== הרצת השרת =====================

# אתחול מסד הנתונים
init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = not os.environ.get('RENDER')

    print("\n Plant Monitor Server")
    print("=" * 40)
    print(f"  Dashboard: http://localhost:{port}")
    print(f"  API:       http://localhost:{port}/api/data")
    print(f"  Database:  {DB_PATH}")
    print(f"  API Key:   {API_KEY[:8]}...")
    print("=" * 40)
    print("Waiting for ESP32 data...\n")

    app.run(host='0.0.0.0', port=port, debug=debug)
