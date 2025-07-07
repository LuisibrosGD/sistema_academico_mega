import tkinter as tk
from tkinter import ttk, messagebox

from sistema_mega.modelo.usuarios_modelo import mostrar_colaboradores, crear_colaborador, editar_colaborador


# Realizado por Luis Bizarro
class GestionColaboradores(tk.Toplevel):
    def __init__(self, ventana_anterior):
        super().__init__()
        self.configurar_ventana()
        self.ventana_anterior = ventana_anterior
        self.colab_seleccionado = None
        self.aplicar_estilos()
        self.agregar_mas_widgets()

    def aplicar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        estilo.configure("Estilo.TButton",
                         foreground="black",
                         background="#d0f0fd",
                         font=("Segoe UI", 10, "bold"),
                         borderwidth=1,
                         padding=6)
        estilo.map("Estilo.TButton",
                   background=[("active", "#b0e0f8")])

        estilo.configure("FondoBlanco.TFrame", background="white")
        estilo.configure("Titulo.TLabel", font=("Segoe UI", 16, "bold"), background="white", foreground="black")

    def configurar_ventana(self):
        self.title("Gestión de Colaboradores")
        self.geometry("1200x600")
        self.configure(bg="white")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def centrar_ventana(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def agregar_mas_widgets(self):
        frame_principal = ttk.Frame(self, padding=10, style="FondoBlanco.TFrame")
        frame_principal.grid(row=0, column=0, sticky="nsew")

        for r in range(4):
            frame_principal.rowconfigure(r, weight=1)
        for c in range(5):
            frame_principal.columnconfigure(c, weight=1)

        label_titulo = ttk.Label(frame_principal, text="Gestión de Colaboradores", style="Titulo.TLabel")
        label_titulo.grid(row=0, column=0, columnspan=4, pady=(10, 5))

        boton_crear = ttk.Button(
            frame_principal,
            text="Crear Colaborador",
            command=self.crear_colaborador,
            style="Estilo.TButton"
        )
        boton_crear.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        boton_editar = ttk.Button(
            frame_principal,
            text="Editar Administrador",
            command=self.editar_colaborador,
            style="Estilo.TButton"
        )
        boton_editar.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        frame_tabla = ttk.Frame(frame_principal, style="FondoBlanco.TFrame")
        frame_tabla.grid(row=2, column=0, columnspan=5, sticky="nsew")
        frame_tabla.rowconfigure(0, weight=1)
        frame_tabla.columnconfigure(0, weight=1)

        columnas = ("ID", "Nombre", "Ap. Paterno", "Ap. Materno", "Tipo Doc.", "Nro Doc.",
                    "Estado", "Usuario", "Correo", "Contraseña")
        self.tabla_colabs = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        self.tabla_colabs.bind("<Double-1>", self.seleccionar_colab)

        for col in columnas:
            self.tabla_colabs.heading(col, text=col)
            self.tabla_colabs.column(col, anchor="center", stretch=True, width=100, minwidth=80)

        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_colabs.yview)
        self.tabla_colabs.configure(yscrollcommand=scrollbar_y.set)

        self.tabla_colabs.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        # Botón volver con estilo
        boton_volver = ttk.Button(self, text="Volver", command=self.regresar_menu, style="Estilo.TButton")
        boton_volver.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.cargar_datos_tabla()

    def seleccionar_colab(self, event):
        item = self.tabla_colabs.focus()
        if item:
            valores = self.tabla_colabs.item(item)["values"]
            self.colab_seleccionado = {
                "id": valores[0],
                "nombre": valores[1],
                "ap_paterno": valores[2],
                "ap_materno": valores[3],
                "tipo_documento": valores[4],
                "nro_documento": valores[5],
                "estado": 1 if valores[6] == "Activado" else 0,
                "nombre_usuario": valores[7],
                "correo": valores[8],
                "contrasena": valores[9],
            }
            print("✅ Admin seleccionado:", self.colab_seleccionado)

    def cargar_datos_tabla(self):
        for item in self.tabla_colabs.get_children():
            self.tabla_colabs.delete(item)
        resultados = mostrar_colaboradores()
        if resultados:
            for fila in resultados:
                id_adm, nombre, ap_paterno, ap_materno, tipo_doc, nro_doc, estado, usuario, correo, contrasena = fila
                estado_str = "Activado" if estado == 1 else "Desactivado"
                self.tabla_colabs.insert("", tk.END, values=(
                    id_adm, nombre, ap_paterno, ap_materno, tipo_doc, nro_doc, estado_str, usuario, correo, contrasena
                ))

    def regresar_menu(self):
        self.destroy()
        self.ventana_anterior.deiconify()

    def crear_colaborador(self):
        self.withdraw()
        app = CrearColaborador(self)
        app.grab_set()

    def editar_colaborador(self):
        if self.colab_seleccionado is None:
            messagebox.showwarning("Atención", "Primero selecciona un colaborador haciendo doble clic en la tabla.")
            return
        self.withdraw()
        app = EditarColaborador(self, self.colab_seleccionado)
        app.grab_set()

    def actualizar_tabla(self):
        self.cargar_datos_tabla()
        self.colab_seleccionado = None

# Estas ventanas son para los botones ====================================
class CrearColaborador(tk.Toplevel):
    def __init__(self, ventana):
        super().__init__()
        self.ventana = ventana
        self.configurar_ventana()
        self.centrar_ventana()

        self.agregar_mas_widgets()
        self.aplicar_estilos()

    def aplicar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")  # Cambia a 'clam' para mejor compatibilidad de colores
        estilo.configure("Estilo.TButton",
                         foreground="black",
                         background="#d0f0fd",  # celeste pastel claro
                         font=("Segoe UI", 10, "bold"),
                         borderwidth=1,
                         padding=6)
        estilo.map("Estilo.TButton",
                   background=[("active", "#b0e0f8")])

    def configurar_ventana(self):
        self.title("Crear Administrador")
        self.geometry("800x600")
        self.configure(bg="grey")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def centrar_ventana(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def agregar_mas_widgets(self):
        f_colab_edit = ttk.Frame(self, padding=20)
        f_colab_edit.grid(row=0, column=0, sticky="nsew")

        # Configuración de la grilla del frame
        for i in range(19):  # 20 filas para inputs, 1 para botones
            f_colab_edit.rowconfigure(i, weight=1)
        for j in range(1):  # 3 columnas
            f_colab_edit.columnconfigure(j, weight=1)

        label_titulo = ttk.Label(f_colab_edit, text="Editar Administrador", font=("Arial", 16, "bold"))
        label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Etiquetas y campos
        ttk.Label(f_colab_edit, text="Nombre de usuario:").grid(row=1, column=0, columnspan=3, sticky="w", padx=5,
                                                                pady=5)
        self.entry_usuario = ttk.Entry(f_colab_edit)
        self.entry_usuario.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Correo:").grid(row=3, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.entry_correo = ttk.Entry(f_colab_edit)
        self.entry_correo.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Contraseña:").grid(row=5, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.entry_contrasena = ttk.Entry(f_colab_edit, show="*")
        self.entry_contrasena.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Nombres:").grid(row=7, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.entry_nombres = ttk.Entry(f_colab_edit)
        self.entry_nombres.grid(row=8, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Apellido Paterno:").grid(row=9, column=0, columnspan=3, sticky="w", padx=5,
                                                               pady=5)
        self.entry_ap_paterno = ttk.Entry(f_colab_edit)
        self.entry_ap_paterno.grid(row=10, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Apellido Materno:").grid(row=11, column=0, columnspan=3, sticky="w", padx=5,
                                                               pady=5)
        self.entry_ap_materno = ttk.Entry(f_colab_edit)
        self.entry_ap_materno.grid(row=12, column=0, sticky="ew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Tipo de documento:").grid(row=13, column=0, columnspan=3, sticky="w", padx=5,
                                                                pady=5)
        self.combo_doc = ttk.Combobox(f_colab_edit, values=["DNI", "Pasaporte"], state="readonly")
        self.combo_doc.grid(row=14, column=0, sticky="ew", padx=5, pady=5)
        self.combo_doc.current(0)

        ttk.Label(f_colab_edit, text="Número de documento:").grid(row=15, column=0, columnspan=3, sticky="w", padx=5,
                                                                  pady=5)
        self.entry_num_doc = ttk.Entry(f_colab_edit)
        self.entry_num_doc.grid(row=16, column=0, sticky="ew", padx=5, pady=5)

        # Botones
        btn_frame = ttk.Frame(f_colab_edit)
        btn_frame.grid(row=17, column=0, columnspan=2, pady=10)

        btn_regresar = ttk.Button(btn_frame, text="Regresar", command=self.regresar_menu)
        btn_regresar.pack(side="left", padx=10)

        btn_confirmar = ttk.Button(btn_frame, text="Confirmar", command=self.confirmar_creacion)
        btn_confirmar.pack(side="right", padx=10)

    def regresar_menu(self):
        self.destroy()
        self.ventana.deiconify()


    def confirmar_creacion(self):
        # Obtener los datos del formulario

        nombre_usuario = self.entry_usuario.get()
        correo = self.entry_correo.get()
        contrasenia = self.entry_contrasena.get()
        nombre = self.entry_nombres.get()
        ap_paterno = self.entry_ap_paterno.get()
        ap_materno = self.entry_ap_materno.get()
        tipo_documento = self.combo_doc.get()
        nro_documento = self.entry_num_doc.get()

        mensaje = crear_colaborador(
            nombre_usuario, correo, contrasenia,
            nombre, ap_paterno, ap_materno,
            tipo_documento, nro_documento
        )
        print("Mensaje devuelto:", mensaje)
        messagebox.showinfo("Resultado", mensaje)

        if "Administrador agregado exitosamente" in mensaje.lower():
            self.ventana.actualizar_tabla()
            self.destroy()
            self.ventana.deiconify()

class EditarColaborador(tk.Toplevel):
    def __init__(self, ventana, colab_data):
        super().__init__()
        self.ventana = ventana
        self.colab_data = colab_data
        self.configurar_ventana()
        self.centrar_ventana()

        # Obteniendo el id del colaborador (no es del usuario)
        self.id_tabla_colaborador = self.colab_data["id"]

        self.agregar_mas_widgets()
        self.cargar_datos()
        self.aplicar_estilos()

    def aplicar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")  # Cambia a 'clam' para mejor compatibilidad de colores
        estilo.configure("Estilo.TButton",
                         foreground="black",
                         background="#d0f0fd",  # celeste pastel claro
                         font=("Segoe UI", 10, "bold"),
                         borderwidth=1,
                         padding=6)
        estilo.map("Estilo.TButton",
                   background=[("active", "#b0e0f8")])


    def cargar_datos(self):

        self.entry_nombres.insert(0, self.colab_data["nombre"])
        self.entry_ap_paterno.insert(0, self.colab_data["ap_paterno"])
        self.entry_ap_materno.insert(0, self.colab_data["ap_materno"])
        self.combo_doc.set(self.colab_data["tipo_documento"])
        self.entry_num_doc.insert(0, self.colab_data["nro_documento"])

        # Suponiendo que colab_data["estado"] es 1 o 0
        estado_str = "Activado" if self.colab_data["estado"] == 1 else "Desactivado"
        self.combo_estado.set(estado_str)

        # Esto deberías cambiarlo si ya tienes los datos reales del usuario
        self.entry_usuario.insert(0, self.colab_data.get("nombre_usuario", f"usuario_{self.colab_data['id']}"))
        self.entry_correo.insert(0, self.colab_data.get("correo", "correo@ejemplo.com"))
        self.entry_contrasena.insert(0, self.colab_data.get("contrasena", "*****"))

    def configurar_ventana(self):
        self.title("Editar Administrador")
        self.geometry("800x900")
        self.configure(bg="grey")

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def centrar_ventana(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def agregar_mas_widgets(self):
        f_colab_edit = ttk.Frame(self, padding=20)
        f_colab_edit.grid(row=0, column=0, sticky="nsew")

        # Configuración de la grilla del frame
        for i in range(19):  # 20 filas para inputs, 1 para botones
            f_colab_edit.rowconfigure(i, weight=1)
        for j in range(1):  # 3 columnas
            f_colab_edit.columnconfigure(j, weight=1)

        label_titulo = ttk.Label(f_colab_edit, text="Editar Administrador", font=("Arial", 16, "bold"))
        label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        # Etiquetas y campos
        ttk.Label(f_colab_edit, text="Nombre de usuario:").grid(row=1, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.entry_usuario = ttk.Entry(f_colab_edit)
        self.entry_usuario.grid(row=2, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Correo:").grid(row=3, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.entry_correo = ttk.Entry(f_colab_edit)
        self.entry_correo.grid(row=4, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Contraseña:").grid(row=5, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.entry_contrasena = ttk.Entry(f_colab_edit, show="*")
        self.entry_contrasena.grid(row=6, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Nombres:").grid(row=7, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.entry_nombres = ttk.Entry(f_colab_edit)
        self.entry_nombres.grid(row=8, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Apellido Paterno:").grid(row=9, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.entry_ap_paterno = ttk.Entry(f_colab_edit)
        self.entry_ap_paterno.grid(row=10, column=0, sticky="nsew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Apellido Materno:").grid(row=11, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.entry_ap_materno = ttk.Entry(f_colab_edit)
        self.entry_ap_materno.grid(row=12, column=0, sticky="ew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text="Tipo de documento:").grid(row=13, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.combo_doc = ttk.Combobox(f_colab_edit, values=["DNI", "Pasaporte"], state="readonly")
        self.combo_doc.grid(row=14, column=0, sticky="ew", padx=5, pady=5)
        self.combo_doc.current(0)

        ttk.Label(f_colab_edit, text="Número de documento:").grid(row=15, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.entry_num_doc = ttk.Entry(f_colab_edit)
        self.entry_num_doc.grid(row=16, column=0, sticky="ew", padx=5, pady=5)

        ttk.Label(f_colab_edit, text = "Estado: ").grid(row=17, column=0, columnspan=3, sticky="w", padx=5, pady=5)
        self.combo_estado = ttk.Combobox(f_colab_edit, values = ["Activado", "Desactivado"], state="readonly")
        self.combo_estado.grid(row=18, column=0, sticky="ew", padx=5, pady=5)

        # Agregar botones

        btn_frame = ttk.Frame(f_colab_edit)
        btn_frame.grid(row=19, column=0, columnspan=2, pady=10)

        btn_regresar = ttk.Button(btn_frame, text="Regresar", command=self.regresar_menu)
        btn_regresar.pack(side="left", padx=10)

        btn_confirmar = ttk.Button(btn_frame, text="Confirmar", command=self.confirmar_editar)
        btn_confirmar.pack(side="right", padx=10)

    def regresar_menu(self):
        self.destroy()
        self.ventana.deiconify()

    def confirmar_editar(self):
        # Obtener datos del formulario
        nombre_usuario = self.entry_usuario.get().strip()
        correo = self.entry_correo.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        nombres = self.entry_nombres.get().strip()
        apellido_paterno = self.entry_ap_paterno.get().strip()
        apellido_materno = self.entry_ap_materno.get().strip()
        tipo_documento = self.combo_doc.get().strip()
        numero_documento = self.entry_num_doc.get().strip()

        # Convertir estado textual a valor numérico
        estado_texto = self.combo_estado.get().strip().lower()
        estado = 1 if estado_texto == "activado" else 0

        mensaje = editar_colaborador(
            self.id_tabla_colaborador,
            nombre_usuario,
            correo,
            contrasena,
            estado,
            nombres,
            apellido_paterno,
            apellido_materno,
            tipo_documento,
            numero_documento
        )
        print("Mensaje devuelto:", mensaje)
        messagebox.showinfo("Resultado", mensaje)

        # MODIFICACIÓN: Actualizar tabla si la edición fue exitosa
        if "Administrador actualizado correctamente" in mensaje.lower() or "éxito" in mensaje.lower():
            self.ventana.actualizar_tabla()
            self.destroy()
            self.ventana.deiconify()



if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana raíz
    app1 = GestionColaboradores(root)
    app1.mainloop()

