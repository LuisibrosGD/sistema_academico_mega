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


def obtener_asistencias(id_usuario, fecha_inicio=None, fecha_fin=None):
    """Obtiene las asistencias de los grupos del profesor"""
    query = """
    SELECT 
        cp.nombre_ciclo AS ciclo,
        cp.modalidad,
        gpc.nombre_grupo AS grupo,
        c.nombre_curso AS curso,
        DATE_FORMAT(a.fecha, '%Y-%m-%d %H:%i:%s') AS fecha,
        a.estado
    FROM 
        usuarios u
        JOIN profesores p ON u.id_usuario = p.id_usuario
        JOIN asistencias a ON p.id_profesor = a.id_profesor
        JOIN ciclos_cursos cc ON a.id_profesor = cc.id_profesor
        JOIN ciclos_programados cp ON cc.id_ciclo = cp.id_ciclo
        JOIN cursos c ON cc.id_curso = c.id_curso
        JOIN ciclos_cursos_grupos ccg ON cc.id_cc = ccg.id_cc
        JOIN grupos_por_ciclo gpc ON ccg.id_grupo = gpc.id_grupo
    WHERE 
        u.id_usuario = %s
    """
    params = [id_usuario]

    # Verificación más robusta de los parámetros de fecha
    if fecha_inicio and fecha_fin and fecha_inicio.strip() and fecha_fin.strip():
        query += " AND a.fecha BETWEEN %s AND %s"
        params.extend([fecha_inicio.strip(), fecha_fin.strip()])
    elif (fecha_inicio and fecha_inicio.strip()) or (fecha_fin and fecha_fin.strip()):
        # Si solo una fecha está completa, no aplicar filtro
        pass

    query += " ORDER BY a.fecha DESC"

    # Debug: Imprimir consulta y parámetros (opcional, para diagnóstico)
    print("Consulta SQL:", query)
    print("Parámetros:", params)

    return ejecutar_select(query, tuple(params)) or []
