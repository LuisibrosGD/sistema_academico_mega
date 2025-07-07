from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion, obtener_conexion, \
    ejecutar_procedimiento_con_out


# Logica para las interfaces para CRUD de Administrador
# =============ADMINISTRADOR============================
# En modeloUsuarios.py
def mostrar_administradores():
    query = (
        "SELECT a.id_administrador, a.nombre, a.ap_paterno, a.ap_materno, "
        "a.tipo_documento, a.nro_documento, u.estado, u.nombre_usuario, u.correo, u.contrasenia "
        "FROM administradores a "
        "JOIN usuarios u ON u.id_usuario = a.id_usuario;"
    )
    resultados = ejecutar_select(query)
    return resultados

def crear_administrador(nombre_usuario, correo, contrasenia, nombre, ap_paterno, ap_materno, tipo_documento, nro_documento):
    lista_parametros = [nombre_usuario, correo, contrasenia, nombre, ap_paterno, ap_materno, tipo_documento, nro_documento]
    resultados = ejecutar_procedimiento_con_out("sp_crear_administrador", lista_parametros, 1)
    return resultados

def editar_administrador(datos_parametros):
    resultados = ejecutar_procedimiento_con_out("sp_actualizar_administrador", datos_parametros, 1)
    return resultados

# ===========COLABORADOR====================
def mostrar_colaboradores():
    query = (
        "SELECT c.id_colaborador, c.nombre, c.ap_paterno, c.ap_materno, "
        "c.tipo_documento, c.nro_documento, u.estado, u.nombre_usuario, u.correo, u.contrasenia "
        "FROM colaboradores c "
        "JOIN usuarios u ON u.id_usuario = c.id_usuario;"
    )
    resultados = ejecutar_select(query)
    return resultados

def crear_colaborador(nombre_usuario, correo, contrasenia, nombre, ap_paterno, ap_materno, tipo_documento, nro_documento):
    lista_parametros = [nombre_usuario, correo, contrasenia, nombre, ap_paterno, ap_materno, tipo_documento, nro_documento]
    resultados = ejecutar_procedimiento_con_out("sp_crear_colaborador", lista_parametros, 1)
    return resultados

def editar_colaborador(id_colaborador, nombre_usuario, correo, contrasena, estado, nombres, ap_paterno, ap_materno, tipo_documento, nro_documento):
    datos_parametros = [
        id_colaborador,
        nombre_usuario,
        correo,
        contrasena,
        estado,
        nombres,
        ap_paterno,
        ap_materno,
        tipo_documento,
        nro_documento
    ]
    return ejecutar_procedimiento_con_out("sp_actualizar_colaborador", datos_parametros, 1)



# Logica para los cruds de profesor ======= POR CONSOLA

# 1. CREATE: insertar una nuevo profesor
def crear_profesor(
    nombre_usuario,
    correo,
    contrasena,
    nombre,
    ap_paterno,
    ap_materno,
    tipo_documento,
    nro_documento,
    estado = 1
):
    rol = "profesor"
    try:
        # 1) Insertar en usuarios
        sql_user = """
        INSERT INTO usuarios 
          (nombre_usuario, correo, contrasenia, estado,rol)
        VALUES (%s, %s, %s, %s,%s)
        """

        datos_user = (
            nombre_usuario,
            correo,
            contrasena,
            estado,
            rol
        )

        # Consulta agregada a la BD
        ejecutar_modificacion(sql_user, datos_user)

        # Obtener el id generado para usuarios
        id_usuario = ejecutar_select("SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s AND correo = %s AND contrasenia = %s AND rol = %s", (nombre_usuario,correo,contrasena, "profesor"))

        if id_usuario and len(id_usuario) > 0:
            id_usuario = id_usuario[0][0]  # ✅ AQUÍ: extraes el valor int
        else:
            print("❌ No se encontró el usuario recién insertado.")
            return

        # 2) Insertar en profesores
        sql_profe = """
        INSERT INTO profesores
          (nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        datos_profe = (
            nombre,
            ap_paterno,
            ap_materno,
            tipo_documento,
            nro_documento,
            id_usuario
        )
        ejecutar_modificacion(sql_profe, datos_profe)

    except Exception as e:
        print(f"❌ Error al crear profesor: {e}")

def editar_profesor(id_profesor, nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, nombre_usuario, correo, contrasenia):
    sql = """UPDATE usuarios u SET u.nombre_usuario = %s, u.correo = %s, u.contrasenia = %s 
        JOIN profesores p
        ON u.id_usuario = p.id_usuario 
    WHERE p.id_profesor = %s"""
    datos_profe = (nombre_usuario,contrasenia, correo, id_profesor)
    ejecutar_modificacion(sql, datos_profe)

    sql = """UPDATE profesores SET nombre = %s, ap_paterno = %s, ap_materno = %s, tipo_documento = %s, nro_documento = %s WHERE id_profe = %s"""
    datos_profe_1 = (nombre,ap_paterno,ap_materno,tipo_documento,nro_documento, id_profesor)
    ejecutar_modificacion(sql, datos_profe_1)



def ver_profesores():
    query = "SELECT * FROM profesores"
    resultados = ejecutar_select(query)
    for resultado in resultados:
        print(f"ID: {resultado[0]}, Nombre: {resultado[1]}, Apellido Pat.: {resultado[2]}, Apellido Mat.: {resultado[3]},Tipo Documento: {resultado[4]}, Numero Documento: {resultado[5]},ID usuario: {resultado[6]}")
        especialidades = obtener_especialidades(resultado[0])
        contador = 1
        print("Especialidades: ")
        for especialidad in especialidades:
            print(f"{contador}. {especialidad[0]}")
            contador = contador + 1
        print("-----------------------------------")
def activar_desactivar_cuenta_profesor(id_profesor, opcion_cuenta):
    resultado = ejecutar_select("SELECT id_usuario FROM profesores WHERE id_profesor = %s", (id_profesor,))

    if not resultado:
        print(f"❌ Error: No se encontró ningún profesor con ID {id_profesor}")
        return  # o puedes lanzar una excepción si prefieres

    id_usuario = resultado[0][0]
    print(f"id_usuario: {id_usuario} - probando opción")

    if opcion_cuenta == 0:
        print("🔒 Desactivando cuenta")
    elif opcion_cuenta == 1:
        print("✅ Activando cuenta")
    else:
        print("⚠️ Opción no existe")
        return

    query = "UPDATE usuarios SET estado = %s WHERE id_usuario = %s"
    datos = (opcion_cuenta, id_usuario)
    print(f"Ejecutando query con datos: {datos}")

    ejecutar_modificacion(query, datos)

def agregar_especialidad_profesor(id_profe, id_usuario):
    sql = """
        INSERT INTO profesores_especialidades VALUES (%s, %s)
    """
    datos_profe = (id_profe, id_usuario)
    ejecutar_modificacion(sql, datos_profe)

def obtener_especialidades(id_profe): # obtener_especialidades de un profesor
    sql = """
        SELECT e.nombre_especialidad FROM especialidades e
        JOIN profesores_especialidades pe
        ON pe.id_especialidad = e.id_especialidad
        JOIN profesores p
        ON pe.id_profesor = p.id_profesor
        where p.id_profesor = %s
    """
    datos_profe = (id_profe,)
    resultados = ejecutar_select(sql, datos_profe)
    return resultados

# Logica para los cruds de administrador ------------------------------------------------------------------





# Logica para los cruds de estudiantes ----------------------------------------------------------------------------------

def crear_estudiante(
    nombre_usuario,
    correo,
    contrasena,
    nombre,
    ap_paterno,
    ap_materno,
    tipo_documento,
    nro_documento,
    area_academica,
    estado = 1
):
    rol = "estudiante"
    try:
        # 1) Insertar en usuarios
        sql_user = """
        INSERT INTO usuarios 
          (nombre_usuario, correo, contrasenia, estado,rol)
        VALUES (%s, %s, %s, %s,%s)
        """

        datos_user = (
            nombre_usuario,
            correo,
            contrasena,
            estado,
            rol
        )

        # Consulta agregada a la BD
        ejecutar_modificacion(sql_user, datos_user)

        # Obtener el id generado para usuarios
        id_usuario = ejecutar_select("SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s AND correo = %s AND contrasenia = %s AND rol = %s", (nombre_usuario,correo,contrasena, "administrador"))

        if id_usuario and len(id_usuario) > 0:
            id_usuario = id_usuario[0][0]  # ✅ AQUÍ: extraes el valor int
        else:
            print("❌ No se encontró el usuario recién insertado.")
            return

        # 2) Insertar en estudiantes
        sql_admin = """
        INSERT INTO estudiantes
          (nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, area_academica, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        datos_estud = (
            nombre,
            ap_paterno,
            ap_materno,
            tipo_documento,
            nro_documento,
            area_academica,
            id_usuario
        )
        ejecutar_modificacion(sql_admin, datos_estud)

    except Exception as e:
        print(f"❌ Error al crear estudiante: {e}")

def editar_estudiante(id, nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, area_academica, nombre_usuario, correo, contrasenia):
    sql = """UPDATE usuarios u SET u.nombre_usuario = %s, u.correo = %s, u.contrasenia = %s 
    JOIN estudiantes e
    ON u.id_usuario = e.id_usuario 
    WHERE e.id_estudiante = %s"""
    datos_estud = (nombre_usuario,contrasenia, correo, id)
    ejecutar_modificacion(sql, datos_estud)

    sql = """UPDATE estudiantes SET nombre = %s, ap_paterno = %s, ap_materno = %s, tipo_documento = %s, nro_documento = %s, area_academica = %s WHERE id_estudiante = %s"""
    datos_estud_1 = (nombre,ap_paterno,ap_materno,tipo_documento,nro_documento,area_academica, id)
    ejecutar_modificacion(sql, datos_estud_1)

def ver_estudiantes():
    query = "SELECT * FROM vista_estudiantes;"
    resultados = ejecutar_select(query)
    for resultado in resultados:
        print(f"ID: {resultado[0]}, Nombre: {resultado[1]}, Apellido Pat.: {resultado[2]}, Apellido Mat.: {resultado[3]},Tipo Documento: {resultado[4]}, Numero Documento: {resultado[5]},Area academica: {resultado[6]},ID usuario: {resultado[7]}")

def ver_examenes():
    query = "SELECT ex.id_examen, ex.puntaje, ex.fecha_realizacion, CONCAT_WS(' ', es.nombre,es.ap_paterno, es.ap_materno) FROM examenes ex JOIN estudiantes es ON ex.id_estudiante = es.id_estudiante"

    resultados = ejecutar_select(query)
    for resultado in resultados:
        print(f"ID: {resultado[0]}, Puntaje: {resultado[1]}, fecha: {resultado[2]}, alumno: {resultado[3]}")
