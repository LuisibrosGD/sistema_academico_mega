
from sistema_mega.database.conexion import *



# Función para ejecutar una consulta SELECT
def ejecutar_select(query, datos=None):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            cursor.execute(query, datos)
            resultados = cursor.fetchall()
            return resultados
        except mysql.connector.Error as err:
            print(f"❌ Error en la consulta: {err}")
            return []
        finally:
            cursor.close()
            conexion.close()


# Función para ejecutar consultas INSERT, UPDATE o DELETE
def ejecutar_modificacion(query, datos=None):
    conexion = obtener_conexion()
    if conexion:
        cursor = conexion.cursor()
        try:
            if datos:
                cursor.execute(query, datos)
            else:
                cursor.execute(query)
            conexion.commit()
            print("✅ Consulta ejecutada correctamente")
            return True
        except mysql.connector.Error as err:
            print(f"❌ Error en la modificación: {err}")
            conexion.rollback()
            return False
        finally:
            cursor.close()
            conexion.close()


class ModeloSedes:
    """Modelo para gestionar las operaciones CRUD de sedes"""

    @staticmethod
    def obtener_todas_sedes():
        """Obtiene todas las sedes de la base de datos"""
        query = "SELECT id_sede, nombre, distrito FROM sedes ORDER BY nombre"
        try:
            resultados = ejecutar_select(query)
            return resultados if resultados else []
        except Exception as e:
            print(f"❌ Error al obtener sedes: {e}")
            return []

    @staticmethod
    def obtener_sede_por_id(id_sede):
        """Obtiene una sede específica por su ID"""
        query = "SELECT id_sede, nombre, distrito FROM sedes WHERE id_sede = %s"
        try:
            resultados = ejecutar_select(query, (id_sede,))
            return resultados[0] if resultados else None
        except Exception as e:
            print(f"❌ Error al obtener sede por ID: {e}")
            return None

    @staticmethod
    def obtener_ciclos_por_sede(id_sede):
        """Obtiene todos los ciclos programados de una sede específica"""
        query = """
            SELECT 
                cp.id_ciclo,
                cp.nombre_ciclo,
                cp.modalidad,
                cp.costo,
                DATE_FORMAT(cp.fecha_inicio, '%Y-%m-%d') as fecha_inicio,
                DATE_FORMAT(cp.fecha_fin, '%Y-%m-%d') as fecha_fin,
                cp.estado
            FROM ciclos_programados cp
            INNER JOIN sedes_ciclos sc ON cp.id_ciclo = sc.id_ciclo
            WHERE sc.id_sede = %s
            ORDER BY cp.fecha_inicio DESC
        """
        try:
            resultados = ejecutar_select(query, (id_sede,))
            return resultados if resultados else []
        except Exception as e:
            print(f"❌ Error al obtener ciclos por sede: {e}")
            return []

    @staticmethod
    def agregar_sede(nombre, distrito):
        """Agrega una nueva sede a la base de datos"""
        query = "INSERT INTO sedes (nombre, distrito) VALUES (%s, %s)"
        try:
            if ModeloSedes.validar_sede_duplicada(nombre, distrito):
                print("❌ Ya existe una sede con ese nombre y distrito")
                return False

            resultado = ejecutar_modificacion(query, (nombre, distrito))
            if resultado:
                print(f"✅ Sede '{nombre}' agregada correctamente")
                return True
            return False
        except Exception as e:
            print(f"❌ Error al agregar sede: {e}")
            return False

    @staticmethod
    def editar_sede(id_sede, nombre, distrito):
        """Edita una sede existente"""
        query = "UPDATE sedes SET nombre = %s, distrito = %s WHERE id_sede = %s"
        try:
            # Verificar si existe otra sede con el mismo nombre y distrito (excluyendo la actual)
            if ModeloSedes.validar_sede_duplicada(nombre, distrito, id_sede):
                print("❌ Ya existe otra sede con ese nombre y distrito")
                return False

            resultado = ejecutar_modificacion(query, (nombre, distrito, id_sede))
            if resultado:
                print(f"✅ Sede actualizada correctamente")
                return True
            return False
        except Exception as e:
            print(f"❌ Error al editar sede: {e}")
            return False

    @staticmethod
    def eliminar_sede(id_sede):
        """Elimina una sede de la base de datos"""
        try:
            # Verificar si la sede tiene ciclos asociados
            ciclos = ModeloSedes.obtener_ciclos_por_sede(id_sede)
            if ciclos:
                print("❌ No se puede eliminar la sede porque tiene ciclos programados asociados")
                return False

            query = "DELETE FROM sedes WHERE id_sede = %s"
            resultado = ejecutar_modificacion(query, (id_sede,))
            if resultado:
                print(f"✅ Sede eliminada correctamente")
                return True
            return False
        except Exception as e:
            print(f"❌ Error al eliminar sede: {e}")
            return False

    @staticmethod
    def validar_sede_duplicada(nombre, distrito, id_excluir=None):
        """Verifica si ya existe una sede con el mismo nombre y distrito"""
        if id_excluir:
            query = "SELECT COUNT(*) FROM sedes WHERE nombre = %s AND distrito = %s AND id_sede != %s"
            datos = (nombre, distrito, id_excluir)
        else:
            query = "SELECT COUNT(*) FROM sedes WHERE nombre = %s AND distrito = %s"
            datos = (nombre, distrito)

        try:
            resultados = ejecutar_select(query, datos)
            return resultados[0][0] > 0 if resultados else False
        except Exception as e:
            print(f"❌ Error al validar sede duplicada: {e}")
            return False

    @staticmethod
    def validar_datos_sede(nombre, distrito):
        """Valida los datos de entrada para una sede"""
        errores = []

        # Validar nombre
        if not nombre or nombre.strip() == "":
            errores.append("El nombre de la sede es obligatorio")
        elif len(nombre.strip()) < 3:
            errores.append("El nombre de la sede debe tener al menos 3 caracteres")
        elif len(nombre.strip()) > 100:
            errores.append("El nombre de la sede no puede exceder 100 caracteres")

        # Validar distrito
        if not distrito or distrito.strip() == "":
            errores.append("El distrito es obligatorio")
        elif len(distrito.strip()) < 3:
            errores.append("El distrito debe tener al menos 3 caracteres")
        elif len(distrito.strip()) > 50:
            errores.append("El distrito no puede exceder 50 caracteres")

        return errores

    @staticmethod
    def obtener_estadisticas_sede(id_sede):
        """Obtiene estadísticas básicas de una sede"""
        try:
            # Contar total de ciclos
            query_ciclos = """
                SELECT COUNT(*) as total_ciclos
                FROM ciclos_programados cp
                INNER JOIN sedes_ciclos sc ON cp.id_ciclo = sc.id_ciclo
                WHERE sc.id_sede = %s
            """

            # Contar ciclos activos
            query_activos = """
                SELECT COUNT(*) as ciclos_activos
                FROM ciclos_programados cp
                INNER JOIN sedes_ciclos sc ON cp.id_ciclo = sc.id_ciclo
                WHERE sc.id_sede = %s AND cp.estado = 'Activo'
            """

            # Contar ciclos por modalidad
            query_modalidades = """
                SELECT cp.modalidad, COUNT(*) as cantidad
                FROM ciclos_programados cp
                INNER JOIN sedes_ciclos sc ON cp.id_ciclo = sc.id_ciclo
                WHERE sc.id_sede = %s
                GROUP BY cp.modalidad
            """

            total_ciclos = ejecutar_select(query_ciclos, (id_sede,))
            ciclos_activos = ejecutar_select(query_activos, (id_sede,))
            modalidades = ejecutar_select(query_modalidades, (id_sede,))

            estadisticas = {
                'total_ciclos': total_ciclos[0][0] if total_ciclos else 0,
                'ciclos_activos': ciclos_activos[0][0] if ciclos_activos else 0,
                'modalidades': modalidades if modalidades else []
            }

            return estadisticas
        except Exception as e:
            print(f"❌ Error al obtener estadísticas de sede: {e}")
            return None

    @staticmethod
    def buscar_sedes(termino_busqueda):
        """Busca sedes por nombre o distrito"""
        query = """
            SELECT id_sede, nombre, distrito 
            FROM sedes 
            WHERE nombre LIKE %s OR distrito LIKE %s
            ORDER BY nombre
        """
        try:
            termino = f"%{termino_busqueda}%"
            resultados = ejecutar_select(query, (termino, termino))
            return resultados if resultados else []
        except Exception as e:
            print(f"❌ Error al buscar sedes: {e}")
            return []

    @staticmethod
    def verificar_sede_existe(id_sede):
        """Verifica si una sede existe en la base de datos"""
        query = "SELECT COUNT(*) FROM sedes WHERE id_sede = %s"
        try:
            resultados = ejecutar_select(query, (id_sede,))
            return resultados[0][0] > 0 if resultados else False
        except Exception as e:
            print(f"❌ Error al verificar existencia de sede: {e}")
            return False

    @staticmethod
    def obtener_sedes_con_ciclos():
        """Obtiene todas las sedes que tienen al menos un ciclo programado"""
        query = """
            SELECT DISTINCT s.id_sede, s.nombre, s.distrito
            FROM sedes s
            INNER JOIN sedes_ciclos sc ON s.id_sede = sc.id_sede
            INNER JOIN ciclos_programados cp ON sc.id_ciclo = cp.id_ciclo
            ORDER BY s.nombre
        """
        try:
            resultados = ejecutar_select(query)
            return resultados if resultados else []
        except Exception as e:
            print(f"❌ Error al obtener sedes con ciclos: {e}")
            return []

    @staticmethod
    def obtener_sedes_sin_ciclos():
        """Obtiene todas las sedes que NO tienen ciclos programados"""
        query = """
            SELECT s.id_sede, s.nombre, s.distrito
            FROM sedes s
            LEFT JOIN sedes_ciclos sc ON s.id_sede = sc.id_sede
            WHERE sc.id_sede IS NULL
            ORDER BY s.nombre
        """
        try:
            resultados = ejecutar_select(query)
            return resultados if resultados else []
        except Exception as e:
            print(f"❌ Error al obtener sedes sin ciclos: {e}")
            return []