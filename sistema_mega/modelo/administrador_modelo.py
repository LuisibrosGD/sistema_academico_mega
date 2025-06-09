# Aqui ira la logica del administrador

from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion


# Sedes

def ver_sedes():
    query = "SELECT * FROM sedes" # de el año actual
    resultados = ejecutar_select(query)
    for resultado in resultados:
        print(f"ID: {resultado[0]}, Nombre: {resultado[1]}, Distrito: {resultado[2]}")


# 1. CREATE: insertar una nueva sede
def crear_sede(nombre, distrito):
    sql = """
    INSERT INTO sedes (nombre, distrito)
    VALUES (%s, %s)
    """
    datos = (nombre, distrito)
    ejecutar_modificacion(sql, datos)


# 2. UPDATE: modificar los datos de una sede existente
def actualizar_sede(id_sede, nombre, distrito):
    sql = """
    UPDATE sedes
       SET nombre = %s,
           distrito = %s
     WHERE id_sede = %s
    """
    datos = (nombre, distrito, id_sede)
    ejecutar_modificacion(sql, datos)

def buscar_sede(id_sede):

    sql = """
    SELECT * FROM sedes WHERE id_sede = %s
    """
    datos = (id_sede,)

    sede = ejecutar_select(sql, datos)

    resultados = ejecutar_select(sql, datos)

    if resultados and len(resultados) > 0:
        sede = resultados[0]  # toma la primera tupla de la lista
        print("Se encontró la sede")
        print(f"ID: {sede[0]}, Nombre: {sede[1]}, Distrito: {sede[2]}")
        return 1, sede
    else:
        print("No se encontró la sede")
        return 0, None


    #Ciclos Programados

def ver_cicloprogramado():
    query = "SELECT * FROM ciclos_programados" # de el año actual
    resultados = ejecutar_select(query)
    for resultado in resultados:
        print(f"ID: {resultado[0]}, Nombre: {resultado[1]}, Modalidad: {resultado[2]}, Costo: {resultado[3]}, Inicio: {resultado[4]}, Final: {resultado[5]}")

def crear_ciclo_programado(
    nombre_ciclo,
    modalidad,
    costo,
    fecha_inicio,  # formato "YYYY-MM-DD"
    fecha_fin  # formato "YYYY-MM-DD"
):
    sql = """
    INSERT INTO ciclos_programados(nombre_ciclo, modalidad, costo, fecha_inicio, fecha_fin) VALUES (%s, %s, %s, %s, %s)
    """
    datos = (
        nombre_ciclo,
        modalidad,
        costo,
        fecha_inicio,
        fecha_fin
    )
    ejecutar_modificacion(sql, datos)

    #CURSOSSSS

def crear_curso(nombre_curso):
    sql = """
    INSERT INTO cursos (nombre_curso)
    VALUES (%s)
    """
    datos = (nombre_curso,)
    ejecutar_modificacion(sql, datos)

def ver_cursos():
    query = "SELECT * FROM cursos"
    resultados = ejecutar_select(query)
    for resultado in resultados:
        print(f"ID: {resultado[0]}, Nombre: {resultado[1]}")

def buscar_curso(id_curso):
    sql = """
    SELECT * FROM cursos WHERE id_curso = %s
    """
    datos = (id_curso,)

    resultados = ejecutar_select(sql, datos)

    if resultados and len(resultados) > 0:
        curso = resultados[0]  # toma la primera tupla de la lista
        print("Se encontró el curso")
        print(f"ID: {curso[0]}, Nombre: {curso[1]}")
        return 1, curso
    else:
        print("No se encontró el curso")
        return 0, None

def actualizar_curso(id_curso, nombre_curso):
    sql = """
    UPDATE cursos
        SET nombre_curso = %s
    WHERE id_curso = %s
    """
    datos = (nombre_curso, id_curso)
    ejecutar_modificacion(sql, datos)

def crear_especialidad(nombre_especialidad):
    sql = """
    INSERT INTO especialidades (nombre_especialidad)
    VALUES (%s)
        """
    datos = (nombre_especialidad,)
    ejecutar_modificacion(sql, datos)

def ver_especialidades():
    query = "SELECT * FROM especialidades"
    resultados = ejecutar_select(query)
    for resultado in resultados:
        print(f"ID: {resultado[0]}, Nombre: {resultado[1]}")

def buscar_especialidad(id_especialidad):
    sql = """
    SELECT * FROM especialidades WHERE id_especialidad = %s
    """
    datos = (id_especialidad,)

    resultados = ejecutar_select(sql, datos)

    if resultados and len(resultados) > 0:
        especialidad = resultados[0]  # toma la primera tupla de la lista
        print("Se encontró la especialidad")
        print(f"ID: {especialidad[0]}, Nombre: {especialidad[1]}")
        return 1, especialidad
    else:
        print("No se encontró la especialidad")
        return 0, None

def actualizar_especialidad(id_especialidad, nombre_especialidad):
    sql = """
    UPDATE especialidades
    SET nombre_especialidad = %s
    WHERE id_especialidad = %s
    """
    datos = (nombre_especialidad, id_especialidad)
    ejecutar_modificacion(sql, datos)