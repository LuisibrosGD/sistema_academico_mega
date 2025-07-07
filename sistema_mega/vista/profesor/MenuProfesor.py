import tkinter as tk
from tkinter import ttk
from sistema_mega.modelo.profesor_modelo import *


class MenuProfesor(tk.Toplevel):
    def __init__(self, master, id_usuario, nombre_usuario):  # Cambio 1: Agregar master
        super().__init__(master)  # Cambio 2: Pasar master al padre
        self.title("Profesor")
        self.geometry("1000x700")
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
        ventana.geometry("1200x600")

        # Frame principal
        frame = ttk.Frame(ventana)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Tabla
        columnas = ("ciclo", "modalidad", "curso", "dia", "hora_inicio", "hora_fin", "grupo")
        tabla = ttk.Treeview(frame, columns=columnas, show="headings")

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
        ttk.Button(
            frame,
            text="Regresar",
            command=lambda: [ventana.destroy(), self.deiconify()]
        ).pack(pady=10)

        ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), self.deiconify()])

    def ver_asistencias(self):
        """Método para ver asistencias"""
        self.withdraw()
        ventana = tk.Toplevel(self)
        ventana.title("Ver Asistencias")
        ventana.geometry("1200x600")

        # Frame principal
        frame = ttk.Frame(ventana)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Filtros
        filtros_frame = ttk.Frame(frame)
        filtros_frame.pack(fill="x", pady=(0, 20))

        ttk.Label(filtros_frame, text="Fecha Inicio:").pack(side="left")
        entry_inicio = ttk.Entry(filtros_frame)
        entry_inicio.pack(side="left", padx=5)

        ttk.Label(filtros_frame, text="Fecha Fin:").pack(side="left")
        entry_fin = ttk.Entry(filtros_frame)
        entry_fin.pack(side="left", padx=5)

        # Tabla
        columnas = ("ciclo", "modalidad", "grupo", "curso", "fecha", "estado")
        tabla = ttk.Treeview(frame, columns=columnas, show="headings")

        for col in columnas:
            tabla.heading(col, text=col.replace("_", " ").title())
            tabla.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)

        tabla.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Función para cargar datos
        def buscar():
            tabla.delete(*tabla.get_children())

            inicio = entry_inicio.get()
            fin = entry_fin.get()

            # Validación adicional
            try:
                asistencias = obtener_asistencias(self.id_usuario, inicio, fin)

                if not asistencias:
                    print("No se encontraron asistencias")  # Mensaje de depuración
                else:
                    for asist in asistencias:
                        tabla.insert("", "end", values=asist)
            except Exception as e:
                print(f"Error al cargar asistencias: {str(e)}")  # Debug
                # Opcional: mostrar mensaje al usuario

        # Botón buscar
        ttk.Button(filtros_frame, text="Buscar", command=buscar).pack(side="left", padx=10)

        # Botón regresar
        ttk.Button(
            frame,
            text="Regresar",
            command=lambda: [ventana.destroy(), self.deiconify()]
        ).pack(pady=10)

        # ✅ Cargar asistencias automáticamente al abrir la ventana
        buscar()

        # Cerrar ventana
        ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), self.deiconify()])

    def salir(self):
        """Método para salir/cerrar sesión"""
        print("Cerrando sesión...")
        self.destroy()
        self.master.deiconify()  # Cambio 6: Mostrar ventana padre al salir

    def mostrar(self):
        """Mostrar la ventana"""
        self.mainloop()