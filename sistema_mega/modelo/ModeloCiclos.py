class ModeloCiclos:
    """Modelo para manejar operaciones relacionadas con ciclos"""

    @staticmethod
    def obtener_ciclos_por_sede(id_sede):
        """
        Obtener todos los ciclos programados para una sede específica

        Args:
            id_sede (int): ID de la sede

        Returns:
            list: Lista de tuplas con información de ciclos
        """
        try:
            # Aquí iría la lógica para obtener ciclos de la base de datos
            # Por ahora importamos desde ModeloSedes para mantener compatibilidad
            from sistema_mega.modelo.modelo_sedes import ModeloSedes
            return ModeloSedes.obtener_ciclos_por_sede(id_sede)
        except Exception as e:
            print(f"❌ Error al obtener ciclos por sede: {e}")
            raise e

    @staticmethod
    def obtener_ciclo_por_id(id_ciclo):
        """
        Obtener información de un ciclo específico

        Args:
            id_ciclo (int): ID del ciclo

        Returns:
            tuple: Información del ciclo o None si no existe
        """
        try:
            # Implementar lógica para obtener un ciclo específico
            # Esta función se puede implementar cuando se necesite
            pass
        except Exception as e:
            print(f"❌ Error al obtener ciclo por ID: {e}")
            raise e

    @staticmethod
    def validar_datos_ciclo(nombre, modalidad, costo, fecha_inicio, fecha_fin):
        """
        Validar datos de un ciclo

        Args:
            nombre (str): Nombre del ciclo
            modalidad (str): Modalidad del ciclo
            costo (float): Costo del ciclo
            fecha_inicio (str): Fecha de inicio
            fecha_fin (str): Fecha de fin

        Returns:
            list: Lista de errores de validación
        """
        errores = []

        if not nombre or not nombre.strip():
            errores.append("El nombre del ciclo es obligatorio")

        if not modalidad or not modalidad.strip():
            errores.append("La modalidad es obligatoria")

        if costo is None or costo < 0:
            errores.append("El costo debe ser un valor positivo")

        if not fecha_inicio or not fecha_inicio.strip():
            errores.append("La fecha de inicio es obligatoria")

        if not fecha_fin or not fecha_fin.strip():
            errores.append("La fecha de fin es obligatoria")

        # Validar formato de fechas (implementar según necesidades)
        # Aquí se pueden agregar más validaciones específicas

        return errores

    @staticmethod
    def agregar_ciclo(id_sede, nombre, modalidad, costo, fecha_inicio, fecha_fin):
        """
        Agregar un nuevo ciclo

        Args:
            id_sede (int): ID de la sede
            nombre (str): Nombre del ciclo
            modalidad (str): Modalidad del ciclo
            costo (float): Costo del ciclo
            fecha_inicio (str): Fecha de inicio
            fecha_fin (str): Fecha de fin

        Returns:
            bool: True si se agregó exitosamente, False en caso contrario
        """
        try:
            # Implementar lógica para agregar ciclo a la base de datos
            # Esta función se puede implementar cuando se necesite
            pass
        except Exception as e:
            print(f"❌ Error al agregar ciclo: {e}")
            return False

    @staticmethod
    def editar_ciclo(id_ciclo, nombre, modalidad, costo, fecha_inicio, fecha_fin):
        """
        Editar un ciclo existente

        Args:
            id_ciclo (int): ID del ciclo a editar
            nombre (str): Nuevo nombre del ciclo
            modalidad (str): Nueva modalidad del ciclo
            costo (float): Nuevo costo del ciclo
            fecha_inicio (str): Nueva fecha de inicio
            fecha_fin (str): Nueva fecha de fin

        Returns:
            bool: True si se editó exitosamente, False en caso contrario
        """
        try:
            # Implementar lógica para editar ciclo en la base de datos
            # Esta función se puede implementar cuando se necesite
            pass
        except Exception as e:
            print(f"❌ Error al editar ciclo: {e}")
            return False

    @staticmethod
    def eliminar_ciclo(id_ciclo):
        """
        Eliminar un ciclo

        Args:
            id_ciclo (int): ID del ciclo a eliminar

        Returns:
            bool: True si se eliminó exitosamente, False en caso contrario
        """
        try:
            # Implementar lógica para eliminar ciclo de la base de datos
            # Esta función se puede implementar cuando se necesite
            pass
        except Exception as e:
            print(f"❌ Error al eliminar ciclo: {e}")
            return False

    @staticmethod
    def obtener_estadisticas_ciclos(id_sede=None):
        """
        Obtener estadísticas de ciclos

        Args:
            id_sede (int, optional): ID de la sede. Si no se especifica, obtiene estadísticas globales

        Returns:
            dict: Diccionario con estadísticas de ciclos
        """
        try:
            # Implementar lógica para obtener estadísticas
            # Esta función se puede implementar cuando se necesite
            return {
                'total_ciclos': 0,
                'ciclos_activos': 0,
                'ciclos_finalizados': 0,
                'ciclos_programados': 0
            }
        except Exception as e:
            print(f"❌ Error al obtener estadísticas de ciclos: {e}")
            return {}