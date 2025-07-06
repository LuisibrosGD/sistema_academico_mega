from datetime import datetime
from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion


class FuncionesColaborador:
    @staticmethod
    def obtener_profesores_con_cursos():
        """Obtener profesores con sus cursos (sin grupos)"""
        query = """
        SELECT 
            p.id_profesor,
            CONCAT(p.nombre, ' ', p.ap_paterno, ' ', p.ap_materno) AS nombre_profesor,
            c.nombre_curso
        FROM profesores p
        JOIN ciclos_cursos cc ON cc.id_profesor = p.id_profesor
        JOIN cursos c ON c.id_curso = cc.id_curso
        WHERE cc.id_ciclo 
        """
        return ejecutar_select(query)

    @staticmethod
    def registrar_asistencia(estado, id_profesor, fecha=None):
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
        query = "SELECT id_estudiante, CONCAT(nombre, ' ', ap_paterno, ' ', ap_materno) FROM estudiantes"
        return ejecutar_select(query)

    @staticmethod
    def registrar_calificacion(id_estudiante, puntaje, fecha_realizacion):
        try:
            query = "INSERT INTO examenes (puntaje, fecha_realizacion, id_estudiante) VALUES (%s, %s, %s)"
            datos = (puntaje, fecha_realizacion, id_estudiante)
            ejecutar_modificacion(query, datos)
            return True, "Calificación registrada exitosamente"
        except Exception as e:
            return False, f"Error al registrar calificación: {str(e)}"

    @staticmethod
    def obtener_notas_estudiantes(filtro_grupo=None, filtro_area=None, fecha_ini=None, fecha_fin=None):
        """Obtener notas con estructura simplificada"""
        query = """
        SELECT 
            s.nombre AS sede,
            cp.nombre_ciclo AS ciclo,
            CONCAT(e.nombre, ' ', e.ap_paterno, ' ', e.ap_materno) AS estudiante,
            e.area_academica AS area,
            ex.puntaje AS nota,
            ex.fecha_realizacion AS fecha
        FROM examenes ex
        JOIN estudiantes e ON ex.id_estudiante = e.id_estudiante
        JOIN inscripciones i ON i.id_estudiante = e.id_estudiante
        JOIN ciclos_programados cp ON cp.id_ciclo = i.id_ciclo
        JOIN sedes_ciclos sc ON sc.id_ciclo = cp.id_ciclo
        JOIN sedes s ON s.id_sede = sc.id_sede
        WHERE 1=1
        """

        params = []

        if filtro_area and filtro_area != "Todas":
            query += " AND e.area_academica = %s"
            params.append(filtro_area)

        if fecha_ini:
            query += " AND ex.fecha_realizacion >= %s"
            params.append(fecha_ini)

        if fecha_fin:
            query += " AND ex.fecha_realizacion <= %s"
            params.append(fecha_fin)

        query += " ORDER BY ex.fecha_realizacion DESC"

        return ejecutar_select(query, tuple(params) if params else None)

    @staticmethod
    def obtener_nombre_estudiante(id_estudiante):
        """Obtener nombre completo de estudiante"""
        query = "SELECT nombre, ap_paterno, ap_materno FROM estudiantes WHERE id_estudiante = %s"
        resultado = ejecutar_select(query, (id_estudiante,))
        if resultado:
            nombre, ap_paterno, ap_materno = resultado[0]
            return f"{nombre} {ap_paterno} {ap_materno}"
        return "Estudiante desconocido"

    @staticmethod
    def obtener_areas_academicas():
        """Obtener lista de áreas académicas"""
        return ["Todas", "A", "B", "C", "D", "E"]