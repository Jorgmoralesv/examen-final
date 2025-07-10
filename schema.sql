-- schema.sql
-- Elimina la tabla 'posts' si ya existe para asegurar una base de datos limpia
DROP TABLE IF EXISTS posts;

-- Crea la tabla 'posts'
CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID único para cada post, se incrementa automáticamente
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de creación del post, se establece automáticamente
    title TEXT NOT NULL, -- Título del post, no puede ser nulo
    content TEXT NOT NULL -- Contenido del post, no puede ser nulo
);