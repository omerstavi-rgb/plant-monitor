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
        CREATE TABLE IF NOT EXISTS devices (
            device_id INTEGER PRIMARY KEY,
            device_name TEXT,
            last_seen DATETIME,
            moisture_threshold_low INTEGER DEFAULT 30,
            moisture_threshold_high INTEGER DEFAULT 70
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

        # עדכון/יצירת מכשיר
        conn.execute('''
            INSERT INTO devices (device_id, device_name, last_seen)
            VALUES (?, ?, ?)
            ON CONFLICT(device_id) DO UPDATE SET
                device_name = excluded.device_name,
                last_seen = excluded.last_seen
        ''', (
            data.get('device_id'),
            data.get('device_name'),
            datetime.now().isoformat()
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
        SELECT d.*,
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
