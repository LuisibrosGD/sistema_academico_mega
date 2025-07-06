from sistema_mega.database.conexion import *

def ver_cicloprogramado():
    return ejecutar_select("CALL ver_ciclos_activos()")

# --------------------------------------------

def ver_pagos(id_estudiante):
    query = "CALL sp_ver_pagos_estudiante(%s)"
    return ejecutar_select(query, (id_estudiante,))

# -----------------------------------------------

def ver_notas(id_estudiante):
    query = "CALL ver_notas_estudiante(%s)"
    return ejecutar_select(query, (id_estudiante,))


def ver_perfil(id_estudiante):
    query = "CALL ver_perfil_estudiante(%s)"
    return ejecutar_select(query, (id_estudiante,))


def ejecutar_procedimiento(nombre_proc, parametros=None):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            if parametros is not None:
                marcadores = ', '.join(['%s'] * len(parametros))
                cursor.callproc(nombre_proc, parametros)
            else:
                cursor.callproc(nombre_proc)

            conexion.commit()

            if parametros is not None:
                resultados = []
                for i in range(len(parametros)):
                    cursor.execute(f"SELECT @_{nombre_proc}_{i}")
                    resultados.append(cursor.fetchone()[0])

                return resultados

        except mysql.connector.Error as err:
            print(f" Error al ejecutar el procedimiento con OUT: {err}")
            conexion.rollback()
            raise Exception(f"Error de base de datos: {err}")
        finally:
            cursor.close()
            conexion.close()