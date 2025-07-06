from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion


class EspecialidadModelo:
    def __init__(self):
        pass

    def obtener_todas_especialidades(self):
        """Obtiene todas las especialidades de la base de datos"""
        try:
            query = "SELECT id_especialidad, nombre_especialidad FROM especialidades"
            resultados = ejecutar_select(query)
            return resultados if resultados else []
        except Exception as e:
            print(f"Error al obtener especialidades: {e}")
            return []

    def obtener_especialidad_por_id(self, id_especialidad):
        """Obtiene una especialidad específica por su ID"""
        try:
            query = "SELECT id_especialidad, nombre_especialidad FROM especialidades WHERE id_especialidad = %s"
            resultados = ejecutar_select(query, (id_especialidad,))
            return resultados[0] if resultados else None
        except Exception as e:
            print(f"Error al obtener especialidad por ID: {e}")
            return None

    def agregar_especialidad(self, nombre_especialidad):
        """Agrega una nueva especialidad a la base de datos"""
        try:
            query = "INSERT INTO especialidades (nombre_especialidad) VALUES (%s)"
            ejecutar_modificacion(query, (nombre_especialidad,))
            return True
        except Exception as e:
            print(f"Error al agregar especialidad: {e}")
            return False

    def editar_especialidad(self, id_especialidad, nuevo_nombre):
        """Edita una especialidad existente"""
        try:
            query = "UPDATE especialidades SET nombre_especialidad = %s WHERE id_especialidad = %s"
            ejecutar_modificacion(query, (nuevo_nombre, id_especialidad))
            return True
        except Exception as e:
            print(f"Error al editar especialidad: {e}")
            return False

    def existe_especialidad(self, nombre_especialidad):
        """Verifica si ya existe una especialidad con ese nombre"""
        try:
            query = "SELECT COUNT(*) FROM especialidades WHERE nombre_especialidad = %s"
            resultados = ejecutar_select(query, (nombre_especialidad,))
            return resultados[0][0] > 0 if resultados else False
        except Exception as e:
            print(f"Error al verificar especialidad: {e}")
            return False