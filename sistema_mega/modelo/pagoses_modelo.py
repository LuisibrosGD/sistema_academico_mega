from sistema_mega.database.conexion import *


def obtener_pagos_estudiante(id_usuario):
    """
    Obtiene todos los pagos realizados por un estudiante específico
    """
    query = """
    SELECT 
        cp.nombre_ciclo,
        cp.modalidad,
        p.monto,
        p.fecha_pago,
        cp.fecha_inicio,
        cp.fecha_fin,
        cp.estado as estado_ciclo
    FROM pagos p
    INNER JOIN inscripciones i ON p.id_inscripcion = i.id_inscripcion
    INNER JOIN ciclos_programados cp ON i.id_ciclo = cp.id_ciclo
    INNER JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
    WHERE e.id_usuario = %s
    ORDER BY p.fecha_pago DESC
    """

    try:
        resultados = ejecutar_select(query, (id_usuario,))
        return resultados if resultados else []
    except Exception as e:
        print(f"❌ Error al obtener pagos del estudiante: {e}")
        return []


def obtener_total_pagado_estudiante(id_usuario):
    """
    Obtiene el total de dinero pagado por un estudiante
    """
    query = """
    SELECT 
        COALESCE(SUM(p.monto), 0) as total_pagado
    FROM pagos p
    INNER JOIN inscripciones i ON p.id_inscripcion = i.id_inscripcion
    INNER JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
    WHERE e.id_usuario = %s
    """

    try:
        resultado = ejecutar_select(query, (id_usuario,))
        return resultado[0][0] if resultado else 0
    except Exception as e:
        print(f"❌ Error al obtener total pagado: {e}")
        return 0


def obtener_datos_estudiante(id_usuario):
    """
    Obtiene los datos básicos del estudiante
    """
    query = """
    SELECT 
        e.nombre,
        e.ap_paterno,
        e.ap_materno,
        e.nro_documento,
        e.area_academica
    FROM estudiantes e
    WHERE e.id_usuario = %s
    """

    try:
        resultado = ejecutar_select(query, (id_usuario,))
        return resultado[0] if resultado else None
    except Exception as e:
        print(f"❌ Error al obtener datos del estudiante: {e}")
        return None