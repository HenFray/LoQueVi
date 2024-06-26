from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('loquevi.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM contenido').fetchall()
    conn.close()
    return render_template('index.html', rows=rows)

@app.route('/filter', methods=['POST'])
def filter_data():
    filters = request.json
    query = 'SELECT * FROM contenido WHERE 1=1'
    params = []

    if filters.get('Tipo'):
        query += ' AND Tipo = ?'
        params.append(filters['Tipo'])
    
    if filters.get('Plataforma'):
        query += ' AND Plataforma = ?'
        params.append(filters['Plataforma'])

    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()

    data = [dict(row) for row in rows]
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)