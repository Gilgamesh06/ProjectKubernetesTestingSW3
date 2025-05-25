-- Conectarse a la base de datos correcta (opcional, psql lo hace con -d)
-- \c ecommerce_inventario Solus;

-- Eliminar tablas si existen para asegurar un estado limpio (OPCIONAL, ¡CUIDADO!)
-- Si quieres que este script sea re-ejecutable y siempre empiece de cero,
-- puedes añadir estas líneas. Pero si ya tienes datos que quieres conservar, NO las uses.
/*
DROP TABLE IF EXISTS detalle_merma;
DROP TABLE IF EXISTS merma;
DROP TABLE IF EXISTS inventario;
DROP TABLE IF EXISTS producto;
DROP TABLE IF EXISTS detalle_producto;
*/

-- Crear tabla detalle_producto
CREATE TABLE IF NOT EXISTS detalle_producto (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(255),
    composicion VARCHAR(255),
    pais VARCHAR(100)
);
ALTER TABLE detalle_producto OWNER TO "Solus"; -- Asegurar propietario correcto

-- Crear tabla producto
CREATE TABLE IF NOT EXISTS producto (
    id SERIAL PRIMARY KEY,
    detalle_producto_id INTEGER, -- FK se añade después si quieres, o directamente
    referencia VARCHAR(50) UNIQUE,
    nombre VARCHAR(255),
    tipo VARCHAR(100),
    subtipo VARCHAR(100),
    talla VARCHAR(50),
    color VARCHAR(50),
    target VARCHAR(50),
    precio_unid NUMERIC(10, 2),
    precio_venta NUMERIC(10, 2),
    CONSTRAINT fk_detalle_producto
        FOREIGN KEY(detalle_producto_id)
        REFERENCES detalle_producto(id)
        ON DELETE SET NULL -- O ON DELETE CASCADE, dependiendo de tu lógica de negocio
);
ALTER TABLE producto OWNER TO "Solus";

-- Crear tabla inventario
CREATE TABLE IF NOT EXISTS inventario (
    id SERIAL PRIMARY KEY,
    producto_id INTEGER UNIQUE, -- Asumo que cada producto tiene una única entrada de inventario
    cantidad INTEGER,
    CONSTRAINT fk_producto_inventario
        FOREIGN KEY(producto_id)
        REFERENCES producto(id)
        ON DELETE CASCADE
);
ALTER TABLE inventario OWNER TO "Solus";

-- Crear tabla merma
CREATE TABLE IF NOT EXISTS merma (
    id SERIAL PRIMARY KEY,
    referencia VARCHAR(50) UNIQUE,
    fecha TIMESTAMP
);
ALTER TABLE merma OWNER TO "Solus";

-- Crear tabla detalle_merma
CREATE TABLE IF NOT EXISTS detalle_merma (
    id SERIAL PRIMARY KEY,
    producto_id INTEGER,
    merma_id INTEGER,
    cantidad INTEGER,
    descripcion VARCHAR(255),
    CONSTRAINT fk_producto_detalle_merma
        FOREIGN KEY(producto_id)
        REFERENCES producto(id)
        ON DELETE SET NULL, -- O CASCADE
    CONSTRAINT fk_merma_detalle_merma
        FOREIGN KEY(merma_id)
        REFERENCES merma(id)
        ON DELETE CASCADE
);
ALTER TABLE detalle_merma OWNER TO "Solus";

-- Mensaje de confirmación (opcional, solo para psql)
\echo 'Esquema de la base de datos de inventario creado/verificado.'