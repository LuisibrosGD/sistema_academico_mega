from sistema_mega.database.conexion import ejecutar_select


class ProfesorEspecialidadModelo:
    def __init__(self):
        pass

    def obtener_profesores_por_especialidad(self, id_especialidad):
        """Obtiene todos los profesores que tienen una especialidad específica"""
        try:
            query = """
                SELECT DISTINCT 
                    p.id_profesor,
                    p.nombre,
                    p.ap_paterno,
                    p.ap_materno,
                    p.tipo_documento,
                    p.nro_documento,
                    u.correo,
                    u.estado
                FROM profesores p
                INNER JOIN profesores_especialidades pe ON p.id_profesor = pe.id_profesor
                INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
                WHERE pe.id_especialidad = %s
                ORDER BY p.nombre, p.ap_paterno
            """
            resultados = ejecutar_select(query, (id_especialidad,))
            return resultados if resultados else []
        except Exception as e:
            print(f"Error al obtener profesores por especialidad: {e}")
            return []

    def obtener_especialidades_profesor(self, id_profesor):
        """Obtiene todas las especialidades de un profesor específico"""
        try:
            query = """
                SELECT e.id_especialidad, e.nombre_especialidad
                FROM especialidades e
                INNER JOIN profesores_especialidades pe ON e.id_especialidad = pe.id_especialidad
                WHERE pe.id_profesor = %s
                ORDER BY e.nombre_especialidad
            """
            resultados = ejecutar_select(query, (id_profesor,))
            return resultados if resultados else []
        except Exception as e:
            print(f"Error al obtener especialidades del profesor: {e}")
            return []

    def contar_profesores_por_especialidad(self, id_especialidad):
        """Cuenta el número de profesores que tienen una especialidad específica"""
        try:
            query = """
                SELECT COUNT(DISTINCT p.id_profesor)
                FROM profesores p
                INNER JOIN profesores_especialidades pe ON p.id_profesor = pe.id_profesor
                WHERE pe.id_especialidad = %s
            """
            resultados = ejecutar_select(query, (id_especialidad,))
            return resultados[0][0] if resultados else 0
        except Exception as e:
            print(f"Error al contar profesores por especialidad: {e}")
            return 0