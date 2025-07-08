import tkinter as tk
from tkinter import ttk, messagebox
from sistema_mega.modelo.EspecialidadModelo import EspecialidadModelo
from sistema_mega.vista.administrador.ProfesorEspecialidadVista import ProfesorEspecialidadVista


class EspecialidadVista(tk.Toplevel):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.modelo = EspecialidadModelo()
        self.especialidades = []
        self.especialidad_seleccionada = None
        self.frame_especialidades = None
        self.configurar_ventana()
        self.crear_estilos()
        self.crear_widgets()
        self.cargar_especialidades()

    def configurar_ventana(self):
        self.title("Gestión de Especialidades")
        self.geometry("1000x700")
        self.configure(bg="#f5f5f5")

        # Hacer la ventana redimensionable
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def crear_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Estilo para el título
        estilo.configure(
            "etiquetaTitulo.TLabel",
            foreground="Gray",
            font=("Helvetica", 16, "bold"),
            background="#f5f5f5"
        )

        # Estilo para botones de especialidad (verde)
        estilo.configure(
            "botonEspecialidad.TButton",
            background="#4CAF50",
            foreground="white",
            font=("Arial", 12, "bold"),
            borderwidth=0,
            relief="flat"
        )
        estilo.map("botonEspecialidad.TButton",
                   background=[("pressed", "#45a049"), ("active", "#66bb6a")])

        # Estilo para botón seleccionado
        estilo.configure("botonSeleccionado.TButton",
                         background="#1B5E20",
                         foreground="white",
                         font=("Arial", 12, "bold"),
                         borderwidth=2,
                         relief="solid")

        # Estilo para botón agregar
        estilo.configure(
            "botonAgregar.TButton",
            background="#2196F3",
            foreground="white",
            font=("Arial", 14, "bold"),
            borderwidth=0,
            relief="flat"
        )
        estilo.map("botonAgregar.TButton",
                   background=[("pressed", "#1976D2"), ("active", "#42A5F5")])

        # Estilo para botón editar
        estilo.configure(
            "botonEditar.TButton",
            background="#FF9800",
            foreground="white",
            font=("Arial", 14, "bold"),
            borderwidth=0,
            relief="flat"
        )
        estilo.map("botonEditar.TButton",
                   background=[("pressed", "#F57C00"), ("active", "#FFB74D")])

        # Estilo para botón ver profesores
        estilo.configure(
            "botonVerProfesores.TButton",
            background="#9C27B0",
            foreground="white",
            font=("Arial", 14, "bold"),
            borderwidth=0,
            relief="flat"
        )
        estilo.map("botonVerProfesores.TButton",
                   background=[("pressed", "#7B1FA2"), ("active", "#BA68C8")])

        # Estilo para botón regresar
        estilo.configure(
            "botonRegresar.TButton",
            background="#9E9E9E",
            foreground="white",
            font=("Arial", 12, "bold"),
            borderwidth=0,
            relief="flat"
        )
        estilo.map("botonRegresar.TButton",
                   background=[("pressed", "#757575"), ("active", "#BDBDBD")])

    def crear_widgets(self):
        # Frame principal
        frame_principal = ttk.Frame(self)
        frame_principal.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Configurar el frame principal
        frame_principal.rowconfigure(1, weight=1)
        frame_principal.columnconfigure(0, weight=1)

        # Título
        titulo = ttk.Label(frame_principal, text="Especialidades Disponibles",
                           style="etiquetaTitulo.TLabel")
        titulo.grid(row=0, column=0, pady=(0, 20))

        # Frame para las especialidades con scrollbar
        frame_scroll = ttk.Frame(frame_principal)
        frame_scroll.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        frame_scroll.rowconfigure(0, weight=1)
        frame_scroll.columnconfigure(0, weight=1)

        # Canvas y scrollbar para especialidades
        canvas = tk.Canvas(frame_scroll, bg="#f5f5f5", highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame_scroll, orient="vertical", command=canvas.yview)
        self.frame_especialidades = ttk.Frame(canvas)

        # Configurar el canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Crear ventana en el canvas
        canvas_frame = canvas.create_window((0, 0), window=self.frame_especialidades, anchor="nw")

        # Función para configurar scroll
        def configurar_scroll(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
            # Ajustar el ancho del frame interno al canvas
            canvas.itemconfig(canvas_frame, width=event.width)

        self.frame_especialidades.bind("<Configure>", configurar_scroll)
        canvas.bind("<Configure>", configurar_scroll)

        # Frame para botones de acción
        frame_botones = ttk.Frame(frame_principal)
        frame_botones.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        frame_botones.columnconfigure(0, weight=1)
        frame_botones.columnconfigure(1, weight=1)
        frame_botones.columnconfigure(2, weight=1)

        # Botones de acción
        btn_agregar = ttk.Button(frame_botones, text="+ Crear especialidad",
                                 command=self.agregar_especialidad,
                                 style="botonAgregar.TButton")
        btn_agregar.grid(row=0, column=0, padx=(0, 5), pady=10, sticky="ew")

        btn_editar = ttk.Button(frame_botones, text="Editar especialidad",
                                command=self.editar_especialidad,
                                style="botonEditar.TButton")
        btn_editar.grid(row=0, column=1, padx=(5, 5), pady=10, sticky="ew")

        btn_ver_profesores = ttk.Button(frame_botones, text="Ver profesores",
                                        command=self.ver_profesores,
                                        style="botonVerProfesores.TButton")
        btn_ver_profesores.grid(row=0, column=2, padx=(5, 0), pady=10, sticky="ew")

        # Botón regresar
        btn_regresar = ttk.Button(frame_principal, text="Regresar a Menu principal",
                                  command=self.regresar_menu,
                                  style="botonRegresar.TButton")
        btn_regresar.grid(row=3, column=0, pady=10, sticky="w")

    def cargar_especialidades(self):
        """Carga todas las especialidades desde la base de datos"""
        # Limpiar frame de especialidades
        for widget in self.frame_especialidades.winfo_children():
            widget.destroy()

        # Obtener especialidades del modelo
        self.especialidades = self.modelo.obtener_todas_especialidades()

        # Crear botones para cada especialidad
        for i, (id_especialidad, nombre) in enumerate(self.especialidades):
            btn = ttk.Button(self.frame_especialidades, text=nombre,
                             command=lambda id_esp=id_especialidad: self.seleccionar_especialidad(id_esp),
                             style="botonEspecialidad.TButton")
            btn.grid(row=i // 5, column=i % 5, padx=5, pady=5, sticky="ew", ipadx=10, ipady=5)

        # Configurar columnas para que sean redimensionables
        for i in range(5):
            self.frame_especialidades.columnconfigure(i, weight=1)

    def seleccionar_especialidad(self, id_especialidad):
        """Selecciona una especialidad"""
        self.especialidad_seleccionada = id_especialidad

        # Actualizar estilos de botones para mostrar selección
        for widget in self.frame_especialidades.winfo_children():
            if isinstance(widget, ttk.Button):
                widget.configure(style="botonEspecialidad.TButton")

        # Destacar botón seleccionado
        for i, (id_esp, nombre) in enumerate(self.especialidades):
            if id_esp == id_especialidad:
                # Aplicar estilo al botón seleccionado
                widgets = self.frame_especialidades.winfo_children()
                if i < len(widgets):
                    widgets[i].configure(style="botonSeleccionado.TButton")
                break

    def agregar_especialidad(self):
        """Muestra ventana para agregar nueva especialidad"""
        self.mostrar_formulario_especialidad("Agregar")

    def editar_especialidad(self):
        """Muestra ventana para editar especialidad seleccionada"""
        if not self.especialidad_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor seleccione una especialidad para editar.")
            return

        self.mostrar_formulario_especialidad("Editar")

    def ver_profesores(self):
        """Muestra ventana con los profesores de la especialidad seleccionada"""
        if not self.especialidad_seleccionada:
            messagebox.showwarning("Advertencia", "Por favor seleccione una especialidad para ver los profesores.")
            return

        # Obtener el nombre de la especialidad seleccionada
        nombre_especialidad = None
        for id_esp, nombre in self.especialidades:
            if id_esp == self.especialidad_seleccionada:
                nombre_especialidad = nombre
                break

        # Abrir ventana de profesores por especialidad
        ventana_profesores = ProfesorEspecialidadVista(self, self.especialidad_seleccionada, nombre_especialidad)

    def mostrar_formulario_especialidad(self, modo):
        """Muestra formulario para agregar o editar especialidad"""
        ventana_form = tk.Toplevel(self)
        ventana_form.title(f"{modo} Especialidad")
        ventana_form.geometry("400x200")
        ventana_form.configure(bg="#f5f5f5")

        # Centrar la ventana
        ventana_form.transient(self)
        ventana_form.grab_set()

        # Frame principal del formulario
        frame_form = ttk.Frame(ventana_form)
        frame_form.pack(expand=True, fill="both", padx=20, pady=20)

        # Título
        titulo = ttk.Label(frame_form, text=f"{modo} Especialidad",
                           style="etiquetaTitulo.TLabel")
        titulo.pack(pady=(0, 20))

        # Campo de entrada
        ttk.Label(frame_form, text="Nombre de la especialidad:").pack(anchor="w", pady=(0, 5))
        entrada_nombre = ttk.Entry(frame_form, font=("Arial", 12), width=30)
        entrada_nombre.pack(pady=(0, 20))

        # Si es edición, cargar datos actuales
        if modo == "Editar" and self.especialidad_seleccionada:
            especialidad_actual = self.modelo.obtener_especialidad_por_id(self.especialidad_seleccionada)
            if especialidad_actual:
                entrada_nombre.insert(0, especialidad_actual[1])

        # Función para guardar
        def guardar():
            nombre = entrada_nombre.get().strip()

            if not nombre:
                messagebox.showerror("Error", "El nombre de la especialidad no puede estar vacío.")
                return

            if modo == "Agregar":
                # Verificar si ya existe
                if self.modelo.existe_especialidad(nombre):
                    messagebox.showerror("Error", "Ya existe una especialidad con ese nombre.")
                    return

                if self.modelo.agregar_especialidad(nombre):
                    messagebox.showinfo("Éxito", "Especialidad agregada correctamente.")
                    ventana_form.destroy()
                    self.cargar_especialidades()
                else:
                    messagebox.showerror("Error", "No se pudo agregar la especialidad.")

            elif modo == "Editar":
                # Verificar si el nuevo nombre ya existe (excepto para la misma especialidad)
                especialidad_actual = self.modelo.obtener_especialidad_por_id(self.especialidad_seleccionada)
                if especialidad_actual and nombre != especialidad_actual[1]:
                    if self.modelo.existe_especialidad(nombre):
                        messagebox.showerror("Error", "Ya existe una especialidad con ese nombre.")
                        return

                if self.modelo.editar_especialidad(self.especialidad_seleccionada, nombre):
                    messagebox.showinfo("Éxito", "Especialidad editada correctamente.")
                    ventana_form.destroy()
                    self.cargar_especialidades()
                    self.especialidad_seleccionada = None
                else:
                    messagebox.showerror("Error", "No se pudo editar la especialidad.")

        # Botones
        frame_botones = ttk.Frame(frame_form)
        frame_botones.pack(pady=10)

        ttk.Button(frame_botones, text="Guardar", command=guardar,
                   style="botonAgregar.TButton").pack(side="left", padx=(0, 10))
        ttk.Button(frame_botones, text="Cancelar", command=ventana_form.destroy,
                   style="botonRegresar.TButton").pack(side="left")

    def regresar_menu(self):
        """Cierra la ventana y regresa al menú principal"""
        self.destroy()
        self.master.deiconify()



# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    app = EspecialidadVista(root)
    app.mainloop()