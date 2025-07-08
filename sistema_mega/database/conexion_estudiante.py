import mysql.connector

# ✅ Establecer conexión con el usuario estudiante
def obtener_conexion():
    return mysql.connector.connect(
        host="localhost",           # Cambia si usas AWS o un host remoto
        user="estudiante_user",
        password="estudiante_pass",
        database="academia_mega"
    )

# ✅ Ejecutar consultas SELECT (procedimientos sin OUT)
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

# ✅ Ejecutar procedimientos que no devuelven OUT
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

# ✅ Ejecutar procedimientos con OUT
def ejecutar_procedimiento_con_out(nombre_proc, parametros=None, cantidad_out=1):
    conexion = obtener_conexion()
    if not conexion:
        return None if cantidad_out == 1 else [None] * cantidad_out

    cursor = conexion.cursor()
    try:
        parametros = parametros or []
        parametros_completos = parametros + [None] * cantidad_out
        resultado = cursor.callproc(nombre_proc, parametros_completos)
        conexion.commit()
        outs = resultado[-cantidad_out:]
        return outs[0] if cantidad_out == 1 else outs
    except mysql.connector.Error as err:
        print(f"❌ Error en el procedimiento con OUT: {err}")
        conexion.rollback()
        return None if cantidad_out == 1 else [None] * cantidad_out
    finally:
        cursor.close()
        conexion.close()
