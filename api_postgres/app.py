from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db():
    conn = sqlite3.connect('hoteles.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reservaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            hotel TEXT,
            fecha TEXT,
            huesped TEXT
        )
    ''')
    
    count = conn.execute('SELECT COUNT(*) FROM reservaciones').fetchone()[0]
    if count == 0:
        hoteles = ['Marriott', 'Hilton', 'Holiday Inn', 'Marriott', 'Hilton', 'Hilton', 'Marriott', 'Holiday Inn']
        for h in hoteles:
            conn.execute('INSERT INTO reservaciones (hotel, fecha, huesped) VALUES (?, ?, ?)',
                        (h, '2024-01-15', 'Cliente'))
    conn.commit()
    conn.close()

init_db()

@app.route('/reservaciones', methods=['GET'])
def get_reservaciones():
    conn = get_db()
    cursor = conn.execute('''
        SELECT hotel, COUNT(*) as total_reservas
        FROM reservaciones
        GROUP BY hotel
        ORDER BY total_reservas DESC
    ''')
    rows = cursor.fetchall()
    conn.close()
    
    data = [{'hotel': row['hotel'], 'reservaciones': row['total_reservas']} for row in rows]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)