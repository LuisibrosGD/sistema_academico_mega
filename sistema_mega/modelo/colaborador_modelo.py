from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion

def registrar_asistencia(estado, id_profesor):
    query = """
    INSERT INTO asistencias (estado, id_profesor)
    VALUES (%s, %s)
    """
    datos = ( estado, id_profesor)
    ejecutar_modificacion(query, datos)
