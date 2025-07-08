import tkinter as tk
from tkinter import ttk, messagebox

from sistema_mega.modelo.usuarios_modelo import mostrar_profesores, crear_profesor, editar_profesor, insertar_especialidades_profesor, obtener_especialidades_profesor, actualizar_especialidades_profesor, eliminar_especialidades_profesor
from sistema_mega.modelo.administrador_modelo import mostrar_nombres_especialidades

# Realizado por Luis Bizarro
class GestionProfesores(tk.Toplevel):
    def __init__(self, ventana_anterior):
        super().__init__()
        self.configurar_ventana()
        self.ventana_anterior = ventana_anterior
        self.profesor_seleccionado = None
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
        self.title("Gestión de Profesores")
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

        label_titulo = ttk.Label(frame_principal, text="Gestión de Profesores", style="Titulo.TLabel")
        label_titulo.grid(row=0, column=0, columnspan=4, pady=(10, 5))

        boton_crear = ttk.Button(
            frame_principal,
            text="Crear Profesor",
            command=self.crear_profesor,
            style="Estilo.TButton"
        )
        boton_crear.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        boton_editar = ttk.Button(
            frame_principal,
            text="Editar Profesor",
            command=self.editar_profesor,
            style="Estilo.TButton"
        )
        boton_editar.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        frame_tabla = ttk.Frame(frame_principal, style="FondoBlanco.TFrame")
        frame_tabla.grid(row=2, column=0, columnspan=5, sticky="nsew")
        frame_tabla.rowconfigure(0, weight=1)
        frame_tabla.columnconfigure(0, weight=1)

        columnas = ("ID", "Nombre", "Ap. Paterno", "Ap. Materno", "Tipo Doc.", "Nro Doc.",
                    "Estado", "Usuario", "Correo", "Contraseña")
        self.tabla_profesores = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        self.tabla_profesores.bind("<Double-1>", self.seleccionar_profesor)

        for col in columnas:
            self.tabla_profesores.heading(col, text=col)
            self.tabla_profesores.column(col, anchor="center", stretch=True, width=100, minwidth=80)

        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla_profesores.yview)
        self.tabla_profesores.configure(yscrollcommand=scrollbar_y.set)

        self.tabla_profesores.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        boton_volver = ttk.Button(self, text="Volver", command=self.regresar_menu, style="Estilo.TButton")
        boton_volver.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.cargar_datos_tabla()

    def seleccionar_profesor(self, event):
        item = self.tabla_profesores.focus()
        if item:
            valores = self.tabla_profesores.item(item)["values"]
            self.profesor_seleccionado = {
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
            print("✅ Profesor seleccionado:", self.profesor_seleccionado)

    def cargar_datos_tabla(self):
        for item in self.tabla_profesores.get_children():
            self.tabla_profesores.delete(item)
        resultados = mostrar_profesores()
        if resultados:
            for fila in resultados:
                id_prof, nombre, ap_paterno, ap_materno, tipo_doc, nro_doc, estado, usuario, correo, contrasena = fila
                estado_str = "Activado" if estado == 1 else "Desactivado"
                self.tabla_profesores.insert("", tk.END, values=(
                    id_prof, nombre, ap_paterno, ap_materno, tipo_doc, nro_doc, estado_str, usuario, correo, contrasena
                ))

    def regresar_menu(self):
        self.destroy()
        self.ventana_anterior.deiconify()

    def crear_profesor(self):
        self.withdraw()
        app = CrearProfesor(self)
        app.grab_set()

    def editar_profesor(self):
        if self.profesor_seleccionado is None:
            messagebox.showwarning("Atención", "Primero selecciona un profesor haciendo doble clic en la tabla.")
            return
        self.withdraw()
        app = EditarProfesor(self, self.profesor_seleccionado)
        app.grab_set()

    def actualizar_tabla(self):
        self.cargar_datos_tabla()
        self.profesor_seleccionado = None

# Estas ventanas son para los botones ====================================
class CrearProfesor(tk.Toplevel):
    def __init__(self, ventana):
        super().__init__()
        self.ventana = ventana
        self.configurar_ventana()
        self.centrar_ventana()
        self.agregar_mas_widgets()
        self.aplicar_estilos()

    def aplicar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Estilo.TButton",
                         foreground="black",
                         background="#d0f0fd",
                         font=("Segoe UI", 10, "bold"),
                         borderwidth=1,
                         padding=6)
        estilo.map("Estilo.TButton", background=[("active", "#b0e0f8")])

    def configurar_ventana(self):
        self.title("Crear Profesor")
        self.geometry("800x700")
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
        f_prof = ttk.Frame(self, padding=20)
        f_prof.grid(row=0, column=0, sticky="nsew")

        for i in range(20):
            f_prof.rowconfigure(i, weight=1)
        f_prof.columnconfigure(0, weight=1)

        # Campos del formulario
        campos = [
            ("Nombre de usuario:", "entry_usuario"),
            ("Correo:", "entry_correo"),
            ("Contraseña:", "entry_contrasena"),
            ("Nombres:", "entry_nombres"),
            ("Apellido Paterno:", "entry_ap_paterno"),
            ("Apellido Materno:", "entry_ap_materno"),
            ("Tipo de documento:", "combo_doc"),
            ("Número de documento:", "entry_num_doc")
        ]

        for i, (label_text, attr_name) in enumerate(campos):
            ttk.Label(f_prof, text=label_text).grid(row=i*2, column=0, sticky="w", padx=5, pady=5)
            if "combo" in attr_name:
                widget = ttk.Combobox(f_prof, values=["DNI", "Pasaporte"], state="readonly")
                widget.current(0)
            else:
                widget = ttk.Entry(f_prof, show="*" if "contrasena" in attr_name else "")
            widget.grid(row=i*2 + 1, column=0, sticky="ew", padx=5, pady=5)
            setattr(self, attr_name, widget)

        # -------------------- NUEVO: Selección múltiple de especialidades --------------------
        ttk.Label(f_prof, text="Especialidades:").grid(row=16, column=0, sticky="w", padx=5, pady=5)

        self.listbox_especialidades = tk.Listbox(f_prof, selectmode="multiple", height=6, exportselection=False)
        self.listbox_especialidades.grid(row=17, column=0, sticky="nsew", padx=5, pady=5)

        # Cargar especialidades desde la base de datos
        especialidades = mostrar_nombres_especialidades()
        for esp in especialidades:
            self.listbox_especialidades.insert(tk.END, esp[0])  # esp es una tupla (nombre_especialidad,)
        # ------------------------------------------------------------------------

        # Botones
        btn_frame = ttk.Frame(f_prof)
        btn_frame.grid(row=18, column=0, pady=10)

        ttk.Button(btn_frame, text="Regresar", command=self.regresar_menu).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Confirmar", command=self.confirmar_creacion).pack(side="right", padx=10)

    def regresar_menu(self):
        self.destroy()
        self.ventana.deiconify()

    def confirmar_creacion(self):
        # Obtener los datos
        nombre_usuario = self.entry_usuario.get().strip()
        correo = self.entry_correo.get().strip()
        contrasenia = self.entry_contrasena.get().strip()
        nombre = self.entry_nombres.get().strip()
        ap_paterno = self.entry_ap_paterno.get().strip()
        ap_materno = self.entry_ap_materno.get().strip()
        tipo_documento = self.combo_doc.get().strip()
        nro_documento = self.entry_num_doc.get().strip()

        # Obtener especialidades seleccionadas
        indices = self.listbox_especialidades.curselection()
        especialidades_seleccionadas = [self.listbox_especialidades.get(i) for i in indices]

        if not especialidades_seleccionadas:
            messagebox.showwarning("Atención", "Selecciona al menos una especialidad.")
            return

        # Crear profesor
        id_profesor, mensaje = crear_profesor(
            nombre_usuario, correo, contrasenia,
            nombre, ap_paterno, ap_materno,
            tipo_documento, nro_documento
        )

        if id_profesor:
            insertar_especialidades_profesor(id_profesor, especialidades_seleccionadas)
            mensaje += "\nEspecialidades agregadas."
        else:
            print("❌ No se pudo crear el profesor")

        print("Mensaje devuelto:", mensaje)
        messagebox.showinfo("Resultado", mensaje)

        if "profesor" in mensaje.lower():
            self.ventana.actualizar_tabla()
            self.destroy()
            self.ventana.deiconify()

class EditarProfesor(tk.Toplevel):
    def __init__(self, ventana, profesor_data):
        super().__init__()
        self.ventana = ventana
        self.profesor_data = profesor_data
        self.configurar_ventana()
        self.centrar_ventana()

        self.id_tabla_profesor = self.profesor_data["id"]

        self.agregar_mas_widgets()
        self.cargar_datos()
        self.aplicar_estilos()

    def aplicar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Estilo.TButton",
                         foreground="black",
                         background="#d0f0fd",
                         font=("Segoe UI", 10, "bold"),
                         borderwidth=1,
                         padding=6)
        estilo.map("Estilo.TButton", background=[("active", "#b0e0f8")])

    def configurar_ventana(self):
        self.title("Editar Profesor")
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
        f_prof_edit = ttk.Frame(self, padding=20)
        f_prof_edit.grid(row=0, column=0, sticky="nsew")

        for i in range(21):
            f_prof_edit.rowconfigure(i, weight=1)
        f_prof_edit.columnconfigure(0, weight=1)

        ttk.Label(f_prof_edit, text="Editar Profesor", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Campos
        etiquetas = [
            ("Nombre de usuario:", "entry_usuario"),
            ("Correo:", "entry_correo"),
            ("Contraseña:", "entry_contrasena"),
            ("Nombres:", "entry_nombres"),
            ("Apellido Paterno:", "entry_ap_paterno"),
            ("Apellido Materno:", "entry_ap_materno"),
            ("Número de documento:", "entry_num_doc")
        ]

        for i, (texto, atributo) in enumerate(etiquetas):
            ttk.Label(f_prof_edit, text=texto).grid(row=1 + i*2, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(f_prof_edit, show="*" if "contrasena" in atributo else "")
            entry.grid(row=2 + i*2, column=0, sticky="ew", padx=5, pady=5)
            setattr(self, atributo, entry)

        # Combo tipo documento
        ttk.Label(f_prof_edit, text="Tipo de documento:").grid(row=15, column=0, sticky="w", padx=5, pady=5)
        self.combo_doc = ttk.Combobox(f_prof_edit, values=["dni", "pasaporte"], state="readonly")
        self.combo_doc.grid(row=16, column=0, sticky="ew", padx=5, pady=5)

        # Combo estado
        ttk.Label(f_prof_edit, text="Estado:").grid(row=17, column=0, sticky="w", padx=5, pady=5)
        self.combo_estado = ttk.Combobox(f_prof_edit, values=["Activado", "Desactivado"], state="readonly")
        self.combo_estado.grid(row=18, column=0, sticky="ew", padx=5, pady=5)

        # ------- Lista de Especialidades (múltiple selección) -------
        ttk.Label(f_prof_edit, text="Especialidades:").grid(row=19, column=0, sticky="w", padx=5, pady=5)

        self.listbox_especialidades = tk.Listbox(f_prof_edit, selectmode="multiple", height=6, exportselection=False)
        self.listbox_especialidades.grid(row=20, column=0, sticky="nsew", padx=5, pady=5)

        # Cargar todas las especialidades disponibles
        especialidades_disponibles = mostrar_nombres_especialidades()
        self.lista_especialidades = [esp[0] for esp in especialidades_disponibles]
        for esp in self.lista_especialidades:
            self.listbox_especialidades.insert(tk.END, esp)

        # Botones
        btn_frame = ttk.Frame(f_prof_edit)
        btn_frame.grid(row=21, column=0, pady=10)

        ttk.Button(btn_frame, text="Regresar", command=self.regresar_menu).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Confirmar", command=self.confirmar_edicion).pack(side="right", padx=10)

    def cargar_datos(self):
        self.entry_nombres.insert(0, self.profesor_data["nombre"])
        self.entry_ap_paterno.insert(0, self.profesor_data["ap_paterno"])
        self.entry_ap_materno.insert(0, self.profesor_data["ap_materno"])
        self.combo_doc.set(self.profesor_data["tipo_documento"])
        self.entry_num_doc.insert(0, self.profesor_data["nro_documento"])
        self.combo_estado.set("Activado" if self.profesor_data["estado"] == 1 else "Desactivado")
        self.entry_usuario.insert(0, self.profesor_data["nombre_usuario"])
        self.entry_correo.insert(0, self.profesor_data["correo"])
        self.entry_contrasena.insert(0, self.profesor_data["contrasena"])
        # Seleccionar las especialidades actuales del profesor
        especialidades_actuales = obtener_especialidades_profesor(self.id_tabla_profesor)
        nombres_actuales = {esp[0] for esp in especialidades_actuales}

        for idx, esp in enumerate(self.lista_especialidades):
            if esp in nombres_actuales:
                self.listbox_especialidades.selection_set(idx)

    def regresar_menu(self):
        self.destroy()
        self.ventana.deiconify()

    def confirmar_edicion(self):
        nombre_usuario = self.entry_usuario.get().strip()
        correo = self.entry_correo.get().strip()
        contrasena = self.entry_contrasena.get().strip()
        nombres = self.entry_nombres.get().strip()
        apellido_paterno = self.entry_ap_paterno.get().strip()
        apellido_materno = self.entry_ap_materno.get().strip()
        tipo_documento = self.combo_doc.get().strip()
        numero_documento = self.entry_num_doc.get().strip()
        estado = 1 if self.combo_estado.get().strip().lower() == "activado" else 0


        # Obtener especialidades seleccionadas
        indices = self.listbox_especialidades.curselection()
        especialidades_seleccionadas = [self.listbox_especialidades.get(i) for i in indices]

        # Guardar especialidades seleccionadas (ej. eliminando anteriores y reinsertando)
        eliminar_especialidades_profesor(self.id_tabla_profesor)
        insertar_especialidades_profesor(self.id_tabla_profesor, especialidades_seleccionadas)

        mensaje = editar_profesor(self.id_tabla_profesor, nombres, apellido_paterno, apellido_materno,tipo_documento, numero_documento, nombre_usuario, correo, contrasena, estado)
        print("Mensaje devuelto:", mensaje)

        if "Profesor actualizado correctamente" in mensaje:
            # ✅ Obtener especialidades seleccionadas
            indices = self.listbox_especialidades.curselection()
            especialidades_seleccionadas = [self.listbox_especialidades.get(i) for i in indices]

            # ✅ Actualizar especialidades en la base de datos
            actualizar_especialidades_profesor(self.id_tabla_profesor, especialidades_seleccionadas)

            # ✅ Refrescar tabla y cerrar ventana
            self.ventana.actualizar_tabla()
            self.destroy()
            self.ventana.deiconify()
