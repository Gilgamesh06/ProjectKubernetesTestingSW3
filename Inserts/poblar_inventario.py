import psycopg2
from faker import Faker
import random
from datetime import datetime

# --- Configuración de la Conexión a la BD de Inventario ---
DB_CONFIG_INVENTARIO = {
    "host": "localhost",
    "port": 5433,  # Puerto mapeado en docker-compose.yml para db-inventario
    "database": "ecommerce_inventario",
    "user": "Solus",
    "password": "123456"
}

fake = Faker(['es_ES', 'es_MX', 'en_US']) # Variedad de datos

def get_db_connection(config):
    """Establece y devuelve una conexión a la base de datos."""
    try:
        conn = psycopg2.connect(**config)
        print(f"Conexión a la base de datos '{config['database']}' en {config['host']}:{config['port']} exitosa.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error al conectar a PostgreSQL ({config['host']}:{config['port']}, DB: {config['database']}): {e}")
        print("Asegúrate de que el contenedor 'db-inventario' esté corriendo y accesible en el puerto mapeado.")
        raise
    except psycopg2.Error as e:
        print(f"Error general al conectar a PostgreSQL: {e}")
        raise

# --- Listas para almacenar IDs generados ---
generated_detalle_producto_ids = []
generated_producto_ids = []
generated_merma_ids = []

# --- Funciones de Población ---

def populate_detalle_producto(cursor, num_detalles):
    """Puebla la tabla detalle_producto y devuelve los IDs generados."""
    print("\n--- Poblando tabla 'detalle_producto' ---")
    ids = []
    for i in range(num_detalles):
        descripcion = fake.sentence(nb_words=random.randint(8, 15))
        composicion = ", ".join(fake.words(nb=random.randint(2, 4)))
        pais = fake.country()
        try:
            cursor.execute(
                "INSERT INTO detalle_producto (descripcion, composicion, pais) VALUES (%s, %s, %s) RETURNING id;",
                (descripcion, composicion, pais)
            )
            ids.append(cursor.fetchone()[0])
            if (i + 1) % 100 == 0 or (i + 1) == num_detalles:
                print(f"  Insertados {i + 1}/{num_detalles} detalles de producto...")
        except psycopg2.Error as e:
            print(f"Error insertando en detalle_producto: {e}")
            raise
    return ids

def populate_producto(cursor, num_productos, detalle_ids):
    """Puebla la tabla producto y devuelve los IDs generados."""
    print("\n--- Poblando tabla 'producto' ---")
    if not detalle_ids and num_productos > 0: # Solo advertir si se esperan productos pero no hay detalles
        print("  Advertencia: No hay IDs de 'detalle_producto' para asignar. Se intentará insertar NULL.")
        # Esto fallará si la FK es NOT NULL. El error de psycopg2 será más específico.

    ids = []
    tipos_comunes = ["Ropa", "Electrónica", "Hogar", "Libros", "Deportes", "Juguetes", "Alimentos", "Belleza"]
    subtipos_ropa = ["Camiseta", "Pantalón", "Chaqueta", "Zapatos", "Vestido", "Accesorio"]
    colores = ["Rojo", "Azul", "Verde", "Negro", "Blanco", "Gris", "Amarillo", "Naranja", "Rosa", "Morado"]
    tallas = ["XS", "S", "M", "L", "XL", "XXL", "Talla Única"]
    targets = ["Hombre", "Mujer", "Niño", "Niña", "Unisex", "Bebé"]

    for i in range(num_productos):
        detalle_producto_id_fk = random.choice(detalle_ids) if detalle_ids else None
        referencia = fake.unique.ean13()
        nombre = fake.bs().title() + " " + fake.word().capitalize()
        tipo = random.choice(tipos_comunes)

        if tipo == "Ropa":
            subtipo = random.choice(subtipos_ropa)
            talla_prod = random.choice(tallas)
        else:
            subtipo = fake.word().capitalize()
            talla_prod = "N/A"

        color_prod = random.choice(colores)
        target_prod = random.choice(targets)
        precio_unid = round(random.uniform(1.00, 300.00), 2)
        precio_venta = round(precio_unid * random.uniform(1.1, 2.5), 2)

        try:
            cursor.execute(
                """
                INSERT INTO producto (
                    detalle_producto_id, referencia, nombre, tipo, subtipo,
                    talla, color, target, precio_unid, precio_venta
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
                """,
                (detalle_producto_id_fk, referencia, nombre, tipo, subtipo,
                 talla_prod, color_prod, target_prod, precio_unid, precio_venta)
            )
            ids.append(cursor.fetchone()[0])
            if (i + 1) % 100 == 0 or (i + 1) == num_productos:
                print(f"  Insertados {i + 1}/{num_productos} productos...")
        except psycopg2.Error as e:
            print(f"Error insertando en producto: {e}")
            raise
    return ids

def populate_inventario_stock(cursor, producto_ids):
    """Puebla la tabla inventario con stock para cada producto."""
    print("\n--- Poblando tabla 'inventario' (stock) ---")
    if not producto_ids:
        print("  No hay IDs de producto para asignar stock. Se omite la tabla 'inventario'.")
        return

    for i, producto_id_fk in enumerate(producto_ids):
        cantidad = random.randint(0, 500)
        try:
            cursor.execute(
                "INSERT INTO inventario (producto_id, cantidad) VALUES (%s, %s);",
                (producto_id_fk, cantidad)
            )
            if (i + 1) % 100 == 0 or (i + 1) == len(producto_ids):
                print(f"  Stock insertado para {i + 1}/{len(producto_ids)} productos...")
        except psycopg2.Error as e:
            print(f"Error insertando en inventario: {e}")
            raise
    

def populate_merma(cursor, num_mermas):
    """Puebla la tabla merma y devuelve los IDs generados."""
    print("\n--- Poblando tabla 'merma' ---")
    ids = []
    for i in range(num_mermas):
        referencia_merma = f"MER-{fake.unique.uuid4()[:8].upper()}"
        fecha_merma = fake.date_time_this_year(before_now=True, after_now=False, tzinfo=None)

        try:
            cursor.execute(
                "INSERT INTO merma (referencia, fecha) VALUES (%s, %s) RETURNING id;",
                (referencia_merma, fecha_merma)
            )
            ids.append(cursor.fetchone()[0])
            if (i + 1) % 50 == 0 or (i + 1) == num_mermas:
                print(f"  Insertados {i + 1}/{num_mermas} registros de merma...")
        except psycopg2.Error as e:
            print(f"Error insertando en merma: {e}")
            raise
    return ids

def populate_detalle_merma(cursor, merma_ids, producto_ids_disponibles):
    """Puebla la tabla detalle_merma."""
    print("\n--- Poblando tabla 'detalle_merma' ---")
    if not merma_ids:
        print("  No hay IDs de merma para crear detalles. Se omite 'detalle_merma'.")
        return
    if not producto_ids_disponibles:
        print("  No hay IDs de producto para asignar a detalles de merma. Se omite 'detalle_merma'.")
        return

    detalles_insertados_count = 0
    total_detalles_a_insertar_aprox = len(merma_ids) * 2 # Promedio de 2 items por merma
    for i, merma_id_fk in enumerate(merma_ids):
        num_items_mermados = random.randint(1, 3)
        for _ in range(num_items_mermados):
            producto_id_fk = random.choice(producto_ids_disponibles)
            cantidad_mermada = random.randint(1, 5)
            descripcion_merma_detalle = fake.sentence(nb_words=random.randint(4, 8))
            try:
                cursor.execute(
                    """
                    INSERT INTO detalle_merma (producto_id, merma_id, cantidad, descripcion)
                    VALUES (%s, %s, %s, %s);
                    """,
                    (producto_id_fk, merma_id_fk, cantidad_mermada, descripcion_merma_detalle)
                )
                detalles_insertados_count += 1
                if detalles_insertados_count % 50 == 0 or detalles_insertados_count == total_detalles_a_insertar_aprox : # Logueo periódico
                    print(f"  Insertados {detalles_insertados_count} detalles de merma (aprox. de {total_detalles_a_insertar_aprox})...")
            except psycopg2.Error as e:
                print(f"Error insertando en detalle_merma: {e}")
                raise
    print(f"  Insertados un total de {detalles_insertados_count} detalles de merma.")


# --- SCRIPT PRINCIPAL ---
if __name__ == '__main__':
    conn_inv = None
    cursor = None # Definir cursor fuera del try para que esté disponible en finally

    try:

        # Para "cantidad significativa":
        NUM_DETALLES_PRODUCTO = 200
        NUM_PRODUCTOS = 1000
        NUM_MERMAS = 50

        print(f"Iniciando población de la base de datos de Inventario...")
        print(f"Se generarán aproximadamente:")
        print(f"  - {NUM_DETALLES_PRODUCTO} registros en 'detalle_producto'")
        print(f"  - {NUM_PRODUCTOS} registros en 'producto' e 'inventario'")
        print(f"  - {NUM_MERMAS} registros en 'merma' y aprox. {NUM_MERMAS * 2} en 'detalle_merma'")


        conn_inv = get_db_connection(DB_CONFIG_INVENTARIO)
        cursor = conn_inv.cursor()

        generated_detalle_producto_ids = populate_detalle_producto(cursor, NUM_DETALLES_PRODUCTO)
        conn_inv.commit()
        print(f"Tabla 'detalle_producto' poblada con {len(generated_detalle_producto_ids)} registros.")

        generated_producto_ids = populate_producto(cursor, NUM_PRODUCTOS, generated_detalle_producto_ids)
        conn_inv.commit()
        print(f"Tabla 'producto' poblada con {len(generated_producto_ids)} registros.")

        populate_inventario_stock(cursor, generated_producto_ids)
        conn_inv.commit()
        print(f"Tabla 'inventario' (stock) poblada.")

        generated_merma_ids = populate_merma(cursor, NUM_MERMAS)
        conn_inv.commit()
        print(f"Tabla 'merma' poblada con {len(generated_merma_ids)} registros.")

        populate_detalle_merma(cursor, generated_merma_ids, generated_producto_ids)
        conn_inv.commit()
        print(f"Tabla 'detalle_merma' poblada.")

        print("\n¡Población de la base de datos de Inventario completada exitosamente!")

    except psycopg2.Error as e: # Captura errores específicos de psycopg2
        print(f"\nError de base de datos durante la población: {e}")
        if conn_inv:
            print("Realizando rollback de la transacción...")
            conn_inv.rollback()
    except Exception as e: # Captura cualquier otro error
        print(f"\nOcurrió un error inesperado: {e}")
        if conn_inv: # Si la conexión existe, intenta rollback
            print("Realizando rollback de la transacción debido a error inesperado...")
            conn_inv.rollback()
    finally:
        if cursor:
            cursor.close()
        if conn_inv:
            conn_inv.close()
            print("Conexión a la base de datos de Inventario cerrada.")