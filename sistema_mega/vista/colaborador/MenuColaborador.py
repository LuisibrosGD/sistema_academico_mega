import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from sistema_mega.modelo.colaborador_modelo import FuncionesColaborador


class VentanaRegistrarAsistencia(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Asistencia")
        self.geometry("500x350")
        self.resizable(False, False)

        # Frame principal
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Título
        ttk.Label(main_frame, text="Registrar Asistencia",
                  font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Profesor
        ttk.Label(main_frame, text="Profesor:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)

        # Obtener profesores con cursos
        profesores = FuncionesColaborador.obtener_profesores_con_cursos()
        self.profesores_dict = {}
        valores_combo = []

        if profesores:
            for profesor in profesores:
                if len(profesor) >= 3:
                    id_prof, nombre, curso = profesor[:3]
                    texto = f"{nombre} - {curso}"
                    valores_combo.append(texto)
                    self.profesores_dict[texto] = id_prof
                else:
                    print(f"Formato inesperado: {profesor}")
        else:
            print("No se encontraron profesores con cursos asignados")

        self.combo_profesor = ttk.Combobox(main_frame, values=valores_combo,
                                           state="readonly", width=40)
        self.combo_profesor.grid(row=1, column=1, sticky="ew", pady=5, padx=(0, 10))

        if valores_combo:
            self.combo_profesor.current(0)
        else:
            self.combo_profesor.set("No hay profesores disponibles")
            messagebox.showwarning("Advertencia", "No hay profesores disponibles para seleccionar")

        # Estado de Asistencia
        ttk.Label(main_frame, text="Estado de Asistencia:",
                  font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.estado_var = tk.StringVar(value="presente")

        frame_estados = ttk.Frame(main_frame)
        frame_estados.grid(row=2, column=1, sticky="w", pady=5)

        ttk.Radiobutton(frame_estados, text="Presente", variable=self.estado_var,
                        value="presente").pack(anchor="w")
        ttk.Radiobutton(frame_estados, text="Tarde", variable=self.estado_var,
                        value="tarde").pack(anchor="w")
        ttk.Radiobutton(frame_estados, text="Ausente", variable=self.estado_var,
                        value="ausente").pack(anchor="w")

        # Fecha (con selector de calendario)
        ttk.Label(main_frame, text="Fecha:",
                  font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=10)
        self.cal_fecha = DateEntry(main_frame,
                                   date_pattern="dd/MM/yyyy",
                                   locale="es_ES",
                                   width=12)
        self.cal_fecha.grid(row=3, column=1, sticky="w", pady=10)
        self.cal_fecha.set_date(datetime.now())

        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Confirmar", command=self.registrar,
                   width=10).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy,
                   width=10).pack(side="left", padx=10)

        # Configurar grid
        main_frame.columnconfigure(1, weight=1)

    def registrar(self):
        profesor_texto = self.combo_profesor.get()
        estado = self.estado_var.get()
        fecha = self.cal_fecha.get_date()

        if not profesor_texto or "No hay profesores" in profesor_texto:
            messagebox.showerror("Error", "No hay profesores disponibles para seleccionar")
            return

        id_profesor = self.profesores_dict.get(profesor_texto)
        if not id_profesor:
            messagebox.showerror("Error", "Profesor no válido")
            return

        # Convertir fecha a formato YYYY-MM-DD HH:MM:SS
        fecha_dt = datetime.combine(fecha, datetime.min.time())
        fecha_str = fecha_dt.strftime("%Y-%m-%d %H:%M:%S")

        # Registrar asistencia con fecha seleccionada
        success, mensaje = FuncionesColaborador.registrar_asistencia(estado, id_profesor, fecha_str)
        if success:
            messagebox.showinfo("Éxito", mensaje)
            self.destroy()
        else:
            messagebox.showerror("Error", mensaje)


class VentanaRegistrarCalificacion(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registrar Calificación")
        self.geometry("500x400")
        self.resizable(False, False)

        # Frame principal
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill="both", expand=True)

        # Título
        ttk.Label(main_frame, text="Registrar Calificación",
                  font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Estudiante
        ttk.Label(main_frame, text="Estudiante:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)

        # Obtener estudiantes
        estudiantes = FuncionesColaborador.obtener_estudiantes()
        self.estudiantes_dict = {}
        valores_combo = []

        for estudiante in estudiantes:
            id_est, nombre = estudiante
            valores_combo.append(nombre)
            self.estudiantes_dict[nombre] = id_est

        self.combo_estudiante = ttk.Combobox(main_frame, values=valores_combo,
                                             state="readonly", width=35)
        self.combo_estudiante.grid(row=1, column=1, sticky="ew", pady=5)
        if valores_combo:
            self.combo_estudiante.current(0)
        else:
            self.combo_estudiante.set("No hay estudiantes disponibles")

        # Puntaje
        ttk.Label(main_frame, text="Puntaje (0.00 - 2000.00):",
                  font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.entry_puntaje = ttk.Entry(main_frame)
        self.entry_puntaje.grid(row=2, column=1, sticky="ew", pady=5)

        # Fecha de evaluación (con selector de calendario)
        ttk.Label(main_frame, text="Fecha de evaluación:",
                  font=("Arial", 10)).grid(row=3, column=0, sticky="w", pady=5)
        self.cal_fecha = DateEntry(main_frame,
                                   date_pattern="dd/MM/yyyy",
                                   locale="es_ES",
                                   width=12)
        self.cal_fecha.grid(row=3, column=1, sticky="w", pady=5)
        self.cal_fecha.set_date(datetime.now())

        # Botones
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        ttk.Button(btn_frame, text="Guardar", command=self.registrar,
                   width=10).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="Cancelar", command=self.destroy,
                   width=10).pack(side="left", padx=10)

        # Configurar grid
        main_frame.columnconfigure(1, weight=1)

    def registrar(self):
        estudiante_nombre = self.combo_estudiante.get()
        puntaje = self.entry_puntaje.get()
        fecha = self.cal_fecha.get_date()

        if not estudiante_nombre or "No hay estudiantes" in estudiante_nombre:
            messagebox.showerror("Error", "No hay estudiantes disponibles para seleccionar")
            return

        if not puntaje:
            messagebox.showerror("Error", "Ingrese un puntaje")
            return

        try:
            puntaje = float(puntaje)
            if puntaje < 0 or puntaje > 2000:
                raise ValueError("Puntaje fuera de rango")
        except ValueError:
            messagebox.showerror("Error", "Ingrese un puntaje válido (0.00 - 2000.00)")
            return

        # Convertir fecha a formato YYYY-MM-DD
        fecha_str = fecha.strftime("%Y-%m-%d")

        id_estudiante = self.estudiantes_dict.get(estudiante_nombre)
        if not id_estudiante:
            messagebox.showerror("Error", "Estudiante no válido")
            return

        success, mensaje = FuncionesColaborador.registrar_calificacion(
            id_estudiante,
            puntaje,
            fecha_str
        )
        if success:
            messagebox.showinfo("Éxito", mensaje)
            self.destroy()
        else:
            messagebox.showerror("Error", mensaje)


class VentanaNotasEstudiantes(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Notas de Estudiantes")
        self.geometry("1000x600")
        self.resizable(True, True)

        # Frame principal
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill="both", expand=True)

        # Título
        ttk.Label(main_frame, text="Notas de Estudiantes - Año Actual",
                  font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=6, pady=(0, 15))

        # Filtros
        filtros_frame = ttk.LabelFrame(main_frame, text="Filtros", padding=10)
        filtros_frame.grid(row=1, column=0, columnspan=6, sticky="ew", pady=(0, 15))

        # Área Académica
        ttk.Label(filtros_frame, text="Área Académica:").grid(row=0, column=0, padx=5, sticky="w")
        areas = FuncionesColaborador.obtener_areas_academicas()
        self.combo_area = ttk.Combobox(filtros_frame, values=areas,
                                       state="readonly", width=5)
        self.combo_area.grid(row=0, column=1, padx=5, sticky="w")
        self.combo_area.set("Todas")

        # Fecha Inicio (con selector de calendario)
        ttk.Label(filtros_frame, text="Fecha Inicio:").grid(row=0, column=2, padx=5, sticky="w")
        self.cal_fecha_ini = DateEntry(filtros_frame,
                                       date_pattern="dd/MM/yyyy",
                                       locale="es_ES",
                                       width=12)
        self.cal_fecha_ini.grid(row=0, column=3, padx=5, sticky="w")
        self.cal_fecha_ini.set_date(datetime(2025, 1, 1))

        # Fecha Fin (con selector de calendario)
        ttk.Label(filtros_frame, text="Fecha Fin:").grid(row=0, column=4, padx=5, sticky="w")
        self.cal_fecha_fin = DateEntry(filtros_frame,
                                       date_pattern="dd/MM/yyyy",
                                       locale="es_ES",
                                       width=12)
        self.cal_fecha_fin.grid(row=0, column=5, padx=5, sticky="w")
        self.cal_fecha_fin.set_date(datetime.now())

        # Botón Aplicar Filtros
        ttk.Button(filtros_frame, text="Aplicar Filtros",
                   command=self.aplicar_filtros).grid(row=0, column=6, padx=10)

        # Tabla de notas
        columns = ("sede", "ciclo", "estudiante", "area", "nota", "fecha")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=20)

        # Configurar columnas
        self.tree.heading("sede", text="Sede")
        self.tree.heading("ciclo", text="Ciclo")
        self.tree.heading("estudiante", text="Nombre Completo")
        self.tree.heading("area", text="Área Académica")
        self.tree.heading("nota", text="Nota")
        self.tree.heading("fecha", text="Fecha")

        self.tree.column("sede", width=120, anchor="w")
        self.tree.column("ciclo", width=80, anchor="center")
        self.tree.column("estudiante", width=180, anchor="w")
        self.tree.column("area", width=100, anchor="center")
        self.tree.column("nota", width=80, anchor="center")
        self.tree.column("fecha", width=100, anchor="center")

        self.tree.grid(row=2, column=0, columnspan=6, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=2, column=6, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Botón Regresar
        ttk.Button(main_frame, text="Regresar a Menú principal",
                   command=self.destroy).grid(row=3, column=0, columnspan=6, pady=20)

        # Configurar grid
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Cargar datos iniciales
        self.cargar_datos()

    def cargar_datos(self):
        # Obtener valores de los filtros
        filtro_area = self.combo_area.get()
        fecha_ini = self.cal_fecha_ini.get_date()
        fecha_fin = self.cal_fecha_fin.get_date()

        # Convertir fechas a formato YYYY-MM-DD
        fecha_ini_str = fecha_ini.strftime("%Y-%m-%d")
        fecha_fin_str = fecha_fin.strftime("%Y-%m-%d")

        # Obtener datos de la base de datos
        resultados = FuncionesColaborador.obtener_notas_estudiantes(
            None, filtro_area, fecha_ini_str, fecha_fin_str
        )

        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insertar datos
        if resultados:
            for dato in resultados:
                # Convertir fecha al formato DD/MM/AAAA
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
                        # Mantener la fecha original si hay error

                self.tree.insert("", "end", values=dato)
        else:
            messagebox.showinfo("Información", "No se encontraron registros con los filtros seleccionados")

    def aplicar_filtros(self):
        self.cargar_datos()

class MenuColaborador(tk.Toplevel):
    def __init__(self, id_colaborador, nombre_colaborador):
        super().__init__()

        self.title("Colaborador")
        self.geometry("1000x700")
        self.configure(bg="#f0f0f0")
        self.id_colaborador = id_colaborador
        self.nombre_colaborador = nombre_colaborador
        self.frame_principal = None  # Inicializar atributo

        # Configurar el grid principal
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.configurar_estilos()
        self.crear_widgets()



    @staticmethod
    def configurar_estilos():
        """Configurar los estilos de la interfaz"""
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Estilo para el frame principal
        estilo.configure("frameColaborador.TFrame", background="#f0f0f0")

        # Estilo para el header
        estilo.configure("headerColaborador.TFrame", background="#4a90e2")

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

    def crear_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        self.frame_principal = ttk.Frame(self, style="frameColaborador.TFrame")
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
        header_frame = ttk.Frame(self.frame_principal, style="headerColaborador.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)

        # Configurar padding interno
        header_frame.configure(padding=(20, 15))

        # Título del menú
        titulo_label = ttk.Label(header_frame,
                                 text=f"Panel Colaborador [{self.nombre_colaborador}]",
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
        botones_frame = ttk.Frame(self.frame_principal, style="frameColaborador.TFrame")
        botones_frame.grid(row=1, column=0, sticky="nsew")

        # Configurar grid para centrar los botones
        botones_frame.rowconfigure(0, weight=1)
        botones_frame.rowconfigure(1, weight=0)
        botones_frame.rowconfigure(2, weight=0)
        botones_frame.rowconfigure(3, weight=0)
        botones_frame.rowconfigure(4, weight=1)
        botones_frame.columnconfigure(0, weight=1)
        botones_frame.columnconfigure(1, weight=0)
        botones_frame.columnconfigure(2, weight=1)

        # Datos de los botones específicos para colaborador
        botones_info = [
            ("✅", "Registrar Asistencia", self.registrar_asistencia),
            ("📝", "Registrar Calificaciones", self.registrar_calificaciones),
            ("📊", "Ver Exámenes", self.ver_examenes)
        ]

        # Crear los botones
        for i, (icono, texto, comando) in enumerate(botones_info):
            self.crear_boton_menu(botones_frame, icono, texto, comando, i + 1)

    @staticmethod
    def crear_boton_menu(parent, icono, texto, comando, fila):
        """Crear un botón del menú con icono y texto"""
        boton_frame = ttk.Frame(parent, style="frameColaborador.TFrame")
        boton_frame.grid(row=fila, column=1, sticky="ew", pady=10)
        boton_frame.configure(padding=(0, 0))

        boton_frame.columnconfigure(0, weight=1)

        boton = ttk.Button(boton_frame,
                           text=f"{icono}  {texto}",
                           style="botonMenu.TButton",
                           command=comando,
                           width=25)
        boton.grid(row=0, column=0, sticky="ew")

    # Métodos para los comandos de los botones
    def registrar_asistencia(self):
        """Abrir ventana para registrar asistencia"""
        ventana = VentanaRegistrarAsistencia(self)
        ventana.grab_set()

    def registrar_calificaciones(self):
        """Abrir ventana para registrar calificaciones"""
        ventana = VentanaRegistrarCalificacion(self)
        ventana.grab_set()

    def ver_examenes(self):
        """Abrir ventana para ver exámenes"""
        ventana = VentanaNotasEstudiantes(self)
        ventana.grab_set()

    def salir(self):
        """Método para salir/cerrar sesión"""
        print("Cerrando sesión de colaborador...")
        self.quit()


    def mostrar(self):
        """Mostrar la ventana"""
        self.mainloop()


