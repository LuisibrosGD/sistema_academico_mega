from sistema_mega.database.conexion import *

# aqui creas la logica osea usas las funciones de la conexion.py
from sistema_mega.database.conexion import ejecutar_select


def obtener_grupos_asignados(id_usuario):
    """Obtiene los grupos asignados al profesor mediante su id_usuario"""
    query = """
    SELECT 
        cp.nombre_ciclo AS ciclo,
        cp.modalidad,
        c.nombre_curso AS curso,
        cc.dia,
        TIME_FORMAT(cc.hora_inicio, '%H:%i') AS hora_inicio,
        TIME_FORMAT(cc.hora_fin, '%H:%i') AS hora_fin,
        gpc.nombre_grupo AS grupo
    FROM 
        usuarios u
        JOIN profesores p ON u.id_usuario = p.id_usuario
        JOIN ciclos_cursos cc ON p.id_profesor = cc.id_profesor
        JOIN ciclos_programados cp ON cc.id_ciclo = cp.id_ciclo
        JOIN cursos c ON cc.id_curso = c.id_curso
        JOIN ciclos_cursos_grupos ccg ON cc.id_cc = ccg.id_cc
        JOIN grupos_por_ciclo gpc ON ccg.id_grupo = gpc.id_grupo
    WHERE 
        u.id_usuario = %s
    ORDER BY 
        cp.nombre_ciclo, gpc.nombre_grupo
    """
    return ejecutar_select(query, (id_usuario,))


def obtener_asistencias(id_usuario):
    """Obtiene las asistencias del profesor"""
    query = """
    SELECT 
        IFNULL(cp.nombre_ciclo, 'General') AS ciclo,
        IFNULL(cp.modalidad, 'No especificado') AS modalidad,
        IFNULL(gpc.nombre_grupo, 'No asignado') AS grupo,
        IFNULL(c.nombre_curso, 'General') AS curso,
        DATE_FORMAT(a.fecha, '%Y-%m-%d %H:%i:%s') AS fecha,
        a.estado
    FROM 
        usuarios u
        JOIN profesores p ON u.id_usuario = p.id_usuario
        JOIN asistencias a ON p.id_profesor = a.id_profesor
        LEFT JOIN ciclos_cursos cc ON p.id_profesor = cc.id_profesor
        LEFT JOIN ciclos_programados cp ON cc.id_ciclo = cp.id_ciclo
        LEFT JOIN cursos c ON cc.id_curso = c.id_curso
        LEFT JOIN ciclos_cursos_grupos ccg ON cc.id_cc = ccg.id_cc
        LEFT JOIN grupos_por_ciclo gpc ON ccg.id_grupo = gpc.id_grupo
    WHERE 
        u.id_usuario = 4
    ORDER BY 
        a.fecha DESC;
    """
    print("📥 Ejecutando consulta con ID:", id_usuario)
    return ejecutar_select(query, (id_usuario,))

