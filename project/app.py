from flask import Flask, render_template, request, jsonify, g
import sqlite3

app = Flask(__name__)

DATABASE = 'loquevi.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.before_request
def before_request():
    g.db = get_db_connection()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/get_contenido', methods=['GET'])
def get_contenido():
    cursor = g.db.execute('SELECT rowid as id, * FROM contenido')
    contenido = cursor.fetchall()
    return jsonify([dict(row) for row in contenido])

@app.route('/add_contenido', methods=['POST'])
def add_contenido():
    data = request.get_json()

    try:
        año = data['año']
    except KeyError:
        año = None  # Asigna un valor por defecto
        # O muestra un mensaje de error al usuario

    query = '''INSERT INTO contenido 
                (Nombre, Tipo, Año, Plataforma, Comentario, Puntuacion, Vista, AñoDeVisualisacion) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)'''
    params = (
        data['nombre'],
        data['tipo'],
        data['año'],
        data['plataforma'],
        data['comentario'],
        data['puntuacion'],
        data['vista'],
        data['añovisualizacion']
    )

    g.db.execute(query, params)
    g.db.commit()

    return jsonify({'status': 'success'})


@app.route('/update_contenido', methods=['POST'])
def update_contenido():
    data = request.get_json()
    # Assuming 'Nombre' is a unique field for each content
    query = '''UPDATE contenido SET 
                Nombre = ?, Tipo = ?, Año = ?, Plataforma = ?, Comentario = ?, Puntuacion = ?, Vista = ?, AñoDeVisualisacion = ? 
                WHERE Nombre = ?'''
    params = (
        data['nombre'],
        data['tipo'],
        data['año'],
        data['plataforma'],
        data['comentario'],
        data['puntuacion'],
        data['vista'],
        data['añovisualizacion'],
        data['nombre']  # Use 'nombre' here to match against the unique 'Nombre' field
    )
    g.db.execute(query, params)
    g.db.commit()
    return jsonify({'status': 'success'})


@app.route('/delete_contenido', methods=['POST'])
def delete_contenido():
  data = request.get_json()
  # Assuming 'Nombre' is a unique field for each content
  query = 'DELETE FROM contenido WHERE Nombre = ?'
  g.db.execute(query, (data['Nombre'],))
  g.db.commit()
  return jsonify({'status': 'success'})


@app.route('/filter_data', methods=['POST'])
def filter_data():
  data = request.get_json()
  # Assuming filters are applied based on a combination of Tipo and Plataforma
  query_base = "SELECT Nombre, Tipo, Año, Plataforma, Comentario, Puntuacion, Vista, AñoDeVisualisacion FROM contenido"
  query_filters = ""
  params = []

  if data.get('Tipo'):
    query_filters += " WHERE Tipo = ?"
    params.append(data['Tipo'])

  if data.get('Plataforma'):
    if query_filters:  # Add AND only if there's already a filter
      query_filters += " AND"
    query_filters += " Plataforma = ?"
    params.append(data['Plataforma'])

  # Combine base query with optional filters
  query = query_base + query_filters

  cursor = g.db.execute(query, params)
  rows = cursor.fetchall()

  # Transform rows to dictionaries (without relying on 'id')
  results = [dict(row) for row in rows]
  return jsonify(results)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
