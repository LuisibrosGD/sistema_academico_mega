from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion

def obtener_profesores():
    """Devuelve una lista de profesores con sus especialidades"""
    query = """
        SELECT 
            p.id_profesor,
            CONCAT(p.nombre, ' ', p.ap_paterno, ' ', p.ap_materno) as nombre_completo,
            GROUP_CONCAT(e.nombre_especialidad SEPARATOR ', ') as especialidades
        FROM profesores p
        LEFT JOIN profesores_especialidades pe ON p.id_profesor = pe.id_profesor
        LEFT JOIN especialidades e ON pe.id_especialidad = e.id_especialidad
        GROUP BY p.id_profesor
        ORDER BY p.id_profesor
    """
    lista_profesores = ejecutar_select(query)
    return lista_profesores

def obtener_cursos():
    """Devuelve una lista de cursos"""
    query = "SELECT id_curso, nombre_curso FROM cursos ORDER BY id_curso"
    lista_cursos = ejecutar_select(query)
    return lista_cursos

def obtener_ciclos_programados():
    """Devuelve ciclos en curso con sus sedes"""
    query = """
        SELECT 
            cp.id_ciclo,
            GROUP_CONCAT(s.nombre SEPARATOR ', ') as sedes,
            cp.nombre_ciclo,
            'Grupo 1' as grupo
        FROM ciclos_programados cp
        LEFT JOIN sedes_ciclos sc ON cp.id_ciclo = sc.id_ciclo
        LEFT JOIN sedes s ON sc.id_sede = s.id_sede
        WHERE cp.estado = 'en curso'
        GROUP BY cp.id_ciclo, cp.nombre_ciclo
        ORDER BY cp.id_ciclo
    """
    ciclos_cursos_sedes = ejecutar_select(query)
    return ciclos_cursos_sedes

def asignar_profesor(id_profesor, id_curso, id_ciclo, hora_inicio, hora_fin, dia):
    """Asigna un profesor a un curso y ciclo"""
    query = """
        INSERT INTO ciclos_cursos (hora_inicio, hora_fin, dia, id_ciclo, id_curso, id_profesor)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    datos = (hora_inicio, hora_fin, dia,id_ciclo, id_curso, id_profesor)
    ejecutar_modificacion(query, datos)

def validar_id_profesor(id_profesor):
    query = "SELECT id_profesor FROM profesores WHERE id_profesor = %s"
    datos = ejecutar_select(query, (id_profesor,))

    return datos

def validar_id_curso(id_curso):
    datos = ejecutar_select("SELECT id_curso FROM cursos WHERE id_curso = %s", (id_curso,))
    return datos

def validar_id_ciclo(id_ciclo):
    datos = ejecutar_select("SELECT id_ciclo FROM ciclos_programados WHERE id_ciclo = %s", (id_ciclo,))

    return datos

