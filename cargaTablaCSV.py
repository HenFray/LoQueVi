import pandas as pd
import sqlite3

# Leer el archivo CSV
csv_file_path = 'D:\Programacion\LoQueVi\loquevi.csv'
df = pd.read_csv(csv_file_path)

# Conectar a la base de datos SQLite (creará la base de datos si no existe)
conn = sqlite3.connect('D:\Programacion\SQLITE\DBS\loquevi.db')

# Crear el cursor
cur = conn.cursor()

# Crear la tabla con ID incremental
cur.execute('''
CREATE TABLE IF NOT EXISTS contenido (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Nombre TEXT,
    Tipo TEXT,
    Año INTEGER,
    Plataforma TEXT,
    Comentario TEXT,
    Puntuacion TEXT,
    Vista BOOLEAN,
    AñoDeVisualisacion INTEGER
);
''')

# Guardar los cambios
conn.commit()

# Escribir los datos del DataFrame en la tabla de la base de datos
df.to_sql('contenido', conn, if_exists='replace', index=False)

# Cerrar la conexión
conn.close()
