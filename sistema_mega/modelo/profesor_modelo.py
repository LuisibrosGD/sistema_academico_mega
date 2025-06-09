from sistema_mega.database.conexion import *

def ver_grupos_asignados():
    consulta = """
    SELECT 
        gpc.id_grupo,
        gpc.nombre_grupo,
        CONCAT(p.nombre, ' ', p.ap_paterno, ' ', p.ap_materno) AS profesor,
        c.nombre_curso,
        cc.dia,
        cc.hora_inicio,
        cc.hora_fin
    FROM grupos_por_ciclo gpc
    JOIN profesores p ON gpc.id_profesor = p.id_profesor
    JOIN ciclos_cursos cc ON gpc.id_cc = cc.id_cc
    JOIN cursos c ON cc.id_curso = c.id_curso
    ORDER BY gpc.id_grupo;
    """

    resultados = ejecutar_select(consulta)

    if not resultados:
        print("No hay grupos asignados.")
        return

    print("Grupos asignados:")
    for grupo in resultados:
        id_grupo = grupo[0]
        nombre_grupo = grupo[1]
        nombre_profesor = grupo[2]
        nombre_curso = grupo[3]
        dia = grupo[4]
        hora_inicio = grupo[5]
        hora_fin = grupo[6]

        print(f"Grupo {nombre_grupo} | Profesor: {nombre_profesor} | Curso: {nombre_curso} | Día: {dia} | {hora_inicio} - {hora_fin}")

def ver_asistencias(id_profesor):
    consulta = f"""
    SELECT 
        ap.id_asistencia,
        CONCAT(p.nombre, ' ', p.ap_paterno, ' ', p.ap_materno) AS nombre_profesor,
        ap.fecha,
        ap.estado
    FROM asistencias ap
    JOIN profesores p ON ap.id_profesor = p.id_profesor
    WHERE p.id_profesor = {id_profesor}
    ORDER BY ap.fecha DESC;
    """

    resultados = ejecutar_select(consulta)

    if not resultados:
        print(f"No hay asistencias registradas para el profesor con ID {id_profesor}.")
        return

    print(f"Asistencias del profesor con ID {id_profesor}:")
    for fila in resultados:
        id_asistencia = fila[0]
        nombre_profesor = fila[1]
        fecha = fila[2]
        estado = fila[3]

        print(f"Asistencia #{id_asistencia} | Profesor: {nombre_profesor} | Fecha: {fecha} | Estado: {estado}")
