from datetime import datetime
from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion


class FuncionesColaborador:
    @staticmethod
    def obtener_id_colaborador_por_usuario(id_usuario: int):
        """
        Devuelve el id_colaborador asociado al id_usuario.
        Retorna None si no existe.
        """
        try:
            q = "SELECT id_colaborador FROM colaboradores WHERE id_usuario = %s"
            r = ejecutar_select(q, (id_usuario,))
            return r[0][0] if r else None
        except Exception as e:
            print(f"Error al obtener id_colaborador: {e}")
            return None
    @staticmethod
    def obtener_profesores_por_colaborador(id_colaborador):
        """Obtener profesores, cursos y grupos asignados a un colaborador usando el stored procedure"""
        try:
            query = "CALL sp_profesores_por_colaborador(%s)"
            return ejecutar_select(query, (id_colaborador,))
        except Exception as e:
            print(f"Error al obtener profesores: {str(e)}")
            return []

    @staticmethod
    def registrar_asistencia(estado, id_profesor, fecha=None):
        """Registrar la asistencia de un profesor"""
        try:
            # Verificar que el profesor existe
            query_check = "SELECT id_profesor FROM profesores WHERE id_profesor = %s"
            profesor_existe = ejecutar_select(query_check, (id_profesor,))

            if not profesor_existe:
                return False, "El profesor no existe en la base de datos"

            if fecha:
                query = "INSERT INTO asistencias (estado, id_profesor, fecha) VALUES (%s, %s, %s)"
                datos = (estado, id_profesor, fecha)
            else:
                query = "INSERT INTO asistencias (estado, id_profesor) VALUES (%s, %s)"
                datos = (estado, id_profesor)

            ejecutar_modificacion(query, datos)
            return True, "Asistencia registrada exitosamente"
        except Exception as e:
            return False, f"Error al registrar asistencia: {str(e)}"

    @staticmethod
    def obtener_estudiantes():
        """Obtener lista de estudiantes con su nombre completo"""
        try:
            query = "SELECT id_estudiante, CONCAT(nombre, ' ', ap_paterno, ' ', ap_materno) FROM estudiantes"
            return ejecutar_select(query)
        except Exception as e:
            print(f"Error al obtener estudiantes: {str(e)}")
            return []

    @staticmethod
    def registrar_calificacion(id_estudiante, puntaje, fecha_realizacion):
        """Registrar una nueva calificación/examen para un estudiante"""
        try:
            query = "INSERT INTO examenes (puntaje, fecha_realizacion, id_estudiante) VALUES (%s, %s, %s)"
            datos = (puntaje, fecha_realizacion, id_estudiante)
            ejecutar_modificacion(query, datos)
            return True, "Calificación registrada exitosamente"
        except Exception as e:
            return False, f"Error al registrar calificación: {str(e)}"

    @staticmethod
    def obtener_notas_estudiantes(id_colaborador, filtro_area=None, fecha_ini=None, fecha_fin=None):
        """Obtener notas de estudiantes usando el nuevo stored procedure y aplicando filtros adicionales"""
        try:
            # Llamar al stored procedure con el ID del colaborador
            query = "CALL sp_reporte_estudiantes_por_colaborador(%s)"
            resultados = ejecutar_select(query, (id_colaborador,))

            if not resultados:
                return []

            # Aplicar filtros adicionales
            datos_filtrados = []

            for fila in resultados:
                # Estructura de fila: (sede, ciclo, estudiante, area, nota, fecha)

                # Filtro por área académica
                if filtro_area and filtro_area != "Todas":
                    if fila[3] != filtro_area:  # El área está en el índice 3
                        continue

                # Filtro por fechas
                fecha_examen = fila[5]  # La fecha está en el índice 5

                # Convertir fechas de filtro a objetos date si existen
                fecha_ini_dt = datetime.strptime(fecha_ini, "%Y-%m-%d").date() if fecha_ini else None
                fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date() if fecha_fin else None

                # Si la fecha del examen es string, convertirla a date
                if isinstance(fecha_examen, str):
                    fecha_examen = datetime.strptime(fecha_examen, "%Y-%m-%d").date()

                # Aplicar filtro de fecha inicial
                if fecha_ini_dt and fecha_examen < fecha_ini_dt:
                    continue

                # Aplicar filtro de fecha final
                if fecha_fin_dt and fecha_examen > fecha_fin_dt:
                    continue

                datos_filtrados.append(fila)

            return datos_filtrados
        except Exception as e:
            print(f"Error al obtener notas: {str(e)}")
            return []

    @staticmethod
    def obtener_nombre_estudiante(id_estudiante):
        """Obtener nombre completo de un estudiante por su ID"""
        try:
            query = "SELECT nombre, ap_paterno, ap_materno FROM estudiantes WHERE id_estudiante = %s"
            resultado = ejecutar_select(query, (id_estudiante,))
            if resultado:
                nombre, ap_paterno, ap_materno = resultado[0]
                return f"{nombre} {ap_paterno} {ap_materno}"
            return "Estudiante desconocido"
        except Exception as e:
            print(f"Error al obtener nombre de estudiante: {str(e)}")
            return "Estudiante desconocido"

    @staticmethod
    def obtener_areas_academicas():
        """Obtener lista de áreas académicas disponibles"""
        return ["Todas", "A", "B", "C", "D", "E"]