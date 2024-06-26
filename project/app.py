from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Función para establecer conexión a la base de datos SQLite
def get_db_connection():
    conn = sqlite3.connect('loquevi.db')
    conn.row_factory = sqlite3.Row  # Para devolver filas como diccionarios
    return conn

# Ruta para filtrar datos basado en los parámetros recibidos
@app.route('/filter', methods=['POST'])
def filter_data():
    filters = request.json
    query = 'SELECT Nombre, Tipo, Año, Plataforma, Comentario, Puntuacion, Vista, AñoDeVisualisacion FROM contenido WHERE 1=1'
    params = []

    if filters.get('Tipo'):
        query += ' AND Tipo = ?'
        params.append(filters['Tipo'])
    
    if filters.get('Plataforma'):
        query += ' AND Plataforma = ?'
        params.append(filters['Plataforma'])

    conn = get_db_connection()
    cursor = conn.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    # Convertir resultados a formato JSON
    data = []
    for row in rows:
        data.append({
            'Nombre': row['Nombre'],
            'Tipo': row['Tipo'],
            'Año': row['Año'],
            'Plataforma': row['Plataforma'],
            'Comentario': row['Comentario'],
            'Puntuacion': row['Puntuacion'],
            'Vista': row['Vista'],
            'AñoDeVisualisacion': row['AñoDeVisualisacion']
        })

    return jsonify(data)

# Ruta principal para renderizar la página HTML
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
