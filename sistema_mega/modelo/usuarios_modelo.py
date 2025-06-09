from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion, obtener_conexion


# Logica para los cruds de profesor

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
    sql = """UPDATE usuarios SET nombre_usuario = %s, correo = %s, contrasenia = %s WHERE id_usuario = %s"""
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
        especialidades = mostrar_especialidades(resultado[0])
        contador = 1
        print("Especialidades: ")
        for especialidad in especialidades:
            print(f"{contador}. {especialidad[0]}")
            contador = contador + 1
        print("-----------------------------------")
def activar_desactivar_cuenta_profesor(id_profesor, opcion_cuenta):

    global query
    if opcion_cuenta == 0:
        query = "UPDATE usuarios SET estado = 0 WHERE id_usuario = %s"
    elif opcion_cuenta == 1:
        query = "UPDATE usuarios SET estado = 1 WHERE id_usuario = %s"
    else:
        print("Opcion no existe")

    datos = (id_profesor,)
    ejecutar_modificacion(query, datos)

def agregar_especialidad_profesor(id_profe, id_usuario):
    sql = """
        INSERT INTO profesores_especialidades VALUES (%s, %s)
    """
    datos_profe = (id_profe, id_usuario)
    ejecutar_modificacion(sql, datos_profe)

def mostrar_especialidades(id_profe):
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
# 1. CREATE: insertar una nuevo administrador
def crear_administrador(
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
    rol = "administrador"
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

        # 2) Insertar en administradores
        sql_admin = """
        INSERT INTO administradores
          (nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        datos_admin = (
            nombre,
            ap_paterno,
            ap_materno,
            tipo_documento,
            nro_documento,
            id_usuario
        )
        ejecutar_modificacion(sql_admin, datos_admin)

    except Exception as e:
        print(f"❌ Error al crear administrador: {e}")

def editar_administrador(id_admin, nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, nombre_usuario, correo, contrasenia):
    sql = """UPDATE usuarios SET nombre_usuario = %s, correo = %s, contrasenia = %s WHERE id_usuario = %s"""
    datos_admin = (nombre_usuario,contrasenia, correo, id_profesor)
    ejecutar_modificacion(sql, datos_admin)

    sql = """UPDATE administradores SET nombre = %s, ap_paterno = %s, ap_materno = %s, tipo_documento = %s, nro_documento = %s WHERE id_profe = %s"""
    datos_admin_1 = (nombre,ap_paterno,ap_materno,tipo_documento,nro_documento, id_profesor)
    ejecutar_modificacion(sql, datos_admin_1)

def ver_administradores():
    query = "SELECT * FROM administradores"
    resultados = ejecutar_select(query)
    for resultado in resultados:
        print(f"ID: {resultado[0]}, Nombre: {resultado[1]}, Apellido Pat.: {resultado[2]}, Apellido Mat.: {resultado[3]},Tipo Documento: {resultado[4]}, Numero Documento: {resultado[5]},ID usuario: {resultado[6]}")

# Logica para los cruds de colaborador ---------------------------------------------------------------

def crear_colaborador(
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
    rol = "colaborador"
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
        id_usuario = ejecutar_select("SELECT id_usuario FROM usuarios WHERE nombre_usuario = %s AND correo = %s AND contrasenia = %s AND rol = %s", (nombre_usuario,correo,contrasena, "colaborador"))

        if id_usuario and len(id_usuario) > 0:
            id_usuario = id_usuario[0][0]  # ✅ AQUÍ: extraes el valor int
        else:
            print("❌ No se encontró el usuario recién insertado.")
            return

        # 2) Insertar en colaboradores
        sql_profe = """
        INSERT INTO colaboradores
          (nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, id_usuario)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        datos_colab = (
            nombre,
            ap_paterno,
            ap_materno,
            tipo_documento,
            nro_documento,
            id_usuario
        )
        ejecutar_modificacion(sql_profe, datos_colab)

    except Exception as e:
        print(f"❌ Error al crear colaborador: {e}")

# Logica para los cruds de estudiantes ----------------------------------------------------------------------------------
