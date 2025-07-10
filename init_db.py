# init_db.py
import sqlite3

# Conecta a la base de datos. Si 'database.db' no existe, SQLite la creará.
connection = sqlite3.connect('database.db')

# Abre el archivo schema.sql y ejecuta su contenido para crear la tabla.
# El 'with' statement asegura que el archivo se cierre correctamente.
with open('schema.sql') as f:
    connection.executescript(f.read())

# Crea un objeto cursor para ejecutar comandos SQL.
cur = connection.cursor()

# Inserta algunos posts de ejemplo en la tabla.
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Primer Post de Ejemplo', 'Este es el contenido del primer post. Puedes editarlo o eliminarlo.')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Segundo Post Increíble', 'Aquí va el contenido de un segundo post, con más detalles interesantes.')
            )

# Guarda los cambios en la base de datos.
connection.commit()

# Cierra la conexión a la base de datos.
connection.close()

print("Base de datos 'database.db' creada y posts iniciales insertados exitosamente.")