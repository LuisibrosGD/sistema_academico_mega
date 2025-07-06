import tkinter as tk
from tkinter import ttk, Tk


class MenuEstudiante(tk.Toplevel):
    def __init__(self, id_usuario, nombre_usuario):
        super().__init__()
        self.title("Estudiante")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0")

        # Obtener id, y el nombre
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
        estilo.configure("frameEstudiante.TFrame",
                         background="#f0f0f0")

        # Estilo para el header
        estilo.configure("headerEstudiante.TFrame",
                         background="#4a90e2")

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
        self.frame_principal = ttk.Frame(self, style="frameEstudiante.TFrame")
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
        header_frame = ttk.Frame(self.frame_principal, style="headerEstudiante.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)

        # Configurar padding interno
        header_frame.configure(padding=(20, 15))

        # Título del menú
        titulo_label = ttk.Label(header_frame,
                                 text= f"Menú del Estudiante {self.nombre_usuario}",
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
        botones_frame = ttk.Frame(self.frame_principal, style="frameEstudiante.TFrame")
        botones_frame.grid(row=1, column=0, sticky="nsew")

        # Configurar grid para centrar los botones
        botones_frame.rowconfigure(0, weight=1)
        botones_frame.rowconfigure(1, weight=0)
        botones_frame.rowconfigure(2, weight=0)
        botones_frame.rowconfigure(3, weight=0)
        botones_frame.rowconfigure(4, weight=0)
        botones_frame.rowconfigure(5, weight=1)
        botones_frame.columnconfigure(0, weight=1)
        botones_frame.columnconfigure(1, weight=0)
        botones_frame.columnconfigure(2, weight=1)

        # Datos de los botones
        botones_info = [
            ("📄", "Ver pagos realizados", self.ver_pagos),
            ("📊", "Ver notas", self.ver_notas),
            ("🔒", "Actualizar contraseña", self.actualizar_contrasena),
            ("👤", "Ver perfil", self.ver_perfil)
        ]

        # Crear los botones
        for i, (icono, texto, comando) in enumerate(botones_info):
            self.crear_boton_menu(botones_frame, icono, texto, comando, i + 1)

    def crear_boton_menu(self, parent, icono, texto, comando, fila):
        """Crear un botón del menú con icono y texto"""
        # Frame para el botón
        boton_frame = ttk.Frame(parent, style="frameEstudiante.TFrame")
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

    # Métodos para los comandos de los botones
    def ver_pagos(self):
        from sistema_mega.vista.estudiante.GestionPagos import GestionPagos
        self.withdraw()  # Oculta esta ventana
        ventana = GestionPagos(self.id_usuario, self.nombre_usuario)
        ventana.grab_set()

        # Cuando se cierre la nueva ventana, vuelve a mostrar la actual
        ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), self.deiconify()])
        # Aquí puedes agregar la lógica para mostrar los pagos

    def ver_notas(self):
        """Método para ver notas"""
        print("Ver notas")
        # Aquí puedes agregar la lógica para mostrar las notas

    def actualizar_contrasena(self):
        """Método para actualizar contraseña"""
        print("Actualizar contraseña")
        # Aquí puedes agregar la lógica para actualizar la contraseña

    def ver_perfil(self):
        """Método para ver perfil"""
        print("Ver perfil")
        # Aquí puedes agregar la lógica para mostrar el perfil

    def salir(self):
        """Método para salir/cerrar sesión"""
        print("Cerrando sesión...")
        self.quit()

    def mostrar(self):
        """Mostrar la ventana"""
        self.mainloop()


# Ejecutar la aplicación
if __name__ == "__main__":
    app = MenuEstudiante()
    app.mostrar()