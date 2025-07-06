from sistema_mega.database.conexion import ejecutar_select

def verificar_cuenta(nombre,contrasenia):
    query = "SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasenia = %s AND estado = 1"
    valores = (nombre,contrasenia)
    resultado = ejecutar_select(query, valores)

    if not resultado:
        print("❌ Usuario no encontrado o credenciales incorrectas")
        return None

    # Tomamos la primera fila
    fila = resultado[0]
    id, nombre, correo, contra, fecha_cre, estado, rol = fila

    if estado == 0:
        print("El usuario ha sido desactivado del sistema")
        return None
    else:
        return fila

