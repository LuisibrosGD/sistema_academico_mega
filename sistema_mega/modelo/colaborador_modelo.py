from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion

def registrar_asistencia(estado, id_profesor):
    query = """
    INSERT INTO asistencias (estado, id_profesor)
    VALUES (%s, %s)
    """
    datos = ( estado, id_profesor)
    ejecutar_modificacion(query, datos)

def obtener_nombre_profesor(id_profesor):
    query = "SELECT nombre FROM profesores WHERE id_profesor = %s"
    resultado = ejecutar_select(query, (id_profesor,))
    if resultado:
        return resultado[0][0]
    return None

def obtener_fecha(id_profesor):
    query = "SELECT fecha FROM asistencias WHERE id_profesor = %s"
    resultado = ejecutar_select(query, (id_profesor,))
    if resultado:
        return resultado[0][0]
    return None

def registrar_calificacion(id_estudiante, puntaje, fecha_realizacion):
    query = """
     INSERT INTO examenes (puntaje, fecha_realizacion, id_estudiante)
     VALUES (%s, %s, %s)
     """
    datos = (puntaje, fecha_realizacion, id_estudiante)
    ejecutar_modificacion(query, datos)

def ver_calificaciones(id_estudiante):
    query = """
    SELECT examenes.id_examen,examenes.puntaje,examenes.fecha_realizacion,estudiantes.nombre,estudiantes.ap_paterno,estudiantes.ap_materno
    FROM examenes
    JOIN estudiantes ON examenes.id_estudiante = estudiantes.id_estudiante
    WHERE examenes.id_estudiante = %s
    """
    resultados = ejecutar_select(query, (id_estudiante,))
    if resultados:
        print("📋 Calificaciones del estudiante:")
        for id_examen, puntaje, fecha_realizacion, nombre, ap_paterno, ap_materno in resultados:
            nombre_completo = f"{nombre} {ap_paterno} {ap_materno}"
            print(f"🧑‍🎓 {nombre_completo} | Examen #{id_examen} - Nota: {puntaje} - Fecha: {fecha_realizacion}")
    else:
        query_nombre = """
              SELECT nombre, ap_paterno, ap_materno
              FROM estudiantes
              WHERE id_estudiante = %s
              """
        estudiante = ejecutar_select(query_nombre, (id_estudiante,))

        if estudiante:
            nombre, ap_paterno, ap_materno = estudiante[0]
            nombre_completo = f"{nombre} {ap_paterno} {ap_materno}"
            print(f"⚠️ No se encontraron calificaciones pipilinas para el estudiantesito: {nombre_completo}")