from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATOS_SOCIALES = {
    "Marriott": {"positivo": 70, "negativo": 30, "total": 10},
    "Hilton": {"positivo": 45, "negativo": 55, "total": 8},
    "Holiday Inn": {"positivo": 60, "negativo": 40, "total": 12}
}

@app.route('/opiniones_social', methods=['GET'])
def get_opiniones_social():
    data = []
    for hotel, stats in DATOS_SOCIALES.items():
        data.append({
            'hotel': hotel,
            'positivo': stats['positivo'],
            'negativo': stats['negativo'],
            'total_opiniones': stats['total']
        })
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)