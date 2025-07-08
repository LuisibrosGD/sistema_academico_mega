from sistema_mega.database.conexion import ejecutar_procedimiento, ejecutar_select, ejecutar_modificacion
from datetime import datetime



"""Modelo para manejar operaciones relacionadas con ciclos"""


def obtener_ciclos_por_sede(id_sede):
    """
    Obtener todos los ciclos programados para una sede específica (solo los que están en curso)
    Args:
        id_sede (int): ID de la sede
    Returns:
        list: Lista de tuplas con información de ciclos
    """
    try:
        # Query para obtener ciclos de una sede específica - SOLO EN CURSO
        query = """
            SELECT cp.id_ciclo, cp.nombre_ciclo, cp.modalidad, cp.costo, 
                   cp.fecha_inicio, cp.fecha_fin, cp.estado
            FROM ciclos_programados cp
            INNER JOIN sedes_ciclos sc ON cp.id_ciclo = sc.id_ciclo
            WHERE sc.id_sede = %s AND cp.estado = 'en curso'
            ORDER BY cp.fecha_inicio DESC
        """

        resultados = ejecutar_select(query, (id_sede,))
        return resultados if resultados else []

    except Exception as e:
        print(f"❌ Error al obtener ciclos por sede: {e}")
        raise e

def obtener_ciclo_por_id(id_ciclo):
    """
    Obtener información de un ciclo específico
    Args:
        id_ciclo (int): ID del ciclo
    Returns:
        tuple: Información del ciclo o None si no existe
    """
    try:
        query = """
            SELECT id_ciclo, nombre_ciclo, modalidad, costo, fecha_inicio, fecha_fin, estado
            FROM ciclos_programados
            WHERE id_ciclo = %s
        """

        resultados = ejecutar_select(query, (id_ciclo,))
        return resultados[0] if resultados else None

    except Exception as e:
        print(f"❌ Error al obtener ciclo por ID: {e}")
        raise e

def obtener_todos_los_ciclos():
    """
    Obtener todos los ciclos programados para el combobox de selección (solo los que están en curso)
    Returns:
        list: Lista de tuplas con (id_ciclo, nombre_ciclo)
    """
    try:
        query = """
            SELECT id_ciclo, nombre_ciclo
            FROM ciclos_programados
            WHERE estado = 'en curso'
            ORDER BY nombre_ciclo
        """

        resultados = ejecutar_select(query, ())
        return resultados if resultados else []

    except Exception as e:
        print(f"❌ Error al obtener todos los ciclos: {e}")
        raise e

def validar_datos_ciclo(nombre, modalidad, costo, fecha_inicio, fecha_fin):
    """
    Validar los datos de un ciclo antes de guardar
    Args:
        nombre (str): Nombre del ciclo
        modalidad (str): Modalidad del ciclo
        costo (float): Costo del ciclo
        fecha_inicio (str): Fecha de inicio en formato YYYY-MM-DD
        fecha_fin (str): Fecha de fin en formato YYYY-MM-DD
    Returns:
        tuple: (es_valido, lista_errores)
    """
    errores = []

    # Validar nombre
    if not nombre or not nombre.strip():
        errores.append("El nombre del ciclo es obligatorio")
    elif len(nombre.strip()) < 3:
        errores.append("El nombre del ciclo debe tener al menos 3 caracteres")
    elif len(nombre.strip()) > 100:
        errores.append("El nombre del ciclo no puede exceder 100 caracteres")

    # Validar modalidad
    modalidades_validas = ['Presencial', 'Virtual', 'Híbrida']
    if not modalidad or modalidad not in modalidades_validas:
        errores.append(f"La modalidad debe ser una de: {', '.join(modalidades_validas)}")

    # Validar costo
    try:
        costo_float = float(costo)
        if costo_float <= 0:
            errores.append("El costo debe ser mayor a 0")
        elif costo_float > 99999999.99:
            errores.append("El costo no puede exceder 99,999,999.99")
    except (ValueError, TypeError):
        errores.append("El costo debe ser un número válido")

    # Validar fechas
    try:
        fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
        fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
        fecha_actual = datetime.now().date()

        # Para edición, permitir fechas pasadas si ya están en el pasado
        # pero validar que la fecha de fin sea posterior a la de inicio
        if fecha_fin_obj <= fecha_inicio_obj:
            errores.append("La fecha de fin debe ser posterior a la fecha de inicio")

        # Validar que el ciclo no sea demasiado corto (mínimo 1 día)
        diferencia_dias = (fecha_fin_obj - fecha_inicio_obj).days
        if diferencia_dias < 1:
            errores.append("El ciclo debe tener una duración mínima de 1 día")

    except ValueError:
        errores.append("Las fechas deben estar en formato válido (YYYY-MM-DD)")

    return len(errores) == 0, errores

def agregar_ciclo(id_sede, nombre, modalidad, costo, fecha_inicio, fecha_fin):
    """
    Agregar un nuevo ciclo programado usando el stored procedure
    Args:
        id_sede (int): ID de la sede
        nombre (str): Nombre del ciclo
        modalidad (str): Modalidad del ciclo
        costo (float): Costo del ciclo
        fecha_inicio (str): Fecha de inicio en formato YYYY-MM-DD
        fecha_fin (str): Fecha de fin en formato YYYY-MM-DD
    Returns:
        bool: True si se creó exitosamente, False en caso contrario
    """
    try:
        # Validar datos antes de enviar
        es_valido, errores = validar_datos_ciclo(
            nombre, modalidad, costo, fecha_inicio, fecha_fin
        )

        if not es_valido:
            print(f"❌ Datos inválidos para crear ciclo: {errores}")
            return False

        # Validar que la sede existe
        if not verificar_sede_existe(id_sede):
            print(f"❌ La sede con ID {id_sede} no existe")
            return False

        # Preparar parámetros para el stored procedure
        parametros = [
            nombre.strip(),
            modalidad,
            float(costo),
            fecha_inicio,
            fecha_fin,
            int(id_sede)
        ]

        # Ejecutar el stored procedure
        ejecutar_procedimiento('sp_crear_ciclo_programado', parametros)

        print(f"✅ Ciclo '{nombre}' creado exitosamente para la sede {id_sede}")
        return True

    except Exception as e:
        print(f"❌ Error al agregar ciclo: {e}")
        return False

def editar_ciclo(id_ciclo, nombre, modalidad, costo, fecha_inicio, fecha_fin):
    """
    Editar un ciclo programado existente
    Args:
        id_ciclo (int): ID del ciclo a editar
        nombre (str): Nuevo nombre del ciclo
        modalidad (str): Nueva modalidad del ciclo
        costo (float): Nuevo costo del ciclo
        fecha_inicio (str): Nueva fecha de inicio en formato YYYY-MM-DD
        fecha_fin (str): Nueva fecha de fin en formato YYYY-MM-DD
    Returns:
        bool: True si se editó exitosamente, False en caso contrario
    """
    try:
        # Validar que el ciclo existe
        ciclo_existente = obtener_ciclo_por_id(id_ciclo)
        if not ciclo_existente:
            print(f"❌ El ciclo con ID {id_ciclo} no existe")
            return False

        # Validar datos antes de enviar
        es_valido, errores = validar_datos_ciclo(
            nombre, modalidad, costo, fecha_inicio, fecha_fin
        )

        if not es_valido:
            print(f"❌ Datos inválidos para editar ciclo: {errores}")
            return False

        # Query para actualizar el ciclo
        query = """
            UPDATE ciclos_programados 
            SET nombre_ciclo = %s, modalidad = %s, costo = %s, 
                fecha_inicio = %s, fecha_fin = %s
            WHERE id_ciclo = %s
        """

        # Preparar parámetros
        parametros = [
            nombre.strip(),
            modalidad,
            float(costo),
            fecha_inicio,
            fecha_fin,
            int(id_ciclo)
        ]

        # Ejecutar la actualización
        ejecutar_modificacion('UPDATE ciclos_programados SET nombre_ciclo = %s, modalidad = %s, costo = %s, fecha_inicio = %s, fecha_fin = %s WHERE id_ciclo = %s', parametros)

        print(f"✅ Ciclo con ID {id_ciclo} editado exitosamente")
        return True

    except Exception as e:
        print(f"❌ Error al editar ciclo: {e}")
        return False

def obtener_todos_los_ciclos():
    """
    Obtener todos los ciclos programados para el combobox de selección
    Returns:
        list: Lista de tuplas con (id_ciclo, nombre_ciclo)
    """
    try:
        query = """
            SELECT id_ciclo, nombre_ciclo
            FROM ciclos_programados
            ORDER BY nombre_ciclo
        """

        resultados = ejecutar_select(query, ())
        return resultados if resultados else []

    except Exception as e:
        print(f"❌ Error al obtener todos los ciclos: {e}")
        raise e

def verificar_sede_existe(id_sede):
    """
    Verificar si una sede existe
    Args:
        id_sede (int): ID de la sede
    Returns:
        bool: True si existe, False si no existe
    """
    try:
        query = "SELECT COUNT(*) FROM sedes WHERE id_sede = %s"
        resultado = ejecutar_select(query, (id_sede,))
        return resultado[0][0] > 0 if resultado else False

    except Exception as e:
        print(f"❌ Error al verificar sede: {e}")
        return False

def verificar_nombre_ciclo_duplicado(nombre, id_sede, id_ciclo_excluir=None):
    """
    Verificar si ya existe un ciclo con el mismo nombre en la misma sede (solo entre los ciclos en curso)
    Args:
        nombre (str): Nombre del ciclo
        id_sede (int): ID de la sede
        id_ciclo_excluir (int, optional): ID del ciclo a excluir en la validación (para edición)
    Returns:
        bool: True si existe duplicado, False si no existe
    """
    try:
        if id_ciclo_excluir:
            query = """
                SELECT COUNT(*) FROM ciclos_programados cp
                INNER JOIN sedes_ciclos sc ON cp.id_ciclo = sc.id_ciclo
                WHERE UPPER(TRIM(cp.nombre_ciclo)) = UPPER(TRIM(%s))
                AND sc.id_sede = %s
                AND cp.id_ciclo != %s
                AND cp.estado = 'en curso'
            """
            parametros = (nombre, id_sede, id_ciclo_excluir)
        else:
            query = """
                SELECT COUNT(*) FROM ciclos_programados cp
                INNER JOIN sedes_ciclos sc ON cp.id_ciclo = sc.id_ciclo
                WHERE UPPER(TRIM(cp.nombre_ciclo)) = UPPER(TRIM(%s))
                AND sc.id_sede = %s
                AND cp.estado = 'en curso'
            """
            parametros = (nombre, id_sede)

        resultado = ejecutar_select(query, parametros)
        return resultado[0][0] > 0 if resultado else False

    except Exception as e:
        print(f"❌ Error al verificar nombre duplicado: {e}")
        return False


def obtener_estadisticas_ciclos_sede(id_sede):
    """
    Obtener estadísticas de ciclos para una sede (solo considerando los en curso)
    Args:
        id_sede (int): ID de la sede
    Returns:
        dict: Diccionario con estadísticas
    """
    try:
        query = """
            SELECT 
                COUNT(*) as total_ciclos,
                SUM(CASE WHEN cp.estado = 'en curso' THEN 1 ELSE 0 END) as ciclos_activos,
                AVG(cp.costo) as costo_promedio
            FROM ciclos_programados cp
            INNER JOIN sedes_ciclos sc ON cp.id_ciclo = sc.id_ciclo
            WHERE sc.id_sede = %s AND cp.estado = 'en curso'
        """

        resultado = ejecutar_select(query, (id_sede,))

        if resultado:
            fila = resultado[0]
            return {
                'total_ciclos': fila[0] or 0,
                'ciclos_activos': fila[1] or 0,
                'costo_promedio': float(fila[2]) if fila[2] else 0.0
            }
        else:
            return {
                'total_ciclos': 0,
                'ciclos_activos': 0,
                'costo_promedio': 0.0
            }

    except Exception as e:
        print(f"❌ Error al obtener estadísticas: {e}")
        return {
            'total_ciclos': 0,
            'ciclos_activos': 0,
            'costo_promedio': 0.0
        }


def obtener_modalidades_disponibles():
    """
    Obtener las modalidades disponibles para los ciclos
    Returns:
        list: Lista de modalidades
    """
    return ['Presencial', 'Virtual', 'Híbrida']

def formatear_fecha_para_display(fecha):
    """
    Formatear fecha para mostrar en la interfaz
    Args:
        fecha (date): Fecha a formatear
    Returns:
        str: Fecha formateada
    """
    try:
        if isinstance(fecha, str):
            fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        else:
            fecha_obj = fecha

        return fecha_obj.strftime('%d/%m/%Y')

    except Exception as e:
        print(f"❌ Error al formatear fecha: {e}")
        return str(fecha)

def formatear_costo_para_display(costo):
    """
    Formatear costo para mostrar en la interfaz
    Args:
        costo (float): Costo a formatear
    Returns:
        str: Costo formateado
    """
    try:
        return f"S/. {float(costo):,.2f}"
    except Exception as e:
        print(f"❌ Error al formatear costo: {e}")
        return f"S/. {costo}"