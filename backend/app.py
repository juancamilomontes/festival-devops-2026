from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
import os
import time

app = Flask(__name__)
CORS(app)

# Variables de entorno para la conexión a MySQL
DB_HOST = os.environ.get('DB_HOST', 'db')
DB_USER = os.environ.get('DB_USER', 'festival_user')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'festival_pass')
DB_NAME = os.environ.get('DB_NAME', 'festival_db')


def get_db_connection():
    """Intenta conectar a MySQL con reintentos."""
    intentos = 0
    while intentos < 5:
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return conn
        except mysql.connector.Error:
            intentos += 1
            time.sleep(3)
    return None


def init_db():
    """Crea la tabla e inserta datos si no existen."""
    conn = get_db_connection()
    if conn is None:
        return

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS concierto (
            id INT AUTO_INCREMENT PRIMARY KEY,
            festival VARCHAR(100),
            fecha VARCHAR(50),
            lugar VARCHAR(100),
            capacidad INT,
            estado VARCHAR(30)
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM concierto")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute("""
            INSERT INTO concierto (festival, fecha, lugar, capacidad, estado)
            VALUES (%s, %s, %s, %s, %s)
        """, ('Pacific DevOps Music Fest', '15 de Agosto 2026',
              'Medellín, Colombia', 5000, 'Entradas disponibles'))
        conn.commit()

    cursor.close()
    conn.close()


@app.route('/api/concierto', methods=['GET'])
def get_concierto():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM concierto LIMIT 1")
    data = cursor.fetchone()
    cursor.close()
    conn.close()

    if data:
        return jsonify(data)
    return jsonify({"error": "Sin datos"}), 404


@app.route('/api/artistas', methods=['GET'])
def get_artistas():
    artistas = [
        {"nombre": "The Linux Penguins", "genero": "Rock alternativo"},
        {"nombre": "Docker Beats", "genero": "Electronic / EDM"},
        {"nombre": "Kubernetes Flow", "genero": "Jazz fusión"},
        {"nombre": "Git & Roll", "genero": "Pop rock"}
    ]
    return jsonify({"artistas": artistas})


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "servicio": "backend-festival"})


if __name__ == '__main__':
    time.sleep(5)  # Espera a que MySQL levante
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
