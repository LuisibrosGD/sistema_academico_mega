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
def ejecutar_procedimiento_con_out(nombre_proc, parametros=None, cantidad_out=1):
    conexion = obtener_conexion()
    if not conexion:
        return None if cantidad_out == 1 else [None] * cantidad_out

    cursor = conexion.cursor()
    try:
        # Si no se pasan parámetros IN, usar lista vacía
        parametros = parametros or []

        # Agregamos 'None' para los parámetros OUT
        parametros_completos = parametros + [None] * cantidad_out

        resultado = cursor.callproc(nombre_proc, parametros_completos)

        conexion.commit()

        # Extraer solo los valores OUT del final
        outs = resultado[-cantidad_out:]
        return outs[0] if cantidad_out == 1 else outs

    except mysql.connector.Error as err:
        print(f"❌ Error al ejecutar el procedimiento con OUT: {err}")
        conexion.rollback()
        return None if cantidad_out == 1 else [None] * cantidad_out
    finally:
        cursor.close()
        conexion.close()
