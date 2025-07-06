import tkinter as tk
from tkinter import ttk, messagebox
from sistema_mega.modelo.pagoses_modelo import obtener_pagos_estudiante, obtener_total_pagado_estudiante, \
    obtener_datos_estudiante


class GestionPagos(tk.Toplevel):
    def __init__(self, id_usuario, nombre_usuario):
        super().__init__()
        # Obteniendo datos de Menu Estudiante
        self.id_usuario = id_usuario
        self.nombre_usuario = nombre_usuario

        self.title("Gestión de Pagos")
        self.geometry("900x600")
        self.configure(bg="#f0f0f0")

        # Configurar el grid principal
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Datos del estudiante
        self.datos_estudiante = None
        self.pagos_data = []

        self.configurar_estilos()
        self.cargar_datos()
        self.crear_widgets()

    def configurar_estilos(self):
        """Configurar los estilos de la interfaz"""
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Estilo para el frame principal
        estilo.configure("framePagos.TFrame",
                         background="#f0f0f0")

        # Estilo para el header
        estilo.configure("headerPagos.TFrame",
                         background="#4a90e2")

        # Estilo para el título del header
        estilo.configure("tituloPagos.TLabel",
                         background="#4a90e2",
                         foreground="white",
                         font=("Arial", 16, "bold"))

        # Estilo para el botón de regresar
        estilo.configure("botonRegresar.TButton",
                         background="#6c757d",
                         foreground="white",
                         font=("Arial", 12, "bold"),
                         borderwidth=0,
                         relief="flat")
        estilo.map("botonRegresar.TButton",
                   background=[("pressed", "#5a6268"), ("active", "#868e96")])

        # Estilo para el treeview
        estilo.configure("Treeview",
                         background="white",
                         foreground="black",
                         fieldbackground="white",
                         font=("Arial", 10))

        estilo.configure("Treeview.Heading",
                         background="#4a90e2",
                         foreground="white",
                         font=("Arial", 11, "bold"))

        # Estilo para labels de información
        estilo.configure("info.TLabel",
                         background="#f0f0f0",
                         foreground="#333333",
                         font=("Arial", 11))

        # Estilo para labels de total
        estilo.configure("total.TLabel",
                         background="#f0f0f0",
                         foreground="#28a745",
                         font=("Arial", 12, "bold"))

    def cargar_datos(self):
        """Cargar los datos del estudiante y sus pagos"""
        try:
            # Obtener datos del estudiante
            self.datos_estudiante = obtener_datos_estudiante(self.id_usuario)

            # Obtener pagos del estudiante
            self.pagos_data = obtener_pagos_estudiante(self.id_usuario)

            # Obtener total pagado
            self.total_pagado = obtener_total_pagado_estudiante(self.id_usuario)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar los datos: {str(e)}")
            self.pagos_data = []
            self.total_pagado = 0

    def crear_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        self.frame_principal = ttk.Frame(self, style="framePagos.TFrame")
        self.frame_principal.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Configurar grid del frame principal
        self.frame_principal.rowconfigure(2, weight=1)
        self.frame_principal.columnconfigure(0, weight=1)

        # Crear header
        self.crear_header()

        # Crear información del estudiante
        self.crear_info_estudiante()

        # Crear tabla de pagos
        self.crear_tabla_pagos()

        # Crear resumen
        self.crear_resumen()

        # Crear botón regresar
        self.crear_boton_regresar()

    def crear_header(self):
        """Crear el header con título"""
        header_frame = ttk.Frame(self.frame_principal, style="headerPagos.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)
        header_frame.configure(padding=(20, 15))

        # Título
        titulo_label = ttk.Label(header_frame,
                                 text="Gestión de Pagos",
                                 style="tituloPagos.TLabel")
        titulo_label.grid(row=0, column=0, sticky="w")

    def crear_info_estudiante(self):
        """Crear la sección de información del estudiante"""
        info_frame = ttk.LabelFrame(self.frame_principal, text="Información del Estudiante", padding=(10, 10))
        info_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        info_frame.columnconfigure(1, weight=1)
        info_frame.columnconfigure(3, weight=1)

        if self.datos_estudiante:
            nombre_completo = f"{self.datos_estudiante[0]} {self.datos_estudiante[1]} {self.datos_estudiante[2]}"

            # Nombre
            ttk.Label(info_frame, text="Nombre:", style="info.TLabel").grid(row=0, column=0, sticky="w", padx=(0, 10))
            ttk.Label(info_frame, text=nombre_completo, style="info.TLabel").grid(row=0, column=1, sticky="w")

            # Documento
            ttk.Label(info_frame, text="Documento:", style="info.TLabel").grid(row=0, column=2, sticky="w",
                                                                               padx=(20, 10))
            ttk.Label(info_frame, text=self.datos_estudiante[3], style="info.TLabel").grid(row=0, column=3, sticky="w")

            # Área Académica
            ttk.Label(info_frame, text="Área Académica:", style="info.TLabel").grid(row=1, column=0, sticky="w",
                                                                                    padx=(0, 10))
            ttk.Label(info_frame, text=self.datos_estudiante[4].upper(), style="info.TLabel").grid(row=1, column=1,
                                                                                                   sticky="w")

    def crear_tabla_pagos(self):
        """Crear la tabla de pagos"""
        # Frame para la tabla
        tabla_frame = ttk.LabelFrame(self.frame_principal, text="Pagos Realizados", padding=(10, 10))
        tabla_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        tabla_frame.rowconfigure(0, weight=1)
        tabla_frame.columnconfigure(0, weight=1)

        # Crear treeview
        columnas = ("Ciclo", "Modalidad", "Monto", "Fecha Pago", "Fecha Inicio", "Fecha Fin", "Estado")
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10)

        # Configurar encabezados
        encabezados = {
            "Ciclo": 180,
            "Modalidad": 100,
            "Monto": 100,
            "Fecha Pago": 120,
            "Fecha Inicio": 120,
            "Fecha Fin": 120,
            "Estado": 100
        }

        for col, ancho in encabezados.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, width=ancho, anchor="center")

        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Grid
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Llenar la tabla
        self.llenar_tabla()

    def llenar_tabla(self):
        """Llenar la tabla con los datos de pagos"""
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Agregar datos
        for pago in self.pagos_data:
            # Formatear los datos
            nombre_ciclo = pago[0]
            modalidad = pago[1]
            monto = f"S/. {pago[2]:.2f}"
            fecha_pago = pago[3].strftime("%Y-%m-%d") if pago[3] else "N/A"
            fecha_inicio = pago[4].strftime("%Y-%m-%d") if pago[4] else "N/A"
            fecha_fin = pago[5].strftime("%Y-%m-%d") if pago[5] else "N/A"
            estado = pago[6].capitalize() if pago[6] else "N/A"

            self.tree.insert("", "end", values=(
                nombre_ciclo, modalidad, monto, fecha_pago,
                fecha_inicio, fecha_fin, estado
            ))

    def crear_resumen(self):
        """Crear el resumen de pagos"""
        resumen_frame = ttk.LabelFrame(self.frame_principal, text="Resumen", padding=(10, 10))
        resumen_frame.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        resumen_frame.columnconfigure(1, weight=1)

        # Total de pagos
        ttk.Label(resumen_frame, text="Total de Pagos:", style="info.TLabel").grid(row=0, column=0, sticky="w",
                                                                                   padx=(0, 10))
        ttk.Label(resumen_frame, text=str(len(self.pagos_data)), style="info.TLabel").grid(row=0, column=1, sticky="w")

        # Monto total pagado
        ttk.Label(resumen_frame, text="Monto Total Pagado:", style="info.TLabel").grid(row=1, column=0, sticky="w",
                                                                                       padx=(0, 10))
        ttk.Label(resumen_frame, text=f"S/. {self.total_pagado:.2f}", style="total.TLabel").grid(row=1, column=1,
                                                                                                 sticky="w")

    def crear_boton_regresar(self):
        """Crear el botón para regresar al menú principal"""
        boton_frame = ttk.Frame(self.frame_principal, style="framePagos.TFrame")
        boton_frame.grid(row=4, column=0, sticky="ew")
        boton_frame.columnconfigure(0, weight=1)

        boton_regresar = ttk.Button(boton_frame,
                                    text="Regresar al Menú Principal",
                                    style="botonRegresar.TButton",
                                    command=self.volver_menu)
        boton_regresar.grid(row=0, column=0, pady=10)
    def volver_menu(self):
        from sistema_mega.vista.estudiante.MenuEstudiante import MenuEstudiante
        self.destroy()
        MenuEstudiante(self.id_usuario, self.nombre_usuario)


    # Para pruebas
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Ocultar la ventana principal

    # Crear la ventana de gestión de pagos (usar un id_usuario válido)
    app = GestionPagos(2, "Fernando123")
    app.mainloop()