from sistema_mega.database.conexion import ejecutar_select

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