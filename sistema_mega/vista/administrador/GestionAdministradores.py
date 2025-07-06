import tkinter as tk
from tkinter import ttk

from sistema_mega.modelo.usuarios_modelo import mostrar_administradores

# Realizado por Luis Bizarro
class GestionAdministradores(tk.Toplevel):
    def __init__(self, ventana_anterior):
        super().__init__()
        self.configurar_ventana()
        self.centrar_ventana()
        self.ventana_anterior = ventana_anterior

        self.agregar_mas_widgets()


    def configurar_ventana(self):
        self.title("Panel del Administrador")
        self.geometry("800x600")
        self.configure(bg="grey")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0,weight=1)

    def centrar_ventana(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def agregar_mas_widgets(self):
        # Crear un frame principal (4 filas y 5 columnas)
        frame_principal = ttk.Frame(self, padding=10)
        frame_principal.grid(row=0, column=0, sticky="nsew")

        # Configuracion de grillas
        frame_principal.rowconfigure(0, weight=1)
        frame_principal.rowconfigure(1, weight=1)
        frame_principal.rowconfigure(2, weight=3)
        frame_principal.rowconfigure(3, weight=1)

        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.columnconfigure(2, weight=1)
        frame_principal.columnconfigure(3, weight=1)
        frame_principal.columnconfigure(4, weight=1)

        # Etiqueta titulo
        label_titulo = ttk.Label(frame_principal, text="Gestion administradores")
        label_titulo.grid(row=0,column=2)

        # botones de crear y editar
        boton_crear = ttk.Button(frame_principal, text="Crear Administrador")
        boton_crear.grid(row=1,column=0, sticky="nsew")

        boton_editar = ttk.Button(frame_principal, text = "Editar Administrador")
        boton_editar.grid(row=1,column=1, sticky="nsew")

        # Tabla para mostrar administradores
        # Frame contenedor exclusivo para la tabla y el scrollbar
        frame_tabla = ttk.Frame(frame_principal)
        frame_tabla.grid(row=2, column=0, columnspan=5, sticky="nsew")

        # Asegura que el frame_tabla se expanda bien
        frame_tabla.rowconfigure(0, weight=1)
        frame_tabla.columnconfigure(0, weight=1)

        columnas = ("ID", "Nombre", "Ap. Paterno", "Ap. Materno", "Tipo Doc.", "Nro Doc.")
        self.tabla_admins = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        # Encabezados de columna
        for col in columnas:
            self.tabla_admins.heading(col, text=col)
            self.tabla_admins.column(col, width=100, anchor="center")
        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_admins.yview)
        self.tabla_admins.configure(yscrollcommand=scrollbar_y.set)

        # Empaquetar tabla y scrollbar uno al lado del otro
        self.tabla_admins.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        # boton para volver
        boton_volver = tk.Button(self, text="Volver", command=self.regresar_menu)
        boton_volver.grid(row=3,column=0,sticky="w")

        # Llenar tabla desde la BD
        self.cargar_datos_tabla()

    def cargar_datos_tabla(self):
        resultados = mostrar_administradores()
        if resultados:
            for fila in resultados:
                self.tabla_admins.insert("", tk.END, values=fila)

    def regresar_menu(self):
        self.destroy()
        self.ventana_anterior.deiconify()




