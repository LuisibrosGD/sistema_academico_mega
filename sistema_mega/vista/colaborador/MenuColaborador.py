import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from sistema_mega.modelo.colaborador_modelo import FuncionesColaborador
from sistema_mega.database.conexion import ejecutar_select

# Paleta de colores moderna
PRIMARY_COLOR = "#3498db"
SECONDARY_COLOR = "#2c3e50"
ACCENT_COLOR = "#e74c3c"
BACKGROUND_COLOR = "#ecf0f1"
TEXT_COLOR = "#2c3e50"
SUCCESS_COLOR = "#2ecc71"
BUTTON_HOVER = "#2980b9"


class VentanaRegistrarAsistencia(tk.Toplevel):
    def __init__(self, parent, id_colaborador):
        super().__init__(parent)
        self.title("✅ Registrar Asistencia")
        self.geometry("750x380")  # Aumentado para acomodar mejor el combobox
        self.resizable(False, False)
        self.id_colaborador = id_colaborador

        # Configurar estilos
        self.style = ttk.Style(self)
        self.style.configure("TFrame", background=BACKGROUND_COLOR)
        self.style.configure("TLabel", background=BACKGROUND_COLOR, foreground=TEXT_COLOR, font=("Arial", 10))
        self.style.configure("TButton", background=PRIMARY_COLOR, foreground="white",
                             font=("Arial", 10, "bold"), borderwidth=1)
        self.style.map("TButton", background=[("active", BUTTON_HOVER), ("pressed", PRIMARY_COLOR)])
        self.style.configure("Title.TLabel", font=("Arial", 14, "bold"),
                             foreground=SECONDARY_COLOR, background=BACKGROUND_COLOR)
        self.style.configure("TRadiobutton", background=BACKGROUND_COLOR)
        self.style.configure("TCombobox", fieldbackground="white", foreground=TEXT_COLOR)

        # Frame principal
        main_frame = ttk.Frame(self, padding=20, style="TFrame")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.columnconfigure(1, weight=1)

        # Título con icono
        ttk.Label(main_frame, text="📝 Registrar Asistencia",
                  style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

        # Profesor - con más espacio para el combobox
        ttk.Label(main_frame, text="Profesor:", style="TLabel").grid(row=1, column=0, sticky="w", pady=5)

        profesores = FuncionesColaborador.obtener_profesores_por_colaborador(self.id_colaborador)
        self.profesores_dict = {}
        valores_combo = []

        if profesores:
            for profesor in profesores:
                if len(profesor) >= 3:
                    nombre, curso, grupo = profesor[:3]
                    texto = f"{nombre} - {curso} - {grupo}"
                    valores_combo.append(texto)
                    self.profesores_dict[texto] = nombre
                else:
                    print(f"Formato inesperado: {profesor}")
        else:
            print("No se encontraron profesores para este colaborador")

        # Ajuste clave: combobox más ancho con scroll horizontal
        self.combo_profesor = ttk.Combobox(main_frame, values=valores_combo,
                                           state="readonly", width=45)  # Aumentado a 45 caracteres
        self.combo_profesor.grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 10))

        # Añadir scroll horizontal para nombres largos
        self.combo_profesor.bind("<<ComboboxSelected>>", self.ajustar_scroll)

        if valores_combo:
            self.combo_profesor.current(0)
        else:
            self.combo_profesor.set("No hay profesores disponibles")
            ttk.Label(main_frame, text="⚠️ No hay profesores asignados",
                      foreground=ACCENT_COLOR, background=BACKGROUND_COLOR).grid(row=1, column=1, sticky="w")

        # Estado de Asistencia
        ttk.Label(main_frame, text="Estado de Asistencia:", style="TLabel").grid(row=2, column=0, sticky="w", pady=5)
        self.estado_var = tk.StringVar(value="presente")

        frame_estados = ttk.Frame(main_frame, style="TFrame")
        frame_estados.grid(row=2, column=1, sticky="w", pady=5)

        ttk.Radiobutton(frame_estados, text="Presente ✅", variable=self.estado_var,
                        value="presente", style="TRadiobutton").pack(anchor="w", padx=5, pady=2)
        ttk.Radiobutton(frame_estados, text="Tarde ⏱️", variable=self.estado_var,
                        value="tarde", style="TRadiobutton").pack(anchor="w", padx=5, pady=2)
        ttk.Radiobutton(frame_estados, text="Ausente ❌", variable=self.estado_var,
                        value="ausente", style="TRadiobutton").pack(anchor="w", padx=5, pady=2)

        # Fecha
        ttk.Label(main_frame, text="Fecha:", style="TLabel").grid(row=3, column=0, sticky="w", pady=10)
        self.cal_fecha = DateEntry(main_frame, date_pattern="dd/MM/yyyy",
                                   locale="es_ES", width=15, background="white")
        self.cal_fecha.grid(row=3, column=1, sticky="w", pady=10)
        self.cal_fecha.set_date(datetime.now())

        # Botones
        btn_frame = ttk.Frame(main_frame, style="TFrame")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Confirmar", command=self.registrar,
                   style="TButton", width=12).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy,
                   style="TButton", width=12).pack(side="left", padx=10)

    def ajustar_scroll(self, event):
        """Ajusta el scroll horizontal cuando se selecciona un profesor"""
        self.combo_profesor.xview_moveto(0)

    def registrar(self):
        profesor_texto = self.combo_profesor.get()
        estado = self.estado_var.get()
        fecha = self.cal_fecha.get_date()

        if not profesor_texto or "No hay profesores" in profesor_texto:
            messagebox.showerror("Error", "⚠️ No hay profesores disponibles para seleccionar")
            return

        # Obtener el nombre del profesor del texto seleccionado
        nombre_profesor = self.profesores_dict.get(profesor_texto)
        if not nombre_profesor:
            messagebox.showerror("Error", "❌ Profesor no válido")
            return

        # Convertir fecha a formato YYYY-MM-DD HH:MM:SS
        fecha_dt = datetime.combine(fecha, datetime.min.time())
        fecha_str = fecha_dt.strftime("%Y-%m-%d %H:%M:%S")

        # Obtener ID del profesor por su nombre completo
        query = "SELECT id_profesor FROM profesores WHERE CONCAT(nombre, ' ', ap_paterno, ' ', ap_materno) = %s"
        resultado = ejecutar_select(query, (nombre_profesor,))

        if not resultado:
            messagebox.showerror("Error", f"⚠️ No se encontró ID para el profesor: {nombre_profesor}")
            return

        id_profesor = resultado[0][0]

        # Registrar asistencia con fecha seleccionada
        success, mensaje = FuncionesColaborador.registrar_asistencia(estado, id_profesor, fecha_str)
        if success:
            messagebox.showinfo("Éxito ✅", mensaje)
            self.destroy()
        else:
            messagebox.showerror("Error ❌", mensaje)

class VentanaRegistrarCalificacion(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("📝 Registrar Calificación")
        self.geometry("500x420")
        self.resizable(False, False)

        # Configurar estilos
        self.style = ttk.Style(self)
        self.style.configure("TFrame", background=BACKGROUND_COLOR)
        self.style.configure("TLabel", background=BACKGROUND_COLOR, foreground=TEXT_COLOR, font=("Arial", 10))
        self.style.configure("TButton", background=PRIMARY_COLOR, foreground="white",
                             font=("Arial", 10, "bold"), borderwidth=1)
        self.style.map("TButton", background=[("active", BUTTON_HOVER), ("pressed", PRIMARY_COLOR)])
        self.style.configure("Title.TLabel", font=("Arial", 14, "bold"),
                             foreground=SECONDARY_COLOR, background=BACKGROUND_COLOR)
        self.style.configure("TCombobox", fieldbackground="white", foreground=TEXT_COLOR)
        self.style.configure("TEntry", fieldbackground="white", foreground=TEXT_COLOR)

        # Frame principal
        main_frame = ttk.Frame(self, padding=20, style="TFrame")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        main_frame.columnconfigure(1, weight=1)

        # Título con icono
        ttk.Label(main_frame, text="📝 Registrar Calificación",
                  style="Title.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 15), sticky="w")

        # Estudiante
        ttk.Label(main_frame, text="Estudiante:", style="TLabel").grid(row=1, column=0, sticky="w", pady=8)

        estudiantes = FuncionesColaborador.obtener_estudiantes()
        self.estudiantes_dict = {}
        valores_combo = []

        for estudiante in estudiantes:
            id_est, nombre = estudiante
            valores_combo.append(nombre)
            self.estudiantes_dict[nombre] = id_est

        self.combo_estudiante = ttk.Combobox(main_frame, values=valores_combo, state="readonly", width=35)
        self.combo_estudiante.grid(row=1, column=1, sticky="ew", pady=8)

        if valores_combo:
            self.combo_estudiante.current(0)
        else:
            self.combo_estudiante.set("No hay estudiantes disponibles")
            ttk.Label(main_frame, text="⚠️ No hay estudiantes registrados",
                      foreground=ACCENT_COLOR, background=BACKGROUND_COLOR).grid(row=1, column=1, sticky="w")

        # Puntaje
        ttk.Label(main_frame, text="Puntaje (0.00 - 2000.00):", style="TLabel").grid(row=2, column=0, sticky="w",
                                                                                     pady=8)
        self.entry_puntaje = ttk.Entry(main_frame, style="TEntry")
        self.entry_puntaje.grid(row=2, column=1, sticky="ew", pady=8)

        # Fecha
        ttk.Label(main_frame, text="Fecha de evaluación:", style="TLabel").grid(row=3, column=0, sticky="w", pady=8)
        self.cal_fecha = DateEntry(main_frame, date_pattern="dd/MM/yyyy",
                                   locale="es_ES", width=12, background="white")
        self.cal_fecha.grid(row=3, column=1, sticky="w", pady=8)
        self.cal_fecha.set_date(datetime.now())

        # Botones
        btn_frame = ttk.Frame(main_frame, style="TFrame")
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Guardar", command=self.registrar,
                   style="TButton", width=12).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy,
                   style="TButton", width=12).pack(side="left", padx=10)

    def registrar(self):
        estudiante_nombre = self.combo_estudiante.get()
        puntaje = self.entry_puntaje.get()
        fecha = self.cal_fecha.get_date()

        if not estudiante_nombre or "No hay estudiantes" in estudiante_nombre:
            messagebox.showerror("Error ❌", "⚠️ No hay estudiantes disponibles para seleccionar")
            return

        if not puntaje:
            messagebox.showerror("Error ❌", "⚠️ Ingrese un puntaje")
            return

        try:
            puntaje = float(puntaje)
            if puntaje < 0 or puntaje > 2000:
                raise ValueError("Puntaje fuera de rango")
        except ValueError:
            messagebox.showerror("Error ❌", "⚠️ Ingrese un puntaje válido (0.00 - 2000.00)")
            return

        # Convertir fecha a formato YYYY-MM-DD
        fecha_str = fecha.strftime("%Y-%m-%d")

        id_estudiante = self.estudiantes_dict.get(estudiante_nombre)
        if not id_estudiante:
            messagebox.showerror("Error ❌", "⚠️ Estudiante no válido")
            return

        success, mensaje = FuncionesColaborador.registrar_calificacion(
            id_estudiante,
            puntaje,
            fecha_str
        )
        if success:
            messagebox.showinfo("Éxito ✅", mensaje)
            self.destroy()
        else:
            messagebox.showerror("Error ❌", mensaje)


class VentanaNotasEstudiantes(tk.Toplevel):
    def __init__(self, parent, id_colaborador):
        super().__init__(parent)
        self.title("📊 Reporte de Notas")
        self.geometry("1100x650")
        self.resizable(True, True)
        self.id_colaborador = id_colaborador

        # Configurar estilos
        self.style = ttk.Style(self)
        self.style.configure("TFrame", background=BACKGROUND_COLOR)
        self.style.configure("TLabel", background=BACKGROUND_COLOR, foreground=TEXT_COLOR, font=("Arial", 10))
        self.style.configure("TButton", background=PRIMARY_COLOR, foreground="white",
                             font=("Arial", 10, "bold"), borderwidth=1)
        self.style.map("TButton", background=[("active", BUTTON_HOVER), ("pressed", PRIMARY_COLOR)])
        self.style.configure("Title.TLabel", font=("Arial", 16, "bold"),
                             foreground=SECONDARY_COLOR, background=BACKGROUND_COLOR)
        self.style.configure("Filter.TFrame", background="#d6eaf8", relief="groove", borderwidth=1)
        self.style.configure("Treeview", background="white", fieldbackground="white", foreground=TEXT_COLOR)
        self.style.configure("Treeview.Heading", background=PRIMARY_COLOR, foreground="white",
                             font=("Arial", 10, "bold"))
        self.style.map("Treeview.Heading", background=[("active", BUTTON_HOVER)])

        # Frame principal
        main_frame = ttk.Frame(self, padding=15, style="TFrame")
        main_frame.pack(fill="both", expand=True)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Título
        ttk.Label(main_frame, text="📊 Reporte de Notas de Estudiantes",
                  style="Title.TLabel").grid(row=0, column=0, columnspan=6, pady=(0, 15), sticky="w")

        # Filtros
        filtros_frame = ttk.LabelFrame(main_frame, text="Filtros", padding=10, style="Filter.TFrame")
        filtros_frame.grid(row=1, column=0, columnspan=6, sticky="ew", pady=(0, 15))
        filtros_frame.columnconfigure(6, weight=1)

        # Área Académica
        ttk.Label(filtros_frame, text="Área Académica:", style="TLabel").grid(row=0, column=0, padx=5, sticky="w")
        areas = FuncionesColaborador.obtener_areas_academicas()
        self.combo_area = ttk.Combobox(filtros_frame, values=areas, state="readonly", width=8)
        self.combo_area.grid(row=0, column=1, padx=5, sticky="w")
        self.combo_area.set("Todas")

        # Fecha Inicio
        ttk.Label(filtros_frame, text="Fecha Inicio:", style="TLabel").grid(row=0, column=2, padx=5, sticky="w")
        self.cal_fecha_ini = DateEntry(filtros_frame, date_pattern="dd/MM/yyyy",
                                       locale="es_ES", width=12, background="white")
        self.cal_fecha_ini.grid(row=0, column=3, padx=5, sticky="w")
        self.cal_fecha_ini.set_date(datetime(2025, 1, 1))

        # Fecha Fin
        ttk.Label(filtros_frame, text="Fecha Fin:", style="TLabel").grid(row=0, column=4, padx=5, sticky="w")
        self.cal_fecha_fin = DateEntry(filtros_frame, date_pattern="dd/MM/yyyy",
                                       locale="es_ES", width=12, background="white")
        self.cal_fecha_fin.grid(row=0, column=5, padx=5, sticky="w")
        self.cal_fecha_fin.set_date(datetime.now())

        # Botón Aplicar Filtros
        ttk.Button(filtros_frame, text="🔍 Aplicar Filtros", command=self.aplicar_filtros,
                   style="TButton").grid(row=0, column=6, padx=10, sticky="e")

        # Tabla de notas
        columns = ("sede", "ciclo", "estudiante", "area", "nota", "fecha")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20, style="Treeview")

        # Configurar columnas con iconos
        self.tree.heading("sede", text="📍 Sede")
        self.tree.heading("ciclo", text="📅 Ciclo")
        self.tree.heading("estudiante", text="👤 Estudiante")
        self.tree.heading("area", text="📚 Área")
        self.tree.heading("nota", text="⭐ Nota")
        self.tree.heading("fecha", text="📆 Fecha")

        self.tree.column("sede", width=150, anchor="w")
        self.tree.column("ciclo", width=100, anchor="center")
        self.tree.column("estudiante", width=220, anchor="w")
        self.tree.column("area", width=80, anchor="center")
        self.tree.column("nota", width=80, anchor="center")
        self.tree.column("fecha", width=100, anchor="center")

        self.tree.grid(row=2, column=0, columnspan=6, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=6, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Botón Regresar
        ttk.Button(main_frame, text="← Regresar", command=self.destroy,
                   style="TButton").grid(row=3, column=0, columnspan=6, pady=20, sticky="e")

        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        filtro_area = self.combo_area.get()
        fecha_ini = self.cal_fecha_ini.get_date()
        fecha_fin = self.cal_fecha_fin.get_date()

        fecha_ini_str = fecha_ini.strftime("%Y-%m-%d")
        fecha_fin_str = fecha_fin.strftime("%Y-%m-%d")

        resultados = FuncionesColaborador.obtener_notas_estudiantes(
            self.id_colaborador,
            filtro_area,
            fecha_ini_str,
            fecha_fin_str
        )

        for item in self.tree.get_children():
            self.tree.delete(item)

        if resultados:
            for dato in resultados:
                if len(dato) >= 6:
                    fecha_original = dato[5]
                    try:
                        if isinstance(fecha_original, str):
                            fecha_dt = datetime.strptime(fecha_original, "%Y-%m-%d")
                            fecha_formateada = fecha_dt.strftime("%d/%m/%Y")
                            dato_lista = list(dato)
                            dato_lista[5] = fecha_formateada
                            dato = tuple(dato_lista)
                    except Exception as e:
                        print(f"Error al formatear fecha: {str(e)}")

                self.tree.insert("", "end", values=dato)
        else:
            messagebox.showinfo("Información ℹ️", "No se encontraron registros con los filtros seleccionados")

    def aplicar_filtros(self):
        self.cargar_datos()


class MenuColaborador(tk.Tk):
    def __init__(self, nombre_colaborador, id_colaborador):
        super().__init__()
        self.title(f"👤 Panel de {nombre_colaborador}")
        self.geometry("1000x700")
        self.resizable(False, False)
        self.nombre_colab = nombre_colaborador
        self.id_colab = id_colaborador

        # Configurar estilos
        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TFrame", background=BACKGROUND_COLOR)
        self.style.configure("Header.TFrame", background=PRIMARY_COLOR)
        self.style.configure("Title.TLabel", background=PRIMARY_COLOR, foreground="white",
                             font=("Arial", 18, "bold"))
        self.style.configure("TButton", background=PRIMARY_COLOR, foreground="white",
                             font=("Arial", 12, "bold"), borderwidth=0, padding=10)
        self.style.map("TButton", background=[("active", BUTTON_HOVER), ("pressed", PRIMARY_COLOR)])
        self.style.configure("MenuButton.TButton", background=PRIMARY_COLOR, foreground="white",
                             font=("Arial", 14, "bold"), padding=(20, 15), width=25)
        self.style.map("MenuButton.TButton", background=[("active", BUTTON_HOVER), ("pressed", PRIMARY_COLOR)])

        # Frame principal
        self.frame_principal = ttk.Frame(self, style="TFrame")
        self.frame_principal.pack(fill="both", expand=True)
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.rowconfigure(1, weight=1)

        # Header
        self.crear_header()

        # Área de botones
        self.crear_area_botones()

    def crear_header(self):
        header = ttk.Frame(self.frame_principal, style="Header.TFrame", padding=(30, 20, 30, 30))
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(1, weight=1)

        # Título con icono
        title_label = ttk.Label(header,
                                text=f"👋 Bienvenido, {self.nombre_colab}",
                                style="Title.TLabel")
        title_label.grid(row=0, column=0, sticky="w")

        # Botón de salir con icono
        btn_salir = ttk.Button(header, text="🚪 Salir",
                               style="TButton",
                               command=self.salir)
        btn_salir.grid(row=0, column=1, sticky="e")

    def crear_area_botones(self):
        area_botones = ttk.Frame(self.frame_principal, style="TFrame", padding=50)
        area_botones.grid(row=1, column=0, sticky="nsew")
        area_botones.columnconfigure(0, weight=1)

        # Frame interno para centrar
        center_frame = ttk.Frame(area_botones, style="TFrame")
        center_frame.pack(expand=True)

        # Botones con iconos
        botones_info = [
            ("✅", "Registrar Asistencia", self.registrar_asistencia),
            ("📝", "Registrar Calificaciones", self.registrar_calificaciones),
            ("📊", "Ver Reporte de Notas", self.ver_examenes)
        ]

        for idx, (icono, texto, comando) in enumerate(botones_info):
            btn_frame = ttk.Frame(center_frame, style="TFrame")
            btn_frame.pack(pady=20, fill="x")

            btn = ttk.Button(btn_frame,
                             text=f"{icono}  {texto}",
                             style="MenuButton.TButton",
                             command=comando)
            btn.pack(ipadx=20, ipady=15)

    def registrar_asistencia(self):
        ventana = VentanaRegistrarAsistencia(self, self.id_colab)
        ventana.grab_set()

    def registrar_calificaciones(self):
        ventana = VentanaRegistrarCalificacion(self)
        ventana.grab_set()

    def ver_examenes(self):
        ventana = VentanaNotasEstudiantes(self, self.id_colab)
        ventana.grab_set()

    def salir(self):
        self.quit()
        self.destroy()

    def mostrar(self):
        self.mainloop()