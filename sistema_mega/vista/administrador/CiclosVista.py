import tkinter as tk
from tkinter import ttk, messagebox
from sistema_mega.modelo.ModeloCiclos import ModeloCiclos


class CiclosVista:
    """Vista para manejar la visualización y gestión de ciclos"""

    def __init__(self, parent_window):
        self.parent_window = parent_window
        self.sede_info = None
        self.ciclos_data = []

    def mostrar_ciclos_sede(self, sede_info):
        """
        Mostrar ventana con los ciclos de una sede específica

        Args:
            sede_info (tuple): Información de la sede (id, nombre, distrito)
        """
        self.sede_info = sede_info

        try:
            # Obtener ciclos de la sede
            self.ciclos_data = ModeloCiclos.obtener_ciclos_por_sede(sede_info[0])

            # Crear y mostrar la ventana
            self.crear_ventana_ciclos()

        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener ciclos: {str(e)}")
            print(f"❌ Error al obtener ciclos: {e}")

    def crear_ventana_ciclos(self):
        """Crear la ventana principal para mostrar ciclos"""
        self.ventana_ciclos = tk.Toplevel(self.parent_window)
        self.ventana_ciclos.title(f"Ciclos de {self.sede_info[1]}")
        self.ventana_ciclos.geometry("1000x700")
        self.ventana_ciclos.configure(bg="#f0f0f0")
        self.ventana_ciclos.resizable(True, True)

        # Centrar ventana
        self.ventana_ciclos.transient(self.parent_window)
        self.ventana_ciclos.grab_set()

        # Configurar grid principal
        self.ventana_ciclos.rowconfigure(1, weight=1)
        self.ventana_ciclos.columnconfigure(0, weight=1)

        # Crear componentes
        self.crear_header_ciclos()
        self.crear_area_contenido_ciclos()
        self.crear_botones_accion_ciclos()

    def crear_header_ciclos(self):
        """Crear el header con información de la sede"""
        header_frame = ttk.Frame(self.ventana_ciclos)
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)
        header_frame.columnconfigure(0, weight=1)

        # Título principal
        titulo_label = ttk.Label(header_frame,
                                 text=f"Ciclos Programados - {self.sede_info[1]}",
                                 font=("Arial", 18, "bold"))
        titulo_label.grid(row=0, column=0, sticky="w")

        # Subtítulo con distrito
        subtitulo_label = ttk.Label(header_frame,
                                    text=f"Distrito: {self.sede_info[2]}",
                                    font=("Arial", 12))
        subtitulo_label.grid(row=1, column=0, sticky="w", pady=(5, 0))

        # Separador
        separator = ttk.Separator(header_frame, orient="horizontal")
        separator.grid(row=2, column=0, sticky="ew", pady=(10, 0))

    def crear_area_contenido_ciclos(self):
        """Crear el área de contenido para mostrar los ciclos"""
        contenido_frame = ttk.Frame(self.ventana_ciclos)
        contenido_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        contenido_frame.rowconfigure(0, weight=1)
        contenido_frame.columnconfigure(0, weight=1)

        if not self.ciclos_data:
            self.mostrar_mensaje_sin_ciclos(contenido_frame)
        else:
            self.mostrar_tabla_ciclos(contenido_frame)
            self.mostrar_estadisticas_ciclos(contenido_frame)

    def mostrar_mensaje_sin_ciclos(self, parent):
        """Mostrar mensaje cuando no hay ciclos disponibles"""
        mensaje_frame = ttk.Frame(parent)
        mensaje_frame.grid(row=0, column=0, sticky="nsew")
        mensaje_frame.rowconfigure(0, weight=1)
        mensaje_frame.columnconfigure(0, weight=1)

        # Icono y mensaje
        no_ciclos_label = ttk.Label(mensaje_frame,
                                    text="📅 No hay ciclos programados para esta sede",
                                    font=("Arial", 16))
        no_ciclos_label.grid(row=0, column=0, pady=50)

        # Mensaje adicional
        info_label = ttk.Label(mensaje_frame,
                               text="Los ciclos aparecerán aquí cuando sean programados",
                               font=("Arial", 12),
                               foreground="gray")
        info_label.grid(row=1, column=0, pady=(0, 20))

    def mostrar_tabla_ciclos(self, parent):
        """Mostrar la tabla con los ciclos"""
        # Frame para la tabla
        tabla_frame = ttk.Frame(parent)
        tabla_frame.grid(row=0, column=0, sticky="nsew", pady=(0, 20))
        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)

        # Crear Treeview
        self.crear_treeview_ciclos(tabla_frame)

        # Insertar datos
        self.cargar_datos_en_tabla()

    def crear_treeview_ciclos(self, parent):
        """Crear el Treeview para mostrar los ciclos"""
        # Definir columnas
        columnas = ("ID", "Nombre", "Modalidad", "Costo", "Inicio", "Fin", "Estado")

        # Crear Treeview
        self.tree_ciclos = ttk.Treeview(parent, columns=columnas, show="headings", height=15)

        # Configurar encabezados
        headers_config = {
            "ID": ("ID", 50),
            "Nombre": ("Nombre del Ciclo", 250),
            "Modalidad": ("Modalidad", 120),
            "Costo": ("Costo", 80),
            "Inicio": ("Fecha Inicio", 100),
            "Fin": ("Fecha Fin", 100),
            "Estado": ("Estado", 100)
        }

        for col, (texto, ancho) in headers_config.items():
            self.tree_ciclos.heading(col, text=texto)
            self.tree_ciclos.column(col, width=ancho)

        # Scrollbars
        scrollbar_v = ttk.Scrollbar(parent, orient="vertical", command=self.tree_ciclos.yview)
        scrollbar_h = ttk.Scrollbar(parent, orient="horizontal", command=self.tree_ciclos.xview)

        self.tree_ciclos.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

        # Grid layout
        self.tree_ciclos.grid(row=0, column=0, sticky="nsew")
        scrollbar_v.grid(row=0, column=1, sticky="ns")
        scrollbar_h.grid(row=1, column=0, sticky="ew")

        # Eventos
        self.tree_ciclos.bind("<Double-1>", self.on_doble_click_ciclo)
        self.tree_ciclos.bind("<Button-3>", self.mostrar_menu_contextual)

    def cargar_datos_en_tabla(self):
        """Cargar los datos de ciclos en la tabla"""
        # Limpiar tabla
        for item in self.tree_ciclos.get_children():
            self.tree_ciclos.delete(item)

        # Insertar datos
        for ciclo in self.ciclos_data:
            self.tree_ciclos.insert("", "end", values=ciclo)

    def mostrar_estadisticas_ciclos(self, parent):
        """Mostrar estadísticas de los ciclos"""
        stats_frame = ttk.LabelFrame(parent, text="Estadísticas", padding=(10, 5))
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(10, 0))
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
        stats_frame.columnconfigure(2, weight=1)

        # Calcular estadísticas
        total_ciclos = len(self.ciclos_data)
        ciclos_activos = sum(1 for ciclo in self.ciclos_data if ciclo[6] == "Activo")
        ciclos_finalizados = sum(1 for ciclo in self.ciclos_data if ciclo[6] == "Finalizado")

        # Mostrar estadísticas
        stats_info = [
            ("Total de ciclos", total_ciclos),
            ("Ciclos activos", ciclos_activos),
            ("Ciclos finalizados", ciclos_finalizados)
        ]

        for i, (label, valor) in enumerate(stats_info):
            stat_label = ttk.Label(stats_frame, text=f"{label}: {valor}", font=("Arial", 12, "bold"))
            stat_label.grid(row=0, column=i, padx=10, pady=5)

    def crear_botones_accion_ciclos(self):
        """Crear los botones de acción para ciclos"""
        botones_frame = ttk.Frame(self.ventana_ciclos)
        botones_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 20))
        botones_frame.columnconfigure(0, weight=1)

        # Frame para botones principales
        acciones_frame = ttk.Frame(botones_frame)
        acciones_frame.pack(fill="x", pady=(0, 10))

        # Botones de acción
        botones_config = [
            ("Agregar Ciclo", self.agregar_ciclo, "#28a745"),
            ("Editar Ciclo", self.editar_ciclo, "#ffc107"),
            ("Eliminar Ciclo", self.eliminar_ciclo, "#dc3545"),
            ("Actualizar", self.actualizar_ciclos, "#17a2b8")
        ]

        for i, (texto, comando, color) in enumerate(botones_config):
            boton = ttk.Button(acciones_frame, text=texto, command=comando)
            boton.grid(row=0, column=i, padx=5, pady=5, sticky="ew")
            acciones_frame.columnconfigure(i, weight=1)

        # Botón cerrar
        boton_cerrar = ttk.Button(botones_frame, text="Cerrar", command=self.cerrar_ventana)
        boton_cerrar.pack(pady=(10, 0))

    def on_doble_click_ciclo(self, event):
        """Manejar doble click en un ciclo"""
        seleccion = self.tree_ciclos.selection()
        if seleccion:
            self.ver_detalles_ciclo()

    def mostrar_menu_contextual(self, event):
        """Mostrar menú contextual al hacer clic derecho"""
        seleccion = self.tree_ciclos.selection()
        if seleccion:
            menu = tk.Menu(self.ventana_ciclos, tearoff=0)
            menu.add_command(label="Ver detalles", command=self.ver_detalles_ciclo)
            menu.add_separator()
            menu.add_command(label="Editar", command=self.editar_ciclo)
            menu.add_command(label="Eliminar", command=self.eliminar_ciclo)
            menu.tk_popup(event.x_root, event.y_root)

    def ver_detalles_ciclo(self):
        """Ver detalles del ciclo seleccionado"""
        seleccion = self.tree_ciclos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un ciclo para ver detalles")
            return

        # Obtener datos del ciclo seleccionado
        item = self.tree_ciclos.item(seleccion[0])
        valores = item['values']

        # Crear ventana de detalles
        self.mostrar_ventana_detalles(valores)

    def mostrar_ventana_detalles(self, datos_ciclo):
        """Mostrar ventana con detalles del ciclo"""
        ventana_detalles = tk.Toplevel(self.ventana_ciclos)
        ventana_detalles.title("Detalles del Ciclo")
        ventana_detalles.geometry("500x400")
        ventana_detalles.configure(bg="#f0f0f0")
        ventana_detalles.resizable(False, False)

        # Centrar ventana
        ventana_detalles.transient(self.ventana_ciclos)
        ventana_detalles.grab_set()

        # Crear contenido de detalles
        main_frame = ttk.Frame(ventana_detalles, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Título
        titulo_label = ttk.Label(main_frame, text="Información del Ciclo",
                                 font=("Arial", 16, "bold"))
        titulo_label.pack(pady=(0, 20))

        # Información del ciclo
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill="x", pady=(0, 20))

        campos = [
            ("ID", datos_ciclo[0]),
            ("Nombre", datos_ciclo[1]),
            ("Modalidad", datos_ciclo[2]),
            ("Costo", f"S/. {datos_ciclo[3]}"),
            ("Fecha de Inicio", datos_ciclo[4]),
            ("Fecha de Fin", datos_ciclo[5]),
            ("Estado", datos_ciclo[6])
        ]

        for i, (campo, valor) in enumerate(campos):
            label_campo = ttk.Label(info_frame, text=f"{campo}:", font=("Arial", 12, "bold"))
            label_campo.grid(row=i, column=0, sticky="w", padx=(0, 10), pady=5)

            label_valor = ttk.Label(info_frame, text=str(valor), font=("Arial", 12))
            label_valor.grid(row=i, column=1, sticky="w", pady=5)

        # Botón cerrar
        boton_cerrar = ttk.Button(main_frame, text="Cerrar", command=ventana_detalles.destroy)
        boton_cerrar.pack(pady=(20, 0))

    def agregar_ciclo(self):
        """Agregar un nuevo ciclo"""
        messagebox.showinfo("Función en desarrollo", "La función de agregar ciclo estará disponible próximamente")

    def editar_ciclo(self):
        """Editar el ciclo seleccionado"""
        seleccion = self.tree_ciclos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un ciclo para editar")
            return

        messagebox.showinfo("Función en desarrollo", "La función de editar ciclo estará disponible próximamente")

    def eliminar_ciclo(self):
        """Eliminar el ciclo seleccionado"""
        seleccion = self.tree_ciclos.selection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Seleccione un ciclo para eliminar")
            return

        # Confirmar eliminación
        respuesta = messagebox.askyesno("Confirmar eliminación",
                                        "¿Está seguro que desea eliminar este ciclo?")
        if respuesta:
            messagebox.showinfo("Función en desarrollo", "La función de eliminar ciclo estará disponible próximamente")

    def actualizar_ciclos(self):
        """Actualizar la lista de ciclos"""
        try:
            self.ciclos_data = ModeloCiclos.obtener_ciclos_por_sede(self.sede_info[0])
            self.cargar_datos_en_tabla()
            messagebox.showinfo("Éxito", "Lista de ciclos actualizada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar ciclos: {str(e)}")

    def cerrar_ventana(self):
        """Cerrar la ventana de ciclos"""
        self.ventana_ciclos.destroy()


# Función de prueba independiente
if __name__ == "__main__":
    # Crear ventana principal para pruebas
    root = tk.Tk()
    root.title("Prueba Vista Ciclos")
    root.geometry("300x200")


    def test_ciclos():
        sede_info = (1, "Sede Principal", "Lima")
        vista_ciclos = CiclosVista(root)
        vista_ciclos.mostrar_ciclos_sede(sede_info)


    boton_test = ttk.Button(root, text="Probar Vista Ciclos", command=test_ciclos)
    boton_test.pack(pady=50)

    root.mainloop()