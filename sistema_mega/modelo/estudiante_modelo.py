from sistema_mega.database.conexion_estudiante import *
"""
def ver_cicloprogramado():
    return ejecutar_select("CALL ver_ciclos_activos()")
"""
# --------------------------------------------

""" def ver_pagos(id_estudiante):
    query = "CALL sp_ver_pagos_estudiante(%s)"
    return ejecutar_select(query, (id_estudiante,))
"""
# -----------------------------------------------

def ver_notas(id_estudiante):
    query = "CALL ver_notas(%s)"
    return ejecutar_select(query, (id_estudiante,))


def ver_perfil(id_estudiante):
    query = "CALL ver_perfil_estudiante(%s)"
    return ejecutar_select(query, (id_estudiante,))

def cambiar_contrasenia(id_usuario, contrasenia_actual, nueva_contrasenia):
    return ejecutar_procedimiento_con_out(
        "cambiar_contrasenia",
        [id_usuario, contrasenia_actual, nueva_contrasenia],  # 👈 PASAR COMO LISTA
        1
    )

