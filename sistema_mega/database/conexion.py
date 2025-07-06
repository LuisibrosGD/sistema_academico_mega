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
            conexion.rollback()  # 🔥 Muy importante
        finally:
            cursor.close()
            conexion.close()

# Ejecutar un procedimiento almacenado sin OUT. Con solo IN
def ejecutar_procedimiento(nombre_proc, parametros=None):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.callproc(nombre_proc, parametros or [])
            conexion.commit()
            print("✅ Procedimiento ejecutado correctamente")
        except mysql.connector.Error as err:
            print(f"❌ Error al ejecutar el procedimiento: {err}")
            conexion.rollback()
        finally:
            cursor.close()
            conexion.close()

# Ejecutar procedimiento con OUT
def ejecutar_procedimiento_con_out(nombre_proc, parametros=None):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            # Si hay parámetros, pásalos; si no, llama sin ellos
            if parametros is not None:
                resultados = cursor.callproc(nombre_proc, parametros)
            else:
                resultados = cursor.callproc(nombre_proc)

            conexion.commit()
            return resultados  # Lista con IN y OUT
        except mysql.connector.Error as err:
            print(f"❌ Error al ejecutar el procedimiento con OUT: {err}")
            conexion.rollback()
        finally:
            cursor.close()
            conexion.close()
