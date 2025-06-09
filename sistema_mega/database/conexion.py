import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="mondongo",
        database="academia_mega"
    )

# Función para ejecutar una consulta SELECT
def ejecutar_select(query, datos=None):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(query,datos)
            resultados = cursor.fetchall()
            return resultados
        except mysql.connector.Error as err:
            print(f"❌ Error en la consulta: {err}")
        finally:
            cursor.close()
            conexion.close()

# Función para ejecutar consultas INSERT, UPDATE o DELETE
def ejecutar_modificacion(query, datos=None):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            if datos:
                cursor.execute(query, datos)
            else:
                cursor.execute(query)
            conexion.commit()
            print("✅ Consulta ejecutada correctamente")
        except mysql.connector.Error as err:
            print(f"❌ Error en la modificación: {err}")
        finally:
            cursor.close()
            conexion.close()