import tkinter as tk
from tkinter import ttk, messagebox
from sistema_mega.modelo.ProfesorEspecialidadModelo import ProfesorEspecialidadModelo


class ProfesorEspecialidadVista(tk.Toplevel):
    def __init__(self, parent, id_especialidad, nombre_especialidad):
        super().__init__()
        self.parent = parent
        self.id_especialidad = id_especialidad
        self.nombre_especialidad = nombre_especialidad
        self.modelo = ProfesorEspecialidadModelo()
        self.profesores = []
        self.configurar_ventana()
        self.crear_estilos()
        self.crear_widgets()
        self.cargar_profesores()

    def configurar_ventana(self):
        self.title(f"Profesores - {self.nombre_especialidad}")
        self.geometry("900x600")
        self.configure(bg="#f5f5f5")

        # Hacer la ventana redimensionable
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Centrar la ventana
        self.transient(self.parent)
        self.grab_set()

    def crear_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Estilo para el título
        estilo.configure(
            "etiquetaTitulo.TLabel",
            foreground="#2E7D32",
            font=("Helvetica", 16, "bold"),
            background="#f5f5f5"
        )

        # Estilo para subtítulos
        estilo.configure(
            "etiquetaSubtitulo.TLabel",
            foreground="#1976D2",
            font=("Helvetica", 12, "bold"),
            background="#f5f5f5"
        )

        # Estilo para texto normal
        estilo.configure(
            "etiquetaTexto.TLabel",
            foreground="#424242",
            font=("Arial", 10),
            background="#f5f5f5"
        )

        # Estilo para botón cerrar
        estilo.configure(
            "botonCerrar.TButton",
            background="#9E9E9E",
            foreground="white",
            font=("Arial", 12, "bold"),
            borderwidth=0,
            relief="flat"
        )
        estilo.map("botonCerrar.TButton",
                   background=[("pressed", "#757575"), ("active", "#BDBDBD")])

        # Estilo para el frame de profesores
        estilo.configure(
            "frameProfesor.TFrame",
            background="white",
            relief="solid",
            borderwidth=1
        )

        # Estilo para Treeview
        estilo.configure("Treeview",
                         background="white",
                         foreground="#424242",
                         fieldbackground="white",
                         font=("Arial", 10))
        estilo.configure("Treeview.Heading",
                         background="#E3F2FD",
                         foreground="#1976D2",
                         font=("Arial", 10, "bold"))

    def crear_widgets(self):
        # Frame principal
        frame_principal = ttk.Frame(self)
        frame_principal.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Configurar el frame principal
        frame_principal.rowconfigure(1, weight=1)
        frame_principal.columnconfigure(0, weight=1)

        # Título
        titulo = ttk.Label(frame_principal,
                           text=f"Profesores con especialidad en {self.nombre_especialidad}",
                           style="etiquetaTitulo.TLabel")
        titulo.grid(row=0, column=0, pady=(0, 20))

        # Frame para la tabla con scrollbar
        frame_tabla = ttk.Frame(frame_principal)
        frame_tabla.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        frame_tabla.rowconfigure(0, weight=1)
        frame_tabla.columnconfigure(0, weight=1)

        # Crear Treeview para mostrar profesores
        self.tree = ttk.Treeview(frame_tabla, columns=("nombre", "apellidos", "documento", "correo", "estado"),
                                 show="headings", height=15)

        # Configurar columnas
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellidos", text="Apellidos")
        self.tree.heading("documento", text="Documento")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("estado", text="Estado")

        # Configurar anchos de columnas
        self.tree.column("nombre", width=120, anchor="w")
        self.tree.column("apellidos", width=180, anchor="w")
        self.tree.column("documento", width=120, anchor="w")
        self.tree.column("correo", width=200, anchor="w")
        self.tree.column("estado", width=80, anchor="center")

        # Scrollbar para la tabla
        scrollbar_tabla = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_tabla.set)

        # Posicionar tabla y scrollbar
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar_tabla.grid(row=0, column=1, sticky="ns")

        # Frame para información adicional
        frame_info = ttk.Frame(frame_principal)
        frame_info.grid(row=2, column=0, sticky="ew", pady=(0, 20))

        # Etiqueta para mostrar total de profesores
        self.lbl_total = ttk.Label(frame_info, text="", style="etiquetaSubtitulo.TLabel")
        self.lbl_total.pack(anchor="w")

        # Botón cerrar
        btn_cerrar = ttk.Button(frame_principal, text="Cerrar",
                                command=self.cerrar_ventana,
                                style="botonCerrar.TButton")
        btn_cerrar.grid(row=3, column=0, pady=10, sticky="w")

    def cargar_profesores(self):
        """Carga los profesores con la especialidad seleccionada"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener profesores del modelo
        self.profesores = self.modelo.obtener_profesores_por_especialidad(self.id_especialidad)

        # Llenar tabla
        for profesor in self.profesores:
            id_profesor, nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, correo, estado = profesor

            # Formatear apellidos
            apellidos = f"{ap_paterno} {ap_materno}"

            # Formatear documento
            documento = f"{tipo_documento.upper()}: {nro_documento}"

            # Formatear estado
            estado_texto = "Activo" if estado else "Inactivo"

            # Insertar en la tabla
            self.tree.insert("", "end", values=(nombre, apellidos, documento, correo, estado_texto))

        # Actualizar información total
        total_profesores = len(self.profesores)
        self.lbl_total.config(text=f"Total de profesores: {total_profesores}")

        # Mostrar mensaje si no hay profesores
        if total_profesores == 0:
            self.tree.insert("", "end", values=("No hay profesores", "registrados con esta", "especialidad", "", ""))

    def cerrar_ventana(self):
        """Cierra la ventana"""
        self.destroy()


# Ejemplo de uso
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal

    # Simular parámetros (en uso real vendrían de la selección)
    id_especialidad = 1
    nombre_especialidad = "Matemáticas"

    app = ProfesorEspecialidadVista(root, id_especialidad, nombre_especialidad)
    app.mainloop()