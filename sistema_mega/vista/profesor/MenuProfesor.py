import tkinter as tk
from tkinter import ttk
from sistema_mega.modelo.profesor_modelo import *


class MenuProfesor(tk.Toplevel):
    def __init__(self, master, id_usuario, nombre_usuario):  # Cambio 1: Agregar master
        super().__init__(master)  # Cambio 2: Pasar master al padre
        self.title("Profesor")
        self.geometry("1400x700")
        self.configure(bg="#f0f0f0")

        self.master = master  # Cambio 3: Guardar referencia al padre
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario

        # Configurar el grid principal
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.configurar_estilos()
        self.crear_widgets()

    def configurar_estilos(self):
        """Configurar los estilos de la interfaz"""
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Estilo para el frame principal
        estilo.configure("frameProfesor.TFrame", background="#f0f0f0")

        # Estilo para el header
        estilo.configure("headerProfesor.TFrame", background="#4a90e2")

        # Estilo para el título del header
        estilo.configure("tituloHeader.TLabel",
                         background="#4a90e2",
                         foreground="white",
                         font=("Arial", 16, "bold"))

        # Estilo para el botón de salir
        estilo.configure("botonSalir.TButton",
                         background="#ff6b6b",
                         foreground="white",
                         font=("Arial", 12, "bold"),
                         borderwidth=0,
                         relief="flat")
        estilo.map("botonSalir.TButton",
                   background=[("pressed", "#e74c3c"), ("active", "#ff8080")])

        # Estilo para los botones del menú
        estilo.configure("botonMenu.TButton",
                         background="white",
                         foreground="#333333",
                         font=("Arial", 14),
                         borderwidth=1,
                         relief="solid",
                         padding=(20, 15))
        estilo.map("botonMenu.TButton",
                   background=[("pressed", "#e0e0e0"), ("active", "#f5f5f5")])

        # Estilo para los iconos de los botones
        estilo.configure("iconoBoton.TLabel",
                         background="white",
                         foreground="#4a90e2",
                         font=("Arial", 20))

    def crear_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        self.frame_principal = ttk.Frame(self, style="frameProfesor.TFrame")
        self.frame_principal.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Configurar grid del frame principal
        self.frame_principal.rowconfigure(1, weight=1)
        self.frame_principal.columnconfigure(0, weight=1)

        # Crear header
        self.crear_header()

        # Crear área de botones
        self.crear_area_botones()

    def crear_header(self):
        """Crear el header con título y botón de salir"""
        header_frame = ttk.Frame(self.frame_principal, style="headerProfesor.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)

        # Configurar padding interno
        header_frame.configure(padding=(20, 15))

        # Título del menú
        titulo_label = ttk.Label(header_frame,
                                 text=f"Menú del Profesor {self.nombre_usuario}",
                                 style="tituloHeader.TLabel")
        titulo_label.grid(row=0, column=0, sticky="w")

        # Botón de salir
        boton_salir = ttk.Button(header_frame,
                                 text="Salir",
                                 style="botonSalir.TButton",
                                 command=self.salir)
        boton_salir.grid(row=0, column=1, sticky="e", padx=(10, 0))

    def crear_area_botones(self):
        """Crear el área con los botones del menú"""
        # Frame contenedor para los botones
        botones_frame = ttk.Frame(self.frame_principal, style="frameProfesor.TFrame")
        botones_frame.grid(row=1, column=0, sticky="nsew")

        # Configurar grid para centrar los botones
        botones_frame.rowconfigure(0, weight=1)
        botones_frame.rowconfigure(1, weight=0)
        botones_frame.rowconfigure(2, weight=0)
        botones_frame.rowconfigure(3, weight=1)
        botones_frame.columnconfigure(0, weight=1)
        botones_frame.columnconfigure(1, weight=0)
        botones_frame.columnconfigure(2, weight=1)

        # Datos de los botones
        botones_info = [
            ("👥", "Ver grupos asignados", self.ver_grupos),
            ("📋", "Ver asistencias", self.ver_asistencias)
        ]

        # Crear los botones
        for i, (icono, texto, comando) in enumerate(botones_info):
            self.crear_boton_menu(botones_frame, icono, texto, comando, i + 1)

    def crear_boton_menu(self, parent, icono, texto, comando, fila):
        """Crear un botón del menú con icono y texto"""
        # Frame para el botón
        boton_frame = ttk.Frame(parent, style="frameProfesor.TFrame")
        boton_frame.grid(row=fila, column=1, sticky="ew", pady=10)
        boton_frame.configure(padding=(0, 0))

        # Configurar el ancho del botón
        boton_frame.columnconfigure(0, weight=1)

        # Botón principal
        boton = ttk.Button(boton_frame,
                           text=f"{icono}  {texto}",
                           style="botonMenu.TButton",
                           command=comando,
                           width=25)
        boton.grid(row=0, column=0, sticky="ew")

    def ver_grupos(self):
        """Método para ver grupos asignados"""
        self.withdraw()
        ventana = tk.Toplevel(self)  # Cambio 4: Pasar self como master
        ventana.title("Grupos Asignados")
        ventana.geometry("1800x600")
        ventana.configure(bg="#f0f0f0")

        # Frame principal
        frame = ttk.Frame(ventana, style="frameProfesor.TFrame")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ttk.Frame(frame, style="headerProfesor.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))

        titulo_label = ttk.Label(header_frame,
                                 text="Grupos Asignados",
                                 style="tituloHeader.TLabel")
        titulo_label.pack(side="left")

        # Tabla
        columnas = ("ciclo", "modalidad", "curso", "dia", "hora_inicio", "hora_fin", "grupo")
        tabla = ttk.Treeview(frame, columns=columnas, show="headings", style="Custom.Treeview")

        # Configurar columnas
        for col in columnas:
            tabla.heading(col, text=col.replace("_", " ").title())
            tabla.column(col, width=120, anchor="center")

        # Cargar datos
        grupos = obtener_grupos_asignados(self.id_usuario)
        for grupo in grupos:
            tabla.insert("", "end", values=grupo)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)

        tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Botón de regreso
        btn_frame = ttk.Frame(frame, style="frameProfesor.TFrame")
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Regresar",
            style="botonMenu.TButton",
            command=lambda: [ventana.destroy(), self.deiconify()]
        ).pack()

        ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), self.deiconify()])

    def ver_asistencias(self):
        self.withdraw()
        ventana = tk.Toplevel(self)
        ventana.title("Ver Asistencias")
        ventana.geometry("1400x600")
        ventana.configure(bg="#f0f0f0")

        frame = ttk.Frame(ventana, style="frameProfesor.TFrame")
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Header
        header_frame = ttk.Frame(frame, style="headerProfesor.TFrame")
        header_frame.pack(fill="x", pady=(0, 20))
        # Filtro por fecha
        filtro_frame = ttk.Frame(frame, style="frameProfesor.TFrame")
        filtro_frame.pack(pady=10)

        titulo_label = ttk.Label(header_frame,
                                 text="Registro de Asistencias",
                                 style="tituloHeader.TLabel")
        titulo_label.pack(side="left")

        columnas = ("ciclo", "modalidad", "grupo", "curso", "fecha", "estado")
        tabla = ttk.Treeview(frame, columns=columnas, show="headings", style="Custom.Treeview")

        for col in columnas:
            tabla.heading(col, text=col.replace("_", " ").title())
            tabla.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)
        tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")



        ttk.Label(filtro_frame, text="Desde:", style="tituloHeader.TLabel").grid(row=0, column=0, padx=5)
        entry_fecha_inicio = DateEntry(
            filtro_frame,
            width=12,
            date_pattern="dd/mm/yyyy",
            background="#4a90e2",
            foreground="white",
            bordercolor="#4a90e2",
            headersbackground="#4a90e2",
            normalbackground="#f0f0f0",
            weekendbackground="#f0f0f0"
        )
        entry_fecha_inicio.grid(row=0, column=1, padx=5)

        ttk.Label(filtro_frame, text="Hasta:", style="tituloHeader.TLabel").grid(row=0, column=2, padx=5)
        entry_fecha_fin = DateEntry(
            filtro_frame,
            width=12,
            date_pattern="dd/mm/yyyy",
            background="#4a90e2",
            foreground="white",
            bordercolor="#4a90e2",
            headersbackground="#4a90e2",
            normalbackground="#f0f0f0",
            weekendbackground="#f0f0f0"
        )
        entry_fecha_fin.grid(row=0, column=3, padx=5)

        # Función para cargar datos
        def buscar(fecha_inicio=None, fecha_fin=None):
            tabla.delete(*tabla.get_children())

            try:
                asistencias = obtener_asistencias(self.id_usuario)

                if fecha_inicio and fecha_fin:
                    fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
                    fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")

                    asistencias = [
                        fila for fila in asistencias
                        if fecha_inicio_dt <= datetime.strptime(fila[4][:10], "%Y-%m-%d") <= fecha_fin_dt
                    ]

                if not asistencias:
                    messagebox.showinfo("Información", "No se encontraron registros de asistencia")
                else:
                    for asist in asistencias:
                        fila_modificada = list(asist)
                        fila_modificada[4] = fila_modificada[4][:10]
                        tabla.insert("", "end", values=fila_modificada)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron cargar las asistencias: {str(e)}")
                print("Error completo:", traceback.format_exc())

        # Botón para aplicar filtro
        def aplicar_filtro():
            fecha_ini = entry_fecha_inicio.get_date().strftime("%Y-%m-%d")
            fecha_fin = entry_fecha_fin.get_date().strftime("%Y-%m-%d")
            buscar(fecha_ini, fecha_fin)

        ttk.Button(
            filtro_frame,
            text="Filtrar por Fecha",
            style="botonMenu.TButton",
            command=aplicar_filtro
        ).grid(row=0, column=4, padx=10)

        # Botón regresar
        btn_frame = ttk.Frame(frame, style="frameProfesor.TFrame")
        btn_frame.pack(pady=10)

        ttk.Button(
            btn_frame,
            text="Regresar",
            style="botonMenu.TButton",
            command=lambda: [ventana.destroy(), self.deiconify()]
        ).pack()

        buscar()  # Mostrar todas las asistencias al inicio
        ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), self.deiconify()])

    def salir(self):
        """Método para salir/cerrar sesión"""
        print("Cerrando sesión...")
        self.destroy()
        self.master.deiconify()  # Cambio 6: Mostrar ventana padre al salir

    def mostrar(self):
        """Mostrar la ventana"""
        self.mainloop()