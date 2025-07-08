from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion, ejecutar_procedimiento_con_out


def obtener_sedes():
    query = "SELECT id_sede, nombre FROM sedes ORDER BY id_sede"
    return ejecutar_select(query)

def obtener_ciclos_por_sede(id_sede):
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
    query = """
        SELECT 
            g.id_grupo,
            g.nombre_grupo,
            (g.capacidad - (
                SELECT COUNT(*) FROM inscripciones i WHERE i.id_grupo = g.id_grupo
            )) AS vacantes
        FROM grupos_por_ciclo g
        INNER JOIN ciclos_programados cp ON g.id_ciclo = cp.id_ciclo
        WHERE cp.id_ciclo = %s
        ORDER BY g.id_grupo;
    """
    return ejecutar_select(query, (id_ciclo,))

def registrar_usuario(nombre_usuario, correo, contrasenia):
    try:
        query = """
            INSERT INTO usuarios (nombre_usuario, correo, contrasenia, estado, rol)
            VALUES (%s, %s, %s, 1, 'estudiante')
        """
        ejecutar_modificacion(query, (nombre_usuario, correo, contrasenia))

        query_id = "SELECT LAST_INSERT_ID()"
        resultado = ejecutar_select(query_id)
        return resultado[0][0]
    except Exception as e:
        print(f"❌ Error al registrar usuario: {e}")
        return None

def buscar_estudiante_por_documento(tipo_doc, nro_doc):
    query = """
        SELECT id_estudiante, id_usuario, area_academica
        FROM estudiantes
        WHERE tipo_documento = %s AND nro_documento = %s
    """
    resultado = ejecutar_select(query, (tipo_doc, nro_doc))
    return resultado[0] if resultado else None

def registrar_estudiante(nombre, ap_paterno, ap_materno, tipo_doc, nro_doc, area, id_usuario):
    existente = buscar_estudiante_por_documento(tipo_doc, nro_doc)

    if existente:
        id_estudiante = existente[0]
        area_actual = existente[2]

        if area_actual != area:
            query_update = "UPDATE estudiantes SET area_academica = %s WHERE id_estudiante = %s"
            ejecutar_modificacion(query_update, (area, id_estudiante))

        return id_estudiante, True  # ya existía

    query = """
        INSERT INTO estudiantes (nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, area_academica, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    ejecutar_modificacion(query, (nombre, ap_paterno, ap_materno, tipo_doc, nro_doc, area, id_usuario))

    query_id = "SELECT LAST_INSERT_ID()"
    resultado = ejecutar_select(query_id)
    return resultado[0][0], False  # nuevo estudiante

def registrar_inscripcion(id_estudiante, id_ciclo, id_grupo):
    try:
        query = """
            INSERT INTO inscripciones (id_ciclo, id_estudiante, id_grupo)
            VALUES (%s, %s, %s)
        """
        ejecutar_modificacion(query, (id_ciclo, id_estudiante, id_grupo))

        query_id = "SELECT LAST_INSERT_ID()"
        resultado = ejecutar_select(query_id)
        return resultado[0][0]
    except Exception as e:
        print(f"❌ Error al registrar inscripción: {e}")
        return None

def registrar_pago(id_inscripcion, monto):
    try:
        query = """
            INSERT INTO pagos (monto, id_inscripcion)
            VALUES (%s, %s)
        """
        ejecutar_modificacion(query, (monto, id_inscripcion))
    except Exception as e:
        print(f"❌ Error al registrar pago: {e}")

def registrar_estudiante_con_sp(nombre_usuario, correo, contrasenia, nombre, ap_paterno, ap_materno,
                                 tipo_documento, nro_documento, area_academica, id_grupo, id_ciclo, pago):
    parametros = [
        nombre_usuario,
        correo,
        contrasenia,
        nombre,
        ap_paterno,
        ap_materno,
        tipo_documento,
        nro_documento,
        area_academica,
        id_grupo,
        id_ciclo,
        pago
    ]

    mensaje = ejecutar_procedimiento_con_out("sp_registrar_estudiante", parametros, 1)
    return mensaje
