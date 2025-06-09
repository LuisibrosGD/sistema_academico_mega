


def ver_cicloprogramado():
    sql_select = ("SELECT nombre_ciclo, modalidad, costo, fecha_inicio, fecha_fin "
                  "FROM academia_mega.ciclos_programados "
                  "WHERE fecha_inicio < NOW() AND NOW() < fecha_fin")
    datos = ejecutar_select(sql_select)
    return datos

# --------------------------------------------

def ver_pagos(id_estudiante):
    sql_select = """
        SELECT c.nombre_ciclo, i.fecha_inscripcion, p.monto, p.fecha_pago FROM pagos p 
        JOIN inscripciones i
        ON p.id_inscripcion = i.id_inscripcion
        JOIN ciclos_programados c
        ON i.id_ciclo = c.id_ciclo
        WHERE i.id_estudiante = %s
    """
    dato = (id_estudiante,)
    return ejecutar_select(sql_select, dato)

# -----------------------------------------------

def ver_notas(id_estudiante):
    sql_select = """
        SELECT puntaje,fecha_realizacion FROM examenes WHERE id_estudiante = %s
    """
    dato = (id_estudiante,)
    return ejecutar_select(sql_select, dato)