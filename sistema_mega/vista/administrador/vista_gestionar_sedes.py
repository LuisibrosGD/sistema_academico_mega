import tkinter as tk
from tkinter import ttk, messagebox
from sistema_mega.modelo.modelo_sedes import ModeloSedes
from sistema_mega.vista.administrador.CiclosVista import CiclosVista


class GestionarSedes:
    def __init__(self, parent=None):
        self.parent = parent
        self.root = tk.Tk() if parent is None else tk.Toplevel(parent)
        self.root.title("Gestionar Sedes")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f0f0f0")

        # Variables
        self.sedes_data = []
        self.sede_seleccionada = None
        self.ciclos_vista = None

        # Configurar el grid principal
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.configurar_estilos()
        self.crear_widgets()
        self.cargar_sedes()

    def configurar_estilos(self):
        """Configurar los estilos de la interfaz"""
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")

        # Estilo para el frame principal
        self.estilo.configure("framePrincipal.TFrame",
                              background="#f0f0f0")

        # Estilo para el título
        self.estilo.configure("tituloSedes.TLabel",
                              background="#f0f0f0",
                              foreground="#333333",
                              font=("Arial", 24, "bold"))

        # Estilo para las tarjetas de sedes
        self.estilo.configure("sedeCard.TFrame",
                              background="#4a90e2",
                              relief="raised",
                              borderwidth=2)

        # Estilo para tarjeta seleccionada
        self.estilo.configure("sedeCardSeleccionada.TFrame",
                              background="#2c5282",
                              relief="raised",
                              borderwidth=3)

        # Estilo para el texto de las sedes
        self.estilo.configure("sedeNombre.TLabel",
                              background="#4a90e2",
                              foreground="white",
                              font=("Arial", 14, "bold"))

        self.estilo.configure("sedeDistrito.TLabel",
                              background="#4a90e2",
                              foreground="white",
                              font=("Arial", 12))

        # Estilo para botones principales
        self.estilo.configure("botonAgregar.TButton",
                              background="#28a745",
                              foreground="white",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonAgregar.TButton",
                        background=[("pressed", "#218838"), ("active", "#34ce57")])

        self.estilo.configure("botonEditar.TButton",
                              background="#ffc107",
                              foreground="black",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonEditar.TButton",
                        background=[("pressed", "#e0a800"), ("active", "#ffcd39")])

        # Estilo para botón Ver Ciclos
        self.estilo.configure("botonVerCiclos.TButton",
                              background="#17a2b8",
                              foreground="white",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonVerCiclos.TButton",
                        background=[("pressed", "#138496"), ("active", "#1fc8e3")])

        # Estilo para botón de regresar
        self.estilo.configure("botonRegresar.TButton",
                              background="#6c757d",
                              foreground="white",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonRegresar.TButton",
                        background=[("pressed", "#5a6268"), ("active", "#78848b")])

        # Estilo para botón eliminar
        self.estilo.configure("botonEliminar.TButton",
                              background="#dc3545",
                              foreground="white",
                              font=("Arial", 10, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonEliminar.TButton",
                        background=[("pressed", "#c82333"), ("active", "#e4606d")])

    def crear_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        self.frame_principal = ttk.Frame(self.root, style="framePrincipal.TFrame")
        self.frame_principal.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Configurar grid del frame principal
        self.frame_principal.rowconfigure(1, weight=1)
        self.frame_principal.columnconfigure(0, weight=1)

        # Crear header
        self.crear_header()

        # Crear área de sedes
        self.crear_area_sedes()

        # Crear botones de acción
        self.crear_botones_accion()

        # Crear botón de regresar
        self.crear_boton_regresar()

    def crear_header(self):
        """Crear el header con título y botones de acción"""
        header_frame = ttk.Frame(self.frame_principal, style="framePrincipal.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)

        # Título
        titulo_label = ttk.Label(header_frame,
                                 text="Sedes Disponibles",
                                 style="tituloSedes.TLabel")
        titulo_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

    def crear_area_sedes(self):
        """Crear el área scrollable para mostrar las sedes"""
        # Frame contenedor con scrollbar
        container_frame = ttk.Frame(self.frame_principal, style="framePrincipal.TFrame")
        container_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        container_frame.rowconfigure(0, weight=1)
        container_frame.columnconfigure(0, weight=1)

        # Canvas para scroll
        self.canvas = tk.Canvas(container_frame, bg="#f0f0f0", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno del canvas
        self.frame_sedes = ttk.Frame(self.canvas, style="framePrincipal.TFrame")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame_sedes, anchor="nw")

        # Configurar el scroll
        self.frame_sedes.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Bind del mouse wheel
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def crear_botones_accion(self):
        """Crear los botones de acción (Agregar, Editar y Ver Ciclos)"""
        botones_frame = ttk.Frame(self.frame_principal, style="framePrincipal.TFrame")
        botones_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        botones_frame.columnconfigure(0, weight=1)
        botones_frame.columnconfigure(1, weight=1)
        botones_frame.columnconfigure(2, weight=1)

        # Botón Agregar sede
        self.boton_agregar = ttk.Button(botones_frame,
                                        text="Crear sede",
                                        style="botonAgregar.TButton",
                                        command=self.agregar_sede)
        self.boton_agregar.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=5)

        # Botón Editar sede
        self.boton_editar = ttk.Button(botones_frame,
                                       text="Editar sede",
                                       style="botonEditar.TButton",
                                       command=self.editar_sede)
        self.boton_editar.grid(row=0, column=1, sticky="ew", padx=(5, 5), pady=5)

        # Botón Ver Ciclos - REFACTORIZADO
        self.boton_ver_ciclos = ttk.Button(botones_frame,
                                           text="Ver ciclos",
                                           style="botonVerCiclos.TButton",
                                           command=self.ver_ciclos_sede)
        self.boton_ver_ciclos.grid(row=0, column=2, sticky="ew", padx=(5, 0), pady=5)

    def crear_boton_regresar(self):
        """Crear el botón de regresar en la esquina inferior izquierda"""
        self.boton_regresar = ttk.Button(self.frame_principal,
                                         text="Regresar a Menú principal",
                                         style="botonRegresar.TButton",
                                         command=self.regresar_menu)
        self.boton_regresar.grid(row=3, column=0, sticky="w", pady=(10, 0))

    def cargar_sedes(self):
        """Cargar las sedes desde la base de datos"""
        try:
            self.sedes_data = ModeloSedes.obtener_todas_sedes()
            self.mostrar_sedes()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar sedes: {str(e)}")
            print(f"❌ Error al cargar sedes: {e}")

    def mostrar_sedes(self):
        """Mostrar las sedes en el área de sedes"""
        # Limpiar frame actual
        for widget in self.frame_sedes.winfo_children():
            widget.destroy()

        if not self.sedes_data:
            # Mostrar mensaje si no hay sedes
            no_sedes_label = ttk.Label(self.frame_sedes,
                                       text="No hay sedes disponibles",
                                       style="tituloSedes.TLabel")
            no_sedes_label.grid(row=0, column=0, pady=50)
            return

        # Configurar grid para mostrar sedes en filas
        columnas_por_fila = 4
        for i, (id_sede, nombre, distrito) in enumerate(self.sedes_data):
            fila = i // columnas_por_fila
            columna = i % columnas_por_fila

            # Configurar columnas del grid
            self.frame_sedes.columnconfigure(columna, weight=1)

            # Crear tarjeta de sede
            self.crear_tarjeta_sede(self.frame_sedes, id_sede, nombre, distrito, fila, columna)

        # Actualizar scroll region
        self.frame_sedes.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def crear_tarjeta_sede(self, parent, id_sede, nombre, distrito, fila, columna):
        """Crear una tarjeta individual para una sede"""
        # Frame de la tarjeta
        card_frame = ttk.Frame(parent, style="sedeCard.TFrame")
        card_frame.grid(row=fila, column=columna, sticky="ew", padx=10, pady=10)
        card_frame.configure(padding=(15, 10))

        # Configurar grid de la tarjeta
        card_frame.columnconfigure(0, weight=1)

        # Nombre de la sede
        nombre_label = ttk.Label(card_frame,
                                 text=nombre,
                                 style="sedeNombre.TLabel")
        nombre_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Distrito
        distrito_label = ttk.Label(card_frame,
                                   text=f"Sede {distrito}",
                                   style="sedeDistrito.TLabel")
        distrito_label.grid(row=1, column=0, sticky="w", pady=(0, 10))

        # Hacer la tarjeta clickeable para seleccionar
        def seleccionar_sede(event):
            self.sede_seleccionada = (id_sede, nombre, distrito)
            self.resaltar_sede_seleccionada()

        card_frame.bind("<Button-1>", seleccionar_sede)
        nombre_label.bind("<Button-1>", seleccionar_sede)
        distrito_label.bind("<Button-1>", seleccionar_sede)

        # Guardar referencia para resaltar
        card_frame.id_sede = id_sede

    def resaltar_sede_seleccionada(self):
        """Resaltar la sede seleccionada"""
        for widget in self.frame_sedes.winfo_children():
            if hasattr(widget, 'id_sede'):
                if widget.id_sede == self.sede_seleccionada[0]:
                    widget.configure(style="sedeCardSeleccionada.TFrame")
                else:
                    widget.configure(style="sedeCard.TFrame")

    def agregar_sede(self):
        """Abrir ventana para agregar nueva sede"""
        self.ventana_formulario("Agregar Sede", self.guardar_nueva_sede)

    def editar_sede(self):
        """Abrir ventana para editar sede seleccionada"""
        if not self.sede_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor seleccione una sede para editar")
            return

        self.ventana_formulario("Editar Sede", self.guardar_edicion_sede, self.sede_seleccionada)

    def ver_ciclos_sede(self):
        """Mostrar los ciclos programados de la sede seleccionada - REFACTORIZADO"""
        if not self.sede_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor seleccione una sede para ver sus ciclos")
            return

        try:
            # Crear instancia de CiclosVista y mostrar ciclos
            self.ciclos_vista = CiclosVista(self.root)
            self.ciclos_vista.mostrar_ciclos_sede(self.sede_seleccionada)

        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar ciclos: {str(e)}")
            print(f"❌ Error al mostrar ciclos: {e}")

    def ventana_formulario(self, titulo, comando_guardar, datos_sede=None):
        """Crear ventana de formulario para agregar/editar sede"""
        ventana = tk.Toplevel(self.root)
        ventana.title(titulo)
        ventana.geometry("400x300")
        ventana.configure(bg="#f0f0f0")
        ventana.resizable(False, False)

        # Centrar ventana
        ventana.transient(self.root)
        ventana.grab_set()

        # Variables
        nombre_var = tk.StringVar()
        distrito_var = tk.StringVar()

        # Si es edición, cargar datos
        if datos_sede:
            nombre_var.set(datos_sede[1])
            distrito_var.set(datos_sede[2])

        # Título
        titulo_label = ttk.Label(ventana, text=titulo, font=("Arial", 16, "bold"))
        titulo_label.pack(pady=20)

        # Frame del formulario
        form_frame = ttk.Frame(ventana)
        form_frame.pack(padx=40, pady=20, fill="both", expand=True)

        # Campo nombre
        ttk.Label(form_frame, text="Nombre de la sede:", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))
        entry_nombre = ttk.Entry(form_frame, textvariable=nombre_var, font=("Arial", 12))
        entry_nombre.pack(fill="x", pady=(0, 15))

        # Campo distrito
        ttk.Label(form_frame, text="Distrito:", font=("Arial", 12)).pack(anchor="w", pady=(0, 5))
        entry_distrito = ttk.Entry(form_frame, textvariable=distrito_var, font=("Arial", 12))
        entry_distrito.pack(fill="x", pady=(0, 20))

        # Botones
        botones_frame = ttk.Frame(form_frame)
        botones_frame.pack(fill="x", pady=20)

        ttk.Button(botones_frame, text="Cancelar",
                   command=ventana.destroy).pack(side="right", padx=(10, 0))

        ttk.Button(botones_frame, text="Guardar",
                   command=lambda: comando_guardar(ventana, nombre_var.get(), distrito_var.get(),
                                                   datos_sede[0] if datos_sede else None)).pack(side="right")

        # Focus en el primer campo
        entry_nombre.focus()

    def guardar_nueva_sede(self, ventana, nombre, distrito, id_sede=None):
        """Guardar nueva sede"""
        # Validar datos
        errores = ModeloSedes.validar_datos_sede(nombre, distrito)
        if errores:
            messagebox.showerror("Error de validación", "\n".join(errores))
            return

        # Agregar sede
        if ModeloSedes.agregar_sede(nombre.strip(), distrito.strip()):
            messagebox.showinfo("Éxito", "Sede agregada correctamente")
            ventana.destroy()
            self.cargar_sedes()
        else:
            messagebox.showerror("Error", "No se pudo agregar la sede")

    def guardar_edicion_sede(self, ventana, nombre, distrito, id_sede):
        """Guardar edición de sede"""
        # Validar datos
        errores = ModeloSedes.validar_datos_sede(nombre, distrito)
        if errores:
            messagebox.showerror("Error de validación", "\n".join(errores))
            return

        # Editar sede
        if ModeloSedes.editar_sede(id_sede, nombre.strip(), distrito.strip()):
            messagebox.showinfo("Éxito", "Sede actualizada correctamente")
            ventana.destroy()
            self.cargar_sedes()
            self.sede_seleccionada = None
        else:
            messagebox.showerror("Error", "No se pudo actualizar la sede")

    def regresar_menu(self):
        """Regresar al menú principal"""
        respuesta = messagebox.askyesno("Confirmar salida",
                                        "¿Está seguro que desea regresar al menú principal?")
        if respuesta:
            self.root.quit()

    # Métodos para el scroll
    def on_frame_configure(self, event):
        """Actualizar scroll region cuando el frame cambia de tamaño"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Actualizar el tamaño del frame interno cuando el canvas cambia"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def on_mousewheel(self, event):
        """Manejar scroll con rueda del mouse"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def mostrar(self):
        """Mostrar la ventana"""
        self.root.mainloop()


# Ejecutar la aplicación
if __name__ == "__main__":
    app = GestionarSedes()
    app.mostrar()