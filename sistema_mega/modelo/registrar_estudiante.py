from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion


def obtener_sedes():
    """Devuelve la lista de sedes disponibles"""
    query = "SELECT id_sede, nombre FROM sedes ORDER BY id_sede"
    return ejecutar_select(query)


def obtener_ciclos_por_sede(id_sede):
    """Devuelve ciclos en curso disponibles para una sede específica"""
    query = """
        SELECT 
            cp.id_ciclo,
            CONCAT(cp.nombre_ciclo, ' - S/', cp.costo) AS nombre_ciclo
        FROM ciclos_programados cp
        INNER JOIN sedes_ciclos sc ON cp.id_ciclo = sc.id_ciclo
        WHERE cp.estado = 'en curso' AND sc.id_sede = %s
        ORDER BY cp.id_ciclo
    """
    return ejecutar_select(query, (id_sede,))


def obtener_grupos_por_ciclo(id_ciclo):
    """Devuelve grupos disponibles para un ciclo, junto con vacantes"""
    query = """
        SELECT 
            g.id_grupo,
            g.nombre_grupo,
            (g.capacidad - (
                SELECT COUNT(*) FROM inscripciones i WHERE i.id_grupo = g.id_grupo
            )) AS vacantes
        FROM grupos_por_ciclo g
        INNER JOIN ciclos_cursos cc ON g.id_cc = cc.id_cc
        WHERE cc.id_ciclo = %s
        ORDER BY g.id_grupo
    """
    return ejecutar_select(query, (id_ciclo,))


def registrar_usuario(nombre_usuario, correo, contrasenia):
    """Registra un nuevo usuario de tipo estudiante y retorna su ID"""
    query = """
        INSERT INTO usuarios (nombre_usuario, correo, contrasenia, estado, rol)
        VALUES (%s, %s, %s, 1, 'estudiante')
    """
    ejecutar_modificacion(query, (nombre_usuario, correo, contrasenia))

    query_id = "SELECT LAST_INSERT_ID() as id_usuario"
    resultado = ejecutar_select(query_id)
    return resultado[0]['id_usuario']


def registrar_estudiante(nombre, ap_paterno, ap_materno, tipo_doc, nro_doc, area, id_usuario):
    """Registra los datos personales del estudiante y retorna su ID"""
    query = """
        INSERT INTO estudiantes (nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, area_academica, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    ejecutar_modificacion(query, (nombre, ap_paterno, ap_materno, tipo_doc, nro_doc, area, id_usuario))

    query_id = "SELECT LAST_INSERT_ID() as id_estudiante"
    resultado = ejecutar_select(query_id)
    return resultado[0]['id_estudiante']


def registrar_inscripcion(id_estudiante, id_ciclo, id_grupo):
    """Registra la inscripción del estudiante a un grupo y ciclo"""
    query = """
        INSERT INTO inscripciones (id_ciclo, id_estudiante, id_grupo)
        VALUES (%s, %s, %s)
    """
    ejecutar_modificacion(query, (id_ciclo, id_estudiante, id_grupo))

    query_id = "SELECT LAST_INSERT_ID() as id_inscripcion"
    resultado = ejecutar_select(query_id)
    return resultado[0]['id_inscripcion']


def registrar_pago(id_inscripcion, monto):
    """Registra el pago correspondiente a una inscripción"""
    query = """
        INSERT INTO pagos (monto, id_inscripcion)
        VALUES (%s, %s)
    """
    ejecutar_modificacion(query, (monto, id_inscripcion))
