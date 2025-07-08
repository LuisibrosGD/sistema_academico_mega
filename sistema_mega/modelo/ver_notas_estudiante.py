# sistema_mega/modelo/modelo_notas_estudiantes.py
from sistema_mega.database.conexion import ejecutar_select

def obtener_sedes():
    query = "SELECT id_sede, nombre FROM sedes"
    resultados = ejecutar_select(query)
    return [{'id_sede': r[0], 'nombre': r[1]} for r in resultados] if resultados else []

def obtener_ciclos():
    query = "SELECT id_ciclo, nombre_ciclo FROM ciclos_programados"
    resultados = ejecutar_select(query)
    return [{'id_ciclo': r[0], 'nombre_ciclo': r[1]} for r in resultados] if resultados else []

def obtener_grupos():
    query = "SELECT id_grupo, nombre_grupo FROM grupos_por_ciclo"
    resultados = ejecutar_select(query)
    return [{'id_grupo': r[0], 'nombre_grupo': r[1]} for r in resultados] if resultados else []

def obtener_notas_filtradas(filtros):
    sql = """
        SELECT 
            s.nombre AS sede,
            cp.nombre_ciclo AS ciclo,
            g.nombre_grupo AS grupo,
            CONCAT(e.nombre, ' ', e.ap_paterno, ' ', e.ap_materno) AS nombre_completo,
            e.area_academica,
            ex.puntaje AS nota,
            ex.fecha_realizacion AS fecha
        FROM examenes ex
        JOIN estudiantes e ON ex.id_estudiante = e.id_estudiante
        JOIN inscripciones i ON i.id_estudiante = e.id_estudiante
        JOIN grupos_por_ciclo g ON g.id_grupo = i.id_grupo
        JOIN ciclos_programados cp ON cp.id_ciclo = i.id_ciclo
        JOIN sedes_ciclos sc ON sc.id_ciclo = cp.id_ciclo
        JOIN sedes s ON s.id_sede = sc.id_sede
        WHERE 1=1
    """

    valores = []

    if filtros['sede']:
        sql += " AND s.nombre = %s"
        valores.append(filtros['sede'])
    if filtros['ciclo']:
        sql += " AND cp.nombre_ciclo = %s"
        valores.append(filtros['ciclo'])
    if filtros['grupo']:
        sql += " AND g.nombre_grupo = %s"
        valores.append(filtros['grupo'])
    if filtros['area_academica']:
        sql += " AND e.area_academica = %s"
        valores.append(filtros['area_academica'])
    if filtros['fecha_inicio']:
        sql += " AND ex.fecha_realizacion >= %s"
        valores.append(filtros['fecha_inicio'])
    if filtros['fecha_fin']:
        sql += " AND ex.fecha_realizacion <= %s"
        valores.append(filtros['fecha_fin'])

    sql += " ORDER BY ex.puntaje DESC"

    resultados = ejecutar_select(sql, tuple(valores))

    if resultados:
        return [{
            'sede': r[0],
            'ciclo': r[1],
            'grupo': r[2],
            'nombre_completo': r[3],
            'area_academica': r[4],
            'nota': float(r[5]),
            'fecha': str(r[6])
        } for r in resultados]
    return []
