from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

CSV_FILE = 'opiniones_manuales.csv'

if not os.path.exists(CSV_FILE):
    datos = []
    for hotel in ['Marriott', 'Hilton', 'Holiday Inn']:
        for i in range(10):
            polaridad = 'positivo' if i < 6 else 'negativo'
            datos.append({'hotel': hotel, 'opinion': f'Opinión {i+1}', 'polaridad': polaridad})
    df = pd.DataFrame(datos)
    df.to_csv(CSV_FILE, index=False)
    print(f"Archivo {CSV_FILE} creado!")

@app.route('/opiniones_csv', methods=['GET'])
def get_opiniones_csv():
    df = pd.read_csv(CSV_FILE)
    resultado = {}
    for hotel in df['hotel'].unique():
        df_hotel = df[df['hotel'] == hotel]
        total = len(df_hotel)
        positivos = len(df_hotel[df_hotel['polaridad'] == 'positivo'])
        negativos = len(df_hotel[df_hotel['polaridad'] == 'negativo'])
        resultado[hotel] = {
            'positivo': round((positivos / total) * 100, 1),
            'negativo': round((negativos / total) * 100, 1),
            'total_opiniones': total
        }
    data = [{'hotel': h, **resultado[h]} for h in resultado]
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)