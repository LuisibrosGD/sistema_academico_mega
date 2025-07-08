import mysql.connector

def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",        # o el host de tu RDS si es en la nube
        user="invitado_user",
        password="invitado_pass",
        database="academia_mega"
    )

def ejecutar_select(query, datos=None):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(query, datos)
            resultados = cursor.fetchall()
            return resultados
        except mysql.connector.Error as err:
            print(f"❌ Error en la consulta: {err}")
        finally:
            cursor.close()
            conexion.close()