import tkinter as tk
from tkinter import ttk, Tk, messagebox
from sistema_mega.modelo.estudiante_modelo import ver_notas
from sistema_mega.modelo.estudiante_modelo import ver_perfil
from sistema_mega.database.conexion_estudiante import ejecutar_procedimiento
from sistema_mega.modelo.estudiante_modelo import cambiar_contrasenia
from sistema_mega.vista.login import LoginVentana


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
        self.withdraw()
        ventana = GestionNotas(self.id_usuario, self.nombre_usuario)
        ventana.grab_set()
        # Cuando se cierre la nueva ventana, vuelve a mostrar la actual
        ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), self.deiconify()])
        # Aquí puedes agregar la lógica para mostrar los pagos

    def actualizar_contrasena(self):
        self.withdraw()
        ventana = GestionContrasena(self.id_usuario, self.nombre_usuario)
        ventana.grab_set()
        # Cuando se cierre la nueva ventana, vuelve a mostrar la actual
        ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), self.deiconify()])
        # Aquí puedes agregar la lógica para mostrar los pagos

    def ver_perfil(self):
        self.withdraw()
        ventana = GestionPerfil(self.id_usuario, self.nombre_usuario)
        ventana.grab_set()
        # Cuando se cierre la nueva ventana, vuelve a mostrar la actual
        ventana.protocol("WM_DELETE_WINDOW", lambda: [ventana.destroy(), self.deiconify()])
        # Aquí puedes agregar la lógica para mostrar los pagos


    def salir(self):
        from sistema_mega.vista.login import LoginVentana
        """Método para cerrar sesión y volver a login"""
        print("Cerrando sesión...")
        self.destroy()  # destruye solo la ventana actual

        login = LoginVentana()
        login.mainloop()

    def mostrar(self):
        """Mostrar la ventana"""
        self.mainloop()

# opciones a ingresar =====================================
class GestionContrasena(tk.Toplevel):
    def __init__(self, id_usuario, nombre_usuario, ventana_anterior=None):
        super().__init__()
        self.title("Actualizar Contraseña")
        self.geometry("500x350")
        self.configure(bg="#eaf6ff")

        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario
        self.ventana_anterior = ventana_anterior

        self.configurar_estilo()
        self.crear_widgets()

    def configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure("Titulo.TLabel",
                         background="#4a90e2",
                         foreground="white",
                         font=("Arial", 14, "bold"),
                         padding=10)

        estilo.configure("Etiqueta.TLabel",
                         background="#eaf6ff",
                         foreground="#004080",
                         font=("Arial", 11, "bold"))

        estilo.configure("Boton.TButton",
                         background="#4a90e2",
                         foreground="white",
                         font=("Arial", 12, "bold"))
        estilo.map("Boton.TButton",
                   background=[("active", "#6fb3f2")])

    def crear_widgets(self):
        ttk.Label(self,
                  text="Cambiar Contraseña",
                  style="Titulo.TLabel").pack(fill="x")

        formulario = ttk.Frame(self, style="frame.TFrame")
        formulario.pack(padx=30, pady=25, fill="both", expand=True)

        ttk.Label(formulario, text="Contraseña Actual:", style="Etiqueta.TLabel").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_actual = ttk.Entry(formulario, show="*")
        self.entry_actual.grid(row=0, column=1, pady=5)

        ttk.Label(formulario, text="Nueva Contraseña:", style="Etiqueta.TLabel").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_nueva = ttk.Entry(formulario, show="*")
        self.entry_nueva.grid(row=1, column=1, pady=5)

        ttk.Label(formulario, text="Repetir Nueva Contraseña:", style="Etiqueta.TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_repetir = ttk.Entry(formulario, show="*")
        self.entry_repetir.grid(row=2, column=1, pady=5)

        btn_actualizar = ttk.Button(formulario,
                                    text="Actualizar Contraseña",
                                    style="Boton.TButton",
                                    command=self.actualizar_contrasena)
        btn_actualizar.grid(row=3, column=0, columnspan=2, pady=20)

        formulario.columnconfigure(1, weight=1)

    def actualizar_contrasena(self):
        actual = self.entry_actual.get().strip()
        nueva = self.entry_nueva.get().strip()
        repetir = self.entry_repetir.get().strip()

        if not actual or not nueva or not repetir:
            self.mostrar_error("Por favor complete todos los campos.")
            return

        if nueva != repetir:
            self.mostrar_error("Las nuevas contraseñas no coinciden.")
            return

        try:
            mensaje = cambiar_contrasenia(self.id_usuario, actual, nueva)
            messagebox.showinfo("Éxito", mensaje)
            # self.destroy()
        except Exception as e:
            self.mostrar_error(str(e))

    def mostrar_error(self, mensaje):
        messagebox.showerror("Error", mensaje)


class GestionNotas(tk.Toplevel):
    def __init__(self, id_usuario, nombre_usuario):
        super().__init__()
        self.title("Notas del Estudiante")
        self.geometry("800x450")
        self.configure(bg="#eaf6ff")

        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario

        self.configurar_estilo()
        self.crear_widgets()

    def configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure("Encabezado.TLabel",
                         background="#4a90e2",
                         foreground="white",
                         font=("Arial", 14, "bold"),
                         padding=10)

        estilo.configure("Tabla.Treeview",
                         background="#ffffff",
                         foreground="#004080",
                         fieldbackground="#ffffff",
                         font=("Arial", 11))

        estilo.configure("Tabla.Treeview.Heading",
                         background="#4a90e2",
                         foreground="white",
                         font=("Arial", 12, "bold"))

    def crear_widgets(self):
        ttk.Label(self,
                  text=f"Notas de {self.nombre_usuario}",
                  style="Encabezado.TLabel").pack(fill="x")

        self.tabla = ttk.Treeview(self,
                                  columns=("Curso", "Ciclo", "Nota", "Fecha"),
                                  style="Tabla.Treeview",
                                  show="headings")

        self.tabla.heading("Curso", text="Curso")
        self.tabla.heading("Ciclo", text="Ciclo")
        self.tabla.heading("Nota", text="Nota")
        self.tabla.heading("Fecha", text="Fecha del Examen")

        self.tabla.column("Curso", width=200)
        self.tabla.column("Ciclo", width=150)
        self.tabla.column("Nota", width=100, anchor="center")
        self.tabla.column("Fecha", width=150, anchor="center")

        self.tabla.pack(padx=20, pady=20, fill="both", expand=True)

        self.cargar_datos()

    def cargar_datos(self):
        try:
            resultados = ver_notas(self.id_usuario)
            for fila in resultados:
                self.tabla.insert("", "end", values=fila)
        except Exception as e:
            print("Error al obtener notas:", e)

def actualizar_contrasena(self):
        """Método para actualizar contraseña"""
        print("Actualizar contraseña")
        # Aquí puedes agregar la lógica para actualizar la contraseña



class GestionPerfil(tk.Toplevel):
    def __init__(self, id_estudiante, nombre_usuario):
        super().__init__()
        self.title("Perfil del Estudiante")
        self.geometry("600x400")
        self.configure(bg="#eaf6ff")

        self.id_estudiante = id_estudiante
        self.nombre_usuario = nombre_usuario

        self.configurar_estilo()
        self.crear_widgets()

    def configurar_estilo(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure("Encabezado.TLabel",
                         background="#4a90e2",
                         foreground="white",
                         font=("Arial", 14, "bold"),
                         padding=10)

        estilo.configure("Etiqueta.TLabel",
                         background="#eaf6ff",
                         foreground="#004080",
                         font=("Arial", 11, "bold"))

        estilo.configure("Valor.TLabel",
                         background="#eaf6ff",
                         foreground="#000000",
                         font=("Arial", 11))

    def crear_widgets(self):
        ttk.Label(self,
                  text=f"Perfil de {self.nombre_usuario}",
                  style="Encabezado.TLabel").pack(fill="x")

        self.frame_info = ttk.Frame(self, style="frame.TFrame")
        self.frame_info.pack(padx=30, pady=20, fill="both", expand=True)

        self.cargar_datos()

    def cargar_datos(self):
        try:
            perfil = ver_perfil(self.id_estudiante)
            if perfil:
                datos = perfil[0]
                etiquetas = [
                    "Nombre de Usuario", "Correo", "Nombre Completo",
                    "Tipo de Documento", "Número de Documento",
                    "Área Académica", "Ciclo Inscrito"
                ]

                for etiqueta, valor in zip(etiquetas, datos):
                    fila = ttk.Frame(self.frame_info)
                    fila.pack(anchor="w", pady=5)

                    ttk.Label(fila, text=f"{etiqueta}: ", style="Etiqueta.TLabel").pack(side="left")
                    ttk.Label(fila, text=valor, style="Valor.TLabel").pack(side="left")

        except Exception as e:
            print("Error al obtener perfil:", e)

# Ejecutar la aplicación
if __name__ == "__main__":
    app = MenuEstudiante()
    app.mostrar()