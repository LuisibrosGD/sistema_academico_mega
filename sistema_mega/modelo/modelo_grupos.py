from sistema_mega.database.conexion import *
from datetime import datetime
import pandas as pd
from datetime import datetime
import os
from tkinter import filedialog, messagebox


def generar_excel_estudiantes_grupo(id_grupo, area_filtro=None, nombre_archivo=None):
    """
    Generar archivo Excel con la información de estudiantes de un grupo
    Args:
        id_grupo (int): ID del grupo
        area_filtro (str, optional): Área académica para filtrar (None para todas)
        nombre_archivo (str, optional): Nombre del archivo, si no se especifica se genera automáticamente
    Returns:
        str: Ruta del archivo generado o None si hubo error
    """
    try:
        # Obtener información completa del grupo
        resumen_grupo = obtener_resumen_grupo_completo(id_grupo)

        if not resumen_grupo:
            print("❌ No se pudo obtener información del grupo")
            return None

        # Obtener estudiantes según el filtro
        if area_filtro and area_filtro != "Todas":
            estudiantes = obtener_estudiantes_por_grupo_y_area(id_grupo, area_filtro)
            sufijo_area = f"_{area_filtro}"
        else:
            estudiantes = obtener_estudiantes_por_grupo(id_grupo)
            sufijo_area = "_Todas_Areas"

        if not estudiantes:
            print("❌ No hay estudiantes para generar el Excel")
            return None

        # Preparar datos para el DataFrame
        datos_estudiantes = []
        for estudiante in estudiantes:
            fecha_inscripcion = estudiante[5].strftime("%d/%m/%Y") if estudiante[5] else "N/A"
            datos_estudiantes.append({
                'Nombre Completo': estudiante[1],
                'Área Académica': estudiante[2].upper() if estudiante[2] else "N/A",
                'Tipo Documento': estudiante[3] if estudiante[3] else "N/A",
                'Número Documento': estudiante[4] if estudiante[4] else "N/A",
                'Fecha Inscripción': fecha_inscripcion
            })

        # Crear DataFrame
        df = pd.DataFrame(datos_estudiantes)

        # Generar nombre del archivo si no se especifica
        if not nombre_archivo:
            nombre_grupo = resumen_grupo['grupo']['nombre_grupo'].replace(' ', '_')
            fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"Estudiantes_{nombre_grupo}{sufijo_area}_{fecha_actual}.xlsx"

        # Solicitar ubicación para guardar el archivo
        archivo_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialvalue=nombre_archivo,
            title="Guardar lista de estudiantes"
        )

        if not archivo_path:
            print("❌ Operación cancelada por el usuario")
            return None

        # Crear el archivo Excel con múltiples hojas
        with pd.ExcelWriter(archivo_path, engine='openpyxl') as writer:
            # Hoja 1: Información del grupo
            info_grupo = {
                'Campo': ['Nombre del Grupo', 'Docente Asignado', 'Ciclo', 'Capacidad Total',
                          'Estudiantes Inscritos', 'Espacios Disponibles', 'Porcentaje Ocupación',
                          'Filtro Aplicado', 'Fecha Generación'],
                'Valor': [
                    resumen_grupo['grupo']['nombre_grupo'],
                    resumen_grupo['grupo']['nombre_colaborador'],
                    resumen_grupo['grupo']['nombre_ciclo'],
                    resumen_grupo['grupo']['capacidad'],
                    len(estudiantes),
                    resumen_grupo['estadisticas']['espacios_disponibles'],
                    f"{resumen_grupo['estadisticas']['porcentaje_ocupacion']}%",
                    area_filtro if area_filtro and area_filtro != "Todas" else "Todas las áreas",
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                ]
            }

            df_info = pd.DataFrame(info_grupo)
            df_info.to_excel(writer, sheet_name='Información del Grupo', index=False)

            # Hoja 2: Lista de estudiantes
            df.to_excel(writer, sheet_name='Lista de Estudiantes', index=False)

            # Hoja 3: Estadísticas por área (si hay múltiples áreas)
            if not area_filtro or area_filtro == "Todas":
                stats_por_area = []
                for area, cantidad in resumen_grupo['estadisticas']['estudiantes_por_area'].items():
                    stats_por_area.append({
                        'Área Académica': area.upper() if area else "N/A",
                        'Cantidad de Estudiantes': cantidad
                    })

                if stats_por_area:
                    df_stats = pd.DataFrame(stats_por_area)
                    df_stats.to_excel(writer, sheet_name='Estadísticas por Área', index=False)

            # Hoja 4: Cursos del grupo
            cursos_grupo = resumen_grupo['cursos']
            if cursos_grupo:
                datos_cursos = []
                for curso in cursos_grupo:
                    datos_cursos.append({
                        'Curso': curso[1],
                        'Día': curso[2].capitalize(),
                        'Hora Inicio': curso[3],
                        'Hora Fin': curso[4],
                        'Profesor': curso[5]
                    })

                df_cursos = pd.DataFrame(datos_cursos)
                df_cursos.to_excel(writer, sheet_name='Cursos del Grupo', index=False)

        print(f"✅ Archivo Excel generado exitosamente: {archivo_path}")
        return archivo_path

    except Exception as e:
        print(f"❌ Error al generar archivo Excel: {e}")
        messagebox.showerror("Error", f"Error al generar archivo Excel: {str(e)}")
        return None


def generar_excel_estudiantes_filtrados(estudiantes_data, grupo_info, area_filtro=None):
    """
    Generar Excel con datos de estudiantes ya filtrados
    Args:
        estudiantes_data (list): Lista de estudiantes ya filtrados
        grupo_info (dict): Información del grupo
        area_filtro (str, optional): Filtro aplicado
    Returns:
        str: Ruta del archivo generado o None si hubo error
    """
    try:
        if not estudiantes_data:
            messagebox.showwarning("Advertencia", "No hay estudiantes para exportar")
            return None

        # Preparar datos para el DataFrame
        datos_estudiantes = []
        for estudiante in estudiantes_data:
            fecha_inscripcion = estudiante[5].strftime("%d/%m/%Y") if estudiante[5] else "N/A"
            datos_estudiantes.append({
                'Nombre Completo': estudiante[1],
                'Área Académica': estudiante[2].upper() if estudiante[2] else "N/A",
                'Tipo Documento': estudiante[3] if estudiante[3] else "N/A",
                'Número Documento': estudiante[4] if estudiante[4] else "N/A",
                'Fecha Inscripción': fecha_inscripcion
            })

        # Crear DataFrame
        df = pd.DataFrame(datos_estudiantes)

        # Generar nombre del archivo
        nombre_grupo = grupo_info['nombre_grupo'].replace(' ', '_')
        sufijo_area = f"_{area_filtro}" if area_filtro and area_filtro != "Todas" else "_Todas_Areas"
        fecha_actual = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"Estudiantes_{nombre_grupo}{sufijo_area}_{fecha_actual}.xlsx"

        # Solicitar ubicación para guardar
        archivo_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            initialvalue=nombre_archivo,
            title="Guardar lista de estudiantes"
        )

        if not archivo_path:
            return None

        # Guardar archivo
        with pd.ExcelWriter(archivo_path, engine='openpyxl') as writer:
            # Información del grupo
            info_grupo = {
                'Campo': ['Nombre del Grupo', 'Docente Asignado', 'Ciclo', 'Capacidad Total',
                          'Estudiantes Exportados', 'Filtro Aplicado', 'Fecha Generación'],
                'Valor': [
                    grupo_info['nombre_grupo'],
                    grupo_info['nombre_colaborador'],
                    grupo_info['nombre_ciclo'],
                    grupo_info['capacidad'],
                    len(estudiantes_data),
                    area_filtro if area_filtro and area_filtro != "Todas" else "Todas las áreas",
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                ]
            }

            df_info = pd.DataFrame(info_grupo)
            df_info.to_excel(writer, sheet_name='Información del Grupo', index=False)

            # Lista de estudiantes
            df.to_excel(writer, sheet_name='Lista de Estudiantes', index=False)

        print(f"✅ Archivo Excel generado exitosamente: {archivo_path}")
        return archivo_path

    except Exception as e:
        print(f"❌ Error al generar archivo Excel: {e}")
        messagebox.showerror("Error", f"Error al generar archivo Excel: {str(e)}")
        return None

def obtener_grupos_por_ciclo(id_ciclo):
    """
    Obtener todos los grupos de un ciclo específico
    Args:
        id_ciclo (int): ID del ciclo
    Returns:
        list: Lista de tuplas con información de grupos
    """
    try:
        # Query para obtener grupos de un ciclo específico
        query = """
            SELECT gpc.id_grupo, gpc.nombre_grupo, gpc.capacidad, 
                   gpc.id_colaborador, gpc.id_ciclo,
                   CONCAT(c.nombre, ' ', c.ap_paterno, ' ', c.ap_materno) as nombre_colaborador,
                   cp.nombre_ciclo
            FROM grupos_por_ciclo gpc
            INNER JOIN colaboradores c ON gpc.id_colaborador = c.id_colaborador
            INNER JOIN ciclos_programados cp ON gpc.id_ciclo = cp.id_ciclo
            WHERE gpc.id_ciclo = %s
            ORDER BY gpc.nombre_grupo
        """

        resultados = ejecutar_select(query, (id_ciclo,))
        return resultados if resultados else []

    except Exception as e:
        print(f" Error al obtener grupos por ciclo: {e}")
        raise e


def obtener_grupo_por_id(id_grupo):
    """
    Obtener información de un grupo específico
    Args:
        id_grupo (int): ID del grupo
    Returns:
        tuple: Información del grupo o None si no existe
    """
    try:
        query = """
            SELECT gpc.id_grupo, gpc.nombre_grupo, gpc.capacidad, 
                   gpc.id_colaborador, gpc.id_ciclo,
                   CONCAT(c.nombre, ' ', c.ap_paterno, ' ', c.ap_materno) as nombre_colaborador,
                   cp.nombre_ciclo
            FROM grupos_por_ciclo gpc
            INNER JOIN colaboradores c ON gpc.id_colaborador = c.id_colaborador
            INNER JOIN ciclos_programados cp ON gpc.id_ciclo = cp.id_ciclo
            WHERE gpc.id_grupo = %s
        """

        resultados = ejecutar_select(query, (id_grupo,))
        return resultados[0] if resultados else None

    except Exception as e:
        print(f"❌ Error al obtener grupo por ID: {e}")
        raise e


def validar_datos_grupo(nombre_grupo, capacidad, id_colaborador, id_ciclo):
    """
    Validar los datos de un grupo antes de guardar
    Args:
        nombre_grupo (str): Nombre del grupo
        capacidad (int): Capacidad del grupo
        id_colaborador (int): ID del colaborador
        id_ciclo (int): ID del ciclo
    Returns:
        tuple: (es_valido, lista_errores)
    """
    errores = []

    # Validar nombre del grupo
    if not nombre_grupo or not nombre_grupo.strip():
        errores.append("El nombre del grupo es obligatorio")
    elif len(nombre_grupo.strip()) < 2:
        errores.append("El nombre del grupo debe tener al menos 2 caracteres")
    elif len(nombre_grupo.strip()) > 45:
        errores.append("El nombre del grupo no puede exceder 45 caracteres")

    # Validar capacidad
    try:
        capacidad_int = int(capacidad)
        if capacidad_int <= 0:
            errores.append("La capacidad debe ser mayor a 0")
        elif capacidad_int > 999:
            errores.append("La capacidad no puede exceder 999 estudiantes")
    except (ValueError, TypeError):
        errores.append("La capacidad debe ser un número entero válido")

    # Validar ID del colaborador
    try:
        id_colaborador_int = int(id_colaborador)
        if id_colaborador_int <= 0:
            errores.append("Debe seleccionar un colaborador válido")
    except (ValueError, TypeError):
        errores.append("El ID del colaborador debe ser un número válido")

    # Validar ID del ciclo
    try:
        id_ciclo_int = int(id_ciclo)
        if id_ciclo_int <= 0:
            errores.append("Debe seleccionar un ciclo válido")
    except (ValueError, TypeError):
        errores.append("El ID del ciclo debe ser un número válido")

    return len(errores) == 0, errores


def agregar_grupo(nombre_grupo, capacidad, id_colaborador, id_ciclo):
    """
    Agregar un nuevo grupo por ciclo usando el stored procedure
    Args:
        nombre_grupo (str): Nombre del grupo
        capacidad (int): Capacidad del grupo
        id_colaborador (int): ID del colaborador
        id_ciclo (int): ID del ciclo
    Returns:
        bool: True si se creó exitosamente, False en caso contrario
    """
    try:
        # Validando datos antes de enviar
        es_valido, errores = validar_datos_grupo(
            nombre_grupo, capacidad, id_colaborador, id_ciclo
        )

        if not es_valido:
            print(f" Datos inválidos para crear grupo: {errores}")
            return False

        # Validando que el colaborador existe
        if not verificar_colaborador_existe(id_colaborador):
            print(f" El colaborador con ID {id_colaborador} no existe")
            return False

        # Validando que el ciclo existe
        if not verificar_ciclo_existe(id_ciclo):
            print(f" El ciclo con ID {id_ciclo} no existe")
            return False

        # Verificar que no exista un grupo con el mismo nombre en el mismo ciclo
        if verificar_nombre_grupo_duplicado(nombre_grupo, id_ciclo):
            print(f" Ya existe un grupo con el nombre '{nombre_grupo}' en este ciclo")
            return False

        # Preparar parámetros para el stored procedure
        parametros = [
            nombre_grupo.strip(),
            int(capacidad),
            int(id_colaborador),
            int(id_ciclo)
        ]

        # Ejecutar el stored procedure
        ejecutar_procedimiento('sp_insertar_grupo_por_ciclo', parametros)

        print(f" Grupo '{nombre_grupo}' creado exitosamente para el ciclo {id_ciclo}")
        return True

    except Exception as e:
        print(f"❌ Error al agregar grupo: {e}")
        return False


def editar_grupo(id_grupo, nombre_grupo, capacidad, id_colaborador, id_ciclo):
    """
    Editar un grupo por ciclo existente
    Args:
        id_grupo (int): ID del grupo a editar
        nombre_grupo (str): Nuevo nombre del grupo
        capacidad (int): Nueva capacidad del grupo
        id_colaborador (int): ID del colaborador
        id_ciclo (int): ID del ciclo
    Returns:
        bool: True si se editó exitosamente, False en caso contrario
    """
    try:
        # Validar que el grupo existe
        grupo_existente = obtener_grupo_por_id(id_grupo)
        if not grupo_existente:
            print(f"❌ El grupo con ID {id_grupo} no existe")
            return False

        # Validar datos antes de enviar
        es_valido, errores = validar_datos_grupo(
            nombre_grupo, capacidad, id_colaborador, id_ciclo
        )

        if not es_valido:
            print(f"❌ Datos inválidos para editar grupo: {errores}")
            return False

        # Validar que el colaborador existe
        if not verificar_colaborador_existe(id_colaborador):
            print(f"❌ El colaborador con ID {id_colaborador} no existe")
            return False

        # Validar que el ciclo existe
        if not verificar_ciclo_existe(id_ciclo):
            print(f"❌ El ciclo con ID {id_ciclo} no existe")
            return False

        # Verificar que no exista un grupo con el mismo nombre en el mismo ciclo (excluyendo el actual)
        if verificar_nombre_grupo_duplicado(nombre_grupo, id_ciclo, id_grupo):
            print(f"❌ Ya existe otro grupo con el nombre '{nombre_grupo}' en este ciclo")
            return False

        # Query para actualizar el grupo
        query = """
            UPDATE grupos_por_ciclo 
            SET nombre_grupo = %s, capacidad = %s, id_colaborador = %s, id_ciclo = %s
            WHERE id_grupo = %s
        """

        # Preparar parámetros
        parametros = [
            nombre_grupo.strip(),
            int(capacidad),
            int(id_colaborador),
            int(id_ciclo),
            int(id_grupo)
        ]

        # Ejecutar la actualización
        ejecutar_modificacion(query, parametros)

        print(f"✅ Grupo con ID {id_grupo} editado exitosamente")
        return True

    except Exception as e:
        print(f"❌ Error al editar grupo: {e}")
        return False


def obtener_todos_los_grupos():
    """
    Obtener todos los grupos para combobox de selección
    Returns:
        list: Lista de tuplas con (id_grupo, nombre_grupo, nombre_ciclo)
    """
    try:
        query = """
            SELECT gpc.id_grupo, gpc.nombre_grupo, cp.nombre_ciclo
            FROM grupos_por_ciclo gpc
            INNER JOIN ciclos_programados cp ON gpc.id_ciclo = cp.id_ciclo
            ORDER BY cp.nombre_ciclo, gpc.nombre_grupo
        """

        resultados = ejecutar_select(query, ())
        return resultados if resultados else []

    except Exception as e:
        print(f"❌ Error al obtener todos los grupos: {e}")
        raise e


def obtener_colaboradores_disponibles():
    """
    Obtener lista de colaboradores disponibles para asignar a grupos
    Returns:
        list: Lista de tuplas con (id_colaborador, nombre_completo)
    """
    try:
        query = """
            SELECT c.id_colaborador, CONCAT(c.nombre, ' ', c.ap_paterno, ' ', c.ap_materno) as nombre_completo
            FROM colaboradores c
            INNER JOIN usuarios u ON c.id_usuario = u.id_usuario
            WHERE u.estado = 1
            ORDER BY c.nombre, c.ap_paterno, c.ap_materno
        """

        resultados = ejecutar_select(query, ())
        return resultados if resultados else []

    except Exception as e:
        print(f"❌ Error al obtener colaboradores disponibles: {e}")
        raise e


def obtener_ciclos_disponibles():
    """
    Obtener lista de ciclos disponibles para crear grupos
    Returns:
        list: Lista de tuplas con (id_ciclo, nombre_ciclo)
    """
    try:
        # CORREGIDO: Cambiar estado 'en curso' por 'activo' según la estructura de la BD
        query = """
            SELECT id_ciclo, nombre_ciclo
            FROM ciclos_programados
            WHERE estado = 'en curso'
            ORDER BY nombre_ciclo
        """

        resultados = ejecutar_select(query, ())
        return resultados if resultados else []

    except Exception as e:
        print(f"❌ Error al obtener ciclos disponibles: {e}")
        raise e


def verificar_colaborador_existe(id_colaborador):
    """
    Verificar si un colaborador existe
    Args:
        id_colaborador (int): ID del colaborador
    Returns:
        bool: True si existe, False si no existe
    """
    try:
        query = "SELECT COUNT(*) FROM colaboradores WHERE id_colaborador = %s"
        resultado = ejecutar_select(query, (id_colaborador,))
        return resultado[0][0] > 0 if resultado else False

    except Exception as e:
        print(f"❌ Error al verificar colaborador: {e}")
        return False


def verificar_ciclo_existe(id_ciclo):
    """
    Verificar si un ciclo existe
    Args:
        id_ciclo (int): ID del ciclo
    Returns:
        bool: True si existe, False si no existe
    """
    try:
        query = "SELECT COUNT(*) FROM ciclos_programados WHERE id_ciclo = %s"
        resultado = ejecutar_select(query, (id_ciclo,))
        return resultado[0][0] > 0 if resultado else False

    except Exception as e:
        print(f" Error al verificar ciclo: {e}")
        return False


def verificar_nombre_grupo_duplicado(nombre_grupo, id_ciclo, id_grupo_excluir=None):
    """
    Verificar si ya existe un grupo con el mismo nombre en el mismo ciclo
    Args:
        nombre_grupo (str): Nombre del grupo
        id_ciclo (int): ID del ciclo
        id_grupo_excluir (int, optional): ID del grupo a excluir en la validación (para edición)
    Returns:
        bool: True si existe duplicado, False si no existe
    """
    try:
        if id_grupo_excluir:
            query = """
                SELECT COUNT(*) FROM grupos_por_ciclo
                WHERE UPPER(TRIM(nombre_grupo)) = UPPER(TRIM(%s))
                AND id_ciclo = %s
                AND id_grupo != %s
            """
            parametros = (nombre_grupo, id_ciclo, id_grupo_excluir)
        else:
            query = """
                SELECT COUNT(*) FROM grupos_por_ciclo
                WHERE UPPER(TRIM(nombre_grupo)) = UPPER(TRIM(%s))
                AND id_ciclo = %s
            """
            parametros = (nombre_grupo, id_ciclo)

        resultado = ejecutar_select(query, parametros)
        return resultado[0][0] > 0 if resultado else False

    except Exception as e:
        print(f" Error al verificar nombre duplicado: {e}")
        return False


def obtener_estadisticas_grupos_ciclo(id_ciclo):

    try:
        query = """
            SELECT 
                COUNT(*) as total_grupos,
                SUM(gpc.capacidad) as capacidad_total,
                AVG(gpc.capacidad) as capacidad_promedio,
                COUNT(DISTINCT gpc.id_colaborador) as colaboradores_asignados
            FROM grupos_por_ciclo gpc
            WHERE gpc.id_ciclo = %s
        """

        resultado = ejecutar_select(query, (id_ciclo,))

        if resultado:
            fila = resultado[0]
            return {
                'total_grupos': fila[0] or 0,
                'capacidad_total': fila[1] or 0,
                'capacidad_promedio': float(fila[2]) if fila[2] else 0.0,
                'colaboradores_asignados': fila[3] or 0
            }
        else:
            return {
                'total_grupos': 0,
                'capacidad_total': 0,
                'capacidad_promedio': 0.0,
                'colaboradores_asignados': 0
            }

    except Exception as e:
        print(f" Error al obtener estadísticas: {e}")
        return {
            'total_grupos': 0,
            'capacidad_total': 0,
            'capacidad_promedio': 0.0,
            'colaboradores_asignados': 0
        }


def obtener_grupos_con_disponibilidad(id_ciclo):


    try:
        query = """
            SELECT 
                gpc.id_grupo,
                gpc.nombre_grupo,
                gpc.capacidad,
                COALESCE(COUNT(i.id_inscripcion), 0) as estudiantes_inscritos,
                (gpc.capacidad - COALESCE(COUNT(i.id_inscripcion), 0)) as espacios_disponibles,
                CONCAT(c.nombre, ' ', c.ap_paterno, ' ', c.ap_materno) as nombre_colaborador
            FROM grupos_por_ciclo gpc
            LEFT JOIN inscripciones i ON gpc.id_grupo = i.id_grupo
            INNER JOIN colaboradores c ON gpc.id_colaborador = c.id_colaborador
            WHERE gpc.id_ciclo = %s
            GROUP BY gpc.id_grupo, gpc.nombre_grupo, gpc.capacidad, 
                     gpc.id_colaborador, c.nombre, c.ap_paterno, c.ap_materno
            ORDER BY gpc.nombre_grupo
        """

        resultados = ejecutar_select(query, (id_ciclo,))
        return resultados if resultados else []

    except Exception as e:
        print(f" Error al obtener grupos con disponibilidad: {e}")
        raise e




def obtener_colaboradores_activos():

    try:
        query = """
            SELECT c.id_colaborador, 
                   CONCAT(c.nombre, ' ', c.ap_paterno, ' ', c.ap_materno) as nombre_completo
            FROM colaboradores c
            INNER JOIN usuarios u ON c.id_usuario = u.id_usuario
            WHERE u.estado = 1
            ORDER BY c.nombre, c.ap_paterno, c.ap_materno
        """

        resultados = ejecutar_select(query, ())
        return resultados if resultados else []

    except Exception as e:
        print(f" Error al obtener colaboradores activos: {e}")
        raise e


def obtener_ciclos_activos():
    """

        Lista de tupla con (id_ciclo, nombre_ciclo, fecha_inicio, fecha_fin)
    """
    try:
        query = """
            SELECT id_ciclo, nombre_ciclo, fecha_inicio, fecha_fin
            FROM ciclos_programados
            WHERE estado = 'en curso'
            ORDER BY fecha_inicio DESC, nombre_ciclo
        """

        resultados = ejecutar_select(query, ())
        return resultados if resultados else []

    except Exception as e:
        print(f" Error al obtener ciclos activos: {e}")
        raise e


def verificar_integridad_grupo(id_grupo):
    """
    Chicos,aqui cree otra funcion para verificar la integridad de un grupo antes de que hayan
    modificaciones

    """
    try:
        # Obtener información del grupo
        grupo = obtener_grupo_por_id(id_grupo)
        if not grupo:
            return {'existe': False, 'mensaje': 'El grupo no existe'}

        # Aqui se va a poder contar inscripciones
        query_inscripciones = "SELECT COUNT(*) FROM inscripciones WHERE id_grupo = %s"
        resultado_inscripciones = ejecutar_select(query_inscripciones, (id_grupo,))
        inscripciones = resultado_inscripciones[0][0] if resultado_inscripciones else 0

        # Aqui se va a contar asignaciones de cursos
        query_cursos = "SELECT COUNT(*) FROM ciclos_cursos_grupos WHERE id_grupo = %s"
        resultado_cursos = ejecutar_select(query_cursos, (id_grupo,))
        cursos_asignados = resultado_cursos[0][0] if resultado_cursos else 0

        return {
            'existe': True,
            'inscripciones': inscripciones,
            'cursos_asignados': cursos_asignados,
            'puede_eliminar': inscripciones == 0 and cursos_asignados == 0,
            'puede_editar': True,  # Recuerden se va a poder editar siempre que exista
            'mensaje': 'Grupo válido'
        }

    except Exception as e:
        print(f" Error al verificar integridad del grupo: {e}")
        return {'existe': False, 'mensaje': f'Error: {e}'}


def obtener_cursos_por_grupo(id_grupo):
    """
    Obtener todos los cursos asignados a un grupo específico
    Args:
        id_grupo (int): ID del grupo
    Returns:
        list: Lista de tuplas con información de cursos del grupo
    """
    try:
        query = """
            SELECT 
                c.id_curso,
                c.nombre_curso,
                cc.dia,
                cc.hora_inicio,
                cc.hora_fin,
                CONCAT(p.nombre, ' ', p.ap_paterno, ' ', p.ap_materno) as nombre_profesor,
                p.id_profesor
            FROM ciclos_cursos_grupos ccg
            INNER JOIN ciclos_cursos cc ON ccg.id_cc = cc.id_cc
            INNER JOIN cursos c ON cc.id_curso = c.id_curso
            INNER JOIN profesores p ON cc.id_profesor = p.id_profesor
            WHERE ccg.id_grupo = %s
            ORDER BY cc.dia, cc.hora_inicio
        """

        resultados = ejecutar_select(query, (id_grupo,))
        return resultados if resultados else []

    except Exception as e:
        print(f" Error al obtener cursos del grupo: {e}")
        raise e


def obtener_estudiantes_por_grupo(id_grupo):

    try:
        query = """
            SELECT 
                e.id_estudiante,
                CONCAT(e.nombre, ' ', e.ap_paterno, ' ', e.ap_materno) as nombre_completo,
                e.area_academica,
                e.tipo_documento,
                e.nro_documento,
                i.fecha_inscripcion,
                i.id_inscripcion
            FROM inscripciones i
            INNER JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
            WHERE i.id_grupo = %s
            ORDER BY e.nombre, e.ap_paterno, e.ap_materno
        """

        resultados = ejecutar_select(query, (id_grupo,))
        return resultados if resultados else []

    except Exception as e:
        print(f"❌ Error al obtener estudiantes del grupo: {e}")
        raise e


def obtener_estudiantes_por_grupo_y_area(id_grupo, area_academica=None):

    try:
        if area_academica:
            query = """
                SELECT 
                    e.id_estudiante,
                    CONCAT(e.nombre, ' ', e.ap_paterno, ' ', e.ap_materno) as nombre_completo,
                    e.area_academica,
                    e.tipo_documento,
                    e.nro_documento,
                    i.fecha_inscripcion,
                    i.id_inscripcion
                FROM inscripciones i
                INNER JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
                WHERE i.id_grupo = %s AND e.area_academica = %s
                ORDER BY e.nombre, e.ap_paterno, e.ap_materno
            """
            parametros = (id_grupo, area_academica)
        else:
            # Si no se especifica área, devolver todos
            query = """
                SELECT 
                    e.id_estudiante,
                    CONCAT(e.nombre, ' ', e.ap_paterno, ' ', e.ap_materno) as nombre_completo,
                    e.area_academica,
                    e.tipo_documento,
                    e.nro_documento,
                    i.fecha_inscripcion,
                    i.id_inscripcion
                FROM inscripciones i
                INNER JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
                WHERE i.id_grupo = %s
                ORDER BY e.nombre, e.ap_paterno, e.ap_materno
            """
            parametros = (id_grupo,)

        resultados = ejecutar_select(query, parametros)
        return resultados if resultados else []

    except Exception as e:
        print(f" Error al obtener estudiantes por área: {e}")
        raise e


def obtener_areas_academicas_disponibles():
    """
    Obtener las áreas académicas disponibles para filtros
    Returns:
        list: Lista de tuplas con áreas académicas
    """
    try:
        query = """
            SELECT DISTINCT area_academica
            FROM estudiantes
            WHERE area_academica IS NOT NULL
            ORDER BY area_academica
        """

        resultados = ejecutar_select(query, ())
        return resultados if resultados else []

    except Exception as e:
        print(f" Error al obtener áreas académicas: {e}")
        raise e


def obtener_resumen_grupo_completo(id_grupo):
    """
    Obtener información completa del grupo con estadísticas
    Args:
        id_grupo (int): ID del grupo
    Returns:
        dict: Diccionario con toda la información del grupo
    """
    try:
        # Obtener información básica del grupo
        grupo = obtener_grupo_por_id(id_grupo)
        if not grupo:
            return None

        # Obtener cursos asignados
        cursos = obtener_cursos_por_grupo(id_grupo)

        # Obtener estudiantes
        estudiantes = obtener_estudiantes_por_grupo(id_grupo)

        # Contar estudiantes por área
        query_areas = """
            SELECT 
                e.area_academica,
                COUNT(*) as cantidad
            FROM inscripciones i
            INNER JOIN estudiantes e ON i.id_estudiante = e.id_estudiante
            WHERE i.id_grupo = %s
            GROUP BY e.area_academica
            ORDER BY e.area_academica
        """

        areas_count = ejecutar_select(query_areas, (id_grupo,))

        # Estructurar la información
        resumen = {
            'grupo': {
                'id_grupo': grupo[0],
                'nombre_grupo': grupo[1],
                'capacidad': grupo[2],
                'id_colaborador': grupo[3],
                'id_ciclo': grupo[4],
                'nombre_colaborador': grupo[5],
                'nombre_ciclo': grupo[6]
            },
            'cursos': cursos,
            'estudiantes': estudiantes,
            'estadisticas': {
                'total_cursos': len(cursos),
                'total_estudiantes': len(estudiantes),
                'espacios_disponibles': grupo[2] - len(estudiantes),
                'porcentaje_ocupacion': round((len(estudiantes) / grupo[2]) * 100, 2) if grupo[2] > 0 else 0,
                'estudiantes_por_area': {area[0]: area[1] for area in areas_count} if areas_count else {}
            }
        }

        return resumen

    except Exception as e:
        print(f" Error al obtener resumen completo del grupo: {e}")
        raise e


def obtener_horarios_grupo(id_grupo):
    """
    Obtener horarios organizados por día de la semana para un grupo
    Args:
        id_grupo (int): ID del grupo
    Returns:
        dict: Diccionario con horarios organizados por día
    """
    try:
        query = """
            SELECT 
                cc.dia,
                cc.hora_inicio,
                cc.hora_fin,
                c.nombre_curso,
                CONCAT(p.nombre, ' ', p.ap_paterno, ' ', p.ap_materno) as nombre_profesor
            FROM ciclos_cursos_grupos ccg
            INNER JOIN ciclos_cursos cc ON ccg.id_cc = cc.id_cc
            INNER JOIN cursos c ON cc.id_curso = c.id_curso
            INNER JOIN profesores p ON cc.id_profesor = p.id_profesor
            WHERE ccg.id_grupo = %s
            ORDER BY 
                CASE cc.dia
                    WHEN 'lunes' THEN 1
                    WHEN 'martes' THEN 2
                    WHEN 'miercoles' THEN 3
                    WHEN 'jueves' THEN 4
                    WHEN 'viernes' THEN 5
                    WHEN 'sabado' THEN 6
                    WHEN 'domingo' THEN 7
                    ELSE 8
                END,
                cc.hora_inicio
        """

        resultados = ejecutar_select(query, (id_grupo,))

        # Organizar por días
        horarios_por_dia = {}
        for resultado in resultados:
            dia = resultado[0]
            if dia not in horarios_por_dia:
                horarios_por_dia[dia] = []

            horarios_por_dia[dia].append({
                'hora_inicio': resultado[1],
                'hora_fin': resultado[2],
                'curso': resultado[3],
                'profesor': resultado[4]
            })

        return horarios_por_dia

    except Exception as e:
        print(f"❌ Error al obtener horarios del grupo: {e}")
        raise e


def verificar_grupo_tiene_datos(id_grupo):
    """
    Verificar si un grupo tiene cursos y estudiantes asignados
    Args:
        id_grupo (int): ID del grupo
    Returns:
        dict: Información sobre los datos del grupo
    """
    try:
        # Contar cursos
        query_cursos = """
            SELECT COUNT(*) 
            FROM ciclos_cursos_grupos 
            WHERE id_grupo = %s
        """
        resultado_cursos = ejecutar_select(query_cursos, (id_grupo,))
        total_cursos = resultado_cursos[0][0] if resultado_cursos else 0

        # Contar estudiantes
        query_estudiantes = """
            SELECT COUNT(*) 
            FROM inscripciones 
            WHERE id_grupo = %s
        """
        resultado_estudiantes = ejecutar_select(query_estudiantes, (id_grupo,))
        total_estudiantes = resultado_estudiantes[0][0] if resultado_estudiantes else 0

        return {
            'tiene_cursos': total_cursos > 0,
            'tiene_estudiantes': total_estudiantes > 0,
            'total_cursos': total_cursos,
            'total_estudiantes': total_estudiantes,
            'tiene_datos': total_cursos > 0 or total_estudiantes > 0
        }

    except Exception as e:
        print(f"❌ Error al verificar datos del grupo: {e}")
        return {
            'tiene_cursos': False,
            'tiene_estudiantes': False,
            'total_cursos': 0,
            'total_estudiantes': 0,
            'tiene_datos': False
        }