import tkinter as tk
from tkinter import ttk, messagebox
from sistema_mega.modelo.modelo_grupos import *


class VistaInformacionGrupo(tk.Toplevel):
    def __init__(self, parent, grupo_info):
        super().__init__(parent)
        self.parent = parent
        self.grupo_info = grupo_info
        self.resumen_grupo = None

        # Configuración de la ventana
        self.title(f"Información del Grupo - {grupo_info[1]}")
        self.geometry("1400x900")
        self.configure(bg="#f0f0f0")

        # Hacer ventana modal
        self.transient(parent)
        self.grab_set()

        # Configurar protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Variables para filtros
        self.area_filtro = tk.StringVar(value="Todas")
        self.estudiantes_filtrados = []

        # Configurar grid principal
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Configurar estilos
        self.configurar_estilos()

        # Crear widgets
        self.crear_widgets()

        # Cargar datos
        self.cargar_informacion()

    def configurar_estilos(self):
        """Configurar estilos de la interfaz"""
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")

        # Estilo para el frame principal
        self.estilo.configure("frameInfo.TFrame", background="#f0f0f0")

        # Estilo para títulos
        self.estilo.configure("tituloInfo.TLabel",
                              background="#f0f0f0",
                              foreground="#2c3e50",
                              font=("Arial", 20, "bold"))

        # Estilo para subtítulos
        self.estilo.configure("subtituloInfo.TLabel",
                              background="#f0f0f0",
                              foreground="#34495e",
                              font=("Arial", 14, "bold"))

        # Estilo para información general
        self.estilo.configure("infoGeneral.TLabel",
                              background="#f0f0f0",
                              foreground="#5a6c7d",
                              font=("Arial", 12))

        # Estilo para header de información
        self.estilo.configure("headerInfo.TFrame",
                              background="#3498db",
                              relief="flat")

        # Estilo para labels del header
        self.estilo.configure("headerInfoLabel.TLabel",
                              background="#3498db",
                              foreground="white",
                              font=("Arial", 12, "bold"))

        # Estilo para estadísticas
        self.estilo.configure("estadistica.TLabel",
                              background="#e8f4f8",
                              foreground="#2980b9",
                              font=("Arial", 11, "bold"),
                              relief="solid",
                              borderwidth=1,
                              padding=5)

        # Estilo para el treeview
        self.estilo.configure("Treeview",
                              background="#ffffff",
                              foreground="#2c3e50",
                              fieldbackground="#ffffff",
                              font=("Arial", 10))

        self.estilo.configure("Treeview.Heading",
                              background="#34495e",
                              foreground="white",
                              font=("Arial", 11, "bold"))

        # Estilo para botones
        self.estilo.configure("botonCerrar.TButton",
                              background="#95a5a6",
                              foreground="white",
                              font=("Arial", 11, "bold"),
                              relief="flat")

        self.estilo.map("botonCerrar.TButton",
                        background=[("pressed", "#7f8c8d"), ("active", "#a2b1b3")])

        # Estilo para filtros
        self.estilo.configure("filtroLabel.TLabel",
                              background="#f0f0f0",
                              foreground="#2c3e50",
                              font=("Arial", 11, "bold"))

    def crear_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self, style="frameInfo.TFrame")
        main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Crear header con información del grupo
        self.crear_header_informacion(main_frame)

        # Frame para contenido con scroll
        self.crear_contenido_scroll(main_frame)

        # Botón cerrar
        self.crear_boton_cerrar(main_frame)

    def crear_header_informacion(self, parent):
        """Crear el header con información básica del grupo"""
        header_frame = ttk.Frame(parent, style="headerInfo.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.configure(padding=(20, 15))

        # Configurar grid
        header_frame.columnconfigure(0, weight=1)
        header_frame.columnconfigure(1, weight=1)

        # Título del grupo
        titulo_label = ttk.Label(header_frame,
                                 text=f"Grupo: {self.grupo_info[1]}",
                                 style="headerInfoLabel.TLabel")
        titulo_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Colaborador asignado
        colaborador_label = ttk.Label(header_frame,
                                      text=f"Docente: {self.grupo_info[5]}",
                                      style="headerInfoLabel.TLabel")
        colaborador_label.grid(row=1, column=0, sticky="w", pady=(0, 5))

        # Ciclo
        ciclo_label = ttk.Label(header_frame,
                                text=f"Ciclo: {self.grupo_info[6]}",
                                style="headerInfoLabel.TLabel")
        ciclo_label.grid(row=2, column=0, sticky="w")

        # Frame para estadísticas
        self.stats_frame = ttk.Frame(header_frame, style="frameInfo.TFrame")
        self.stats_frame.grid(row=0, column=1, rowspan=3, sticky="nsew", padx=(20, 0))
        self.stats_frame.columnconfigure(0, weight=1)
        self.stats_frame.columnconfigure(1, weight=1)

    def crear_contenido_scroll(self, parent):
        """Crear el área de contenido con scroll"""
        # Frame contenedor
        container_frame = ttk.Frame(parent, style="frameInfo.TFrame")
        container_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        container_frame.rowconfigure(0, weight=1)
        container_frame.columnconfigure(0, weight=1)

        # Canvas para scroll
        self.canvas = tk.Canvas(container_frame, bg="#f0f0f0", highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbar
        scrollbar = ttk.Scrollbar(container_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        # Frame interno
        self.content_frame = ttk.Frame(self.canvas, style="frameInfo.TFrame")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")

        # Configurar scroll
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

        # Configurar grid del contenido
        self.content_frame.columnconfigure(0, weight=1)

        # Crear secciones
        self.crear_seccion_cursos()
        self.crear_seccion_estudiantes()

    def crear_seccion_cursos(self):
        """Crear la sección de cursos"""
        # Frame para cursos
        cursos_frame = ttk.Frame(self.content_frame, style="frameInfo.TFrame")
        cursos_frame.grid(row=0, column=0, sticky="ew", pady=(0, 30))
        cursos_frame.columnconfigure(0, weight=1)

        # Título de la sección
        titulo_cursos = ttk.Label(cursos_frame,
                                  text="Cursos Asignados",
                                  style="subtituloInfo.TLabel")
        titulo_cursos.grid(row=0, column=0, sticky="w", pady=(0, 15))

        # Treeview para cursos
        self.crear_tabla_cursos(cursos_frame)

    def crear_tabla_cursos(self, parent):
        """Crear la tabla de cursos"""
        # Frame para la tabla
        tabla_frame = ttk.Frame(parent, style="frameInfo.TFrame")
        tabla_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        tabla_frame.columnconfigure(0, weight=1)

        # Definir columnas
        columnas_cursos = ("Curso", "Día", "Hora Inicio", "Hora Fin", "Profesor")

        # Crear Treeview
        self.tree_cursos = ttk.Treeview(tabla_frame,
                                        columns=columnas_cursos,
                                        show="headings",
                                        height=6)

        # Configurar columnas
        self.tree_cursos.heading("Curso", text="Curso")
        self.tree_cursos.heading("Día", text="Día")
        self.tree_cursos.heading("Hora Inicio", text="Hora Inicio")
        self.tree_cursos.heading("Hora Fin", text="Hora Fin")
        self.tree_cursos.heading("Profesor", text="Profesor")

        # Configurar anchos
        self.tree_cursos.column("Curso", width=300, anchor="w")
        self.tree_cursos.column("Día", width=100, anchor="center")
        self.tree_cursos.column("Hora Inicio", width=120, anchor="center")
        self.tree_cursos.column("Hora Fin", width=120, anchor="center")
        self.tree_cursos.column("Profesor", width=300, anchor="w")

        # Scrollbar para cursos
        scrollbar_cursos = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree_cursos.yview)
        self.tree_cursos.configure(yscrollcommand=scrollbar_cursos.set)

        # Grid
        self.tree_cursos.grid(row=0, column=0, sticky="ew")
        scrollbar_cursos.grid(row=0, column=1, sticky="ns")

    def crear_seccion_estudiantes(self):
        """Crear la sección de estudiantes"""
        # Frame para estudiantes
        estudiantes_frame = ttk.Frame(self.content_frame, style="frameInfo.TFrame")
        estudiantes_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        estudiantes_frame.columnconfigure(0, weight=1)

        # Header con título y filtros
        header_estudiantes = ttk.Frame(estudiantes_frame, style="frameInfo.TFrame")
        header_estudiantes.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        header_estudiantes.columnconfigure(0, weight=1)

        # Título
        titulo_estudiantes = ttk.Label(header_estudiantes,
                                       text="Lista de Estudiantes",
                                       style="subtituloInfo.TLabel")
        titulo_estudiantes.grid(row=0, column=0, sticky="w", pady=(0, 10))

        # Filtros
        self.crear_filtros_estudiantes(header_estudiantes)

        # Tabla de estudiantes
        self.crear_tabla_estudiantes(estudiantes_frame)

    def crear_filtros_estudiantes(self, parent):
        """Crear los filtros para estudiantes"""
        filtros_frame = ttk.Frame(parent, style="frameInfo.TFrame")
        filtros_frame.grid(row=1, column=0, sticky="w", pady=(0, 10))

        # Label para filtro
        filtro_label = ttk.Label(filtros_frame,
                                 text="Filtrar por Área Académica:",
                                 style="filtroLabel.TLabel")
        filtro_label.grid(row=0, column=0, padx=(0, 10))

        # Combobox para áreas
        self.combo_areas = ttk.Combobox(filtros_frame,
                                        textvariable=self.area_filtro,
                                        state="readonly",
                                        width=15)
        self.combo_areas.grid(row=0, column=1, padx=(0, 10))

        # Bind del cambio de filtro
        self.combo_areas.bind("<<ComboboxSelected>>", self.aplicar_filtro_area)

        # Botón para limpiar filtro
        btn_limpiar = ttk.Button(filtros_frame,
                                 text="Mostrar Todos",
                                 command=self.limpiar_filtro)
        btn_limpiar.grid(row=0, column=2)

    def crear_tabla_estudiantes(self, parent):
        """Crear la tabla de estudiantes"""
        # Frame para la tabla
        tabla_frame = ttk.Frame(parent, style="frameInfo.TFrame")
        tabla_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        tabla_frame.columnconfigure(0, weight=1)

        # Definir columnas
        columnas_estudiantes = ("Nombre Completo", "Área Académica", "Tipo Doc.", "Nro. Documento", "Fecha Inscripción")

        # Crear Treeview
        self.tree_estudiantes = ttk.Treeview(tabla_frame,
                                             columns=columnas_estudiantes,
                                             show="headings",
                                             height=10)

        # Configurar columnas
        self.tree_estudiantes.heading("Nombre Completo", text="Nombre Completo")
        self.tree_estudiantes.heading("Área Académica", text="Área Académica")
        self.tree_estudiantes.heading("Tipo Doc.", text="Tipo Doc.")
        self.tree_estudiantes.heading("Nro. Documento", text="Nro. Documento")
        self.tree_estudiantes.heading("Fecha Inscripción", text="Fecha Inscripción")

        # Configurar anchos
        self.tree_estudiantes.column("Nombre Completo", width=300, anchor="w")
        self.tree_estudiantes.column("Área Académica", width=120, anchor="center")
        self.tree_estudiantes.column("Tipo Doc.", width=100, anchor="center")
        self.tree_estudiantes.column("Nro. Documento", width=150, anchor="center")
        self.tree_estudiantes.column("Fecha Inscripción", width=150, anchor="center")

        # Scrollbar para estudiantes
        scrollbar_estudiantes = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tree_estudiantes.yview)
        self.tree_estudiantes.configure(yscrollcommand=scrollbar_estudiantes.set)

        # Grid
        self.tree_estudiantes.grid(row=0, column=0, sticky="ew")
        scrollbar_estudiantes.grid(row=0, column=1, sticky="ns")

    def crear_boton_cerrar(self, parent):
        """Crear el botón de cerrar"""
        btn_cerrar = ttk.Button(parent,
                                text="Cerrar",
                                style="botonCerrar.TButton",
                                command=self.on_closing)
        btn_cerrar.grid(row=2, column=0, pady=(10, 0))

    def cargar_informacion(self):
        """Cargar toda la información del grupo"""
        try:
            # Obtener resumen completo del grupo
            id_grupo = self.grupo_info[0]
            self.resumen_grupo = obtener_resumen_grupo_completo(id_grupo)

            if self.resumen_grupo:
                # Actualizar estadísticas en el header
                self.actualizar_estadisticas()

                # Cargar cursos
                self.cargar_cursos()

                # Cargar estudiantes
                self.cargar_estudiantes()

                # Cargar áreas disponibles para filtro
                self.cargar_areas_filtro()
            else:
                messagebox.showerror("Error", "No se pudo cargar la información del grupo")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar información: {str(e)}")
            print(f" Error al cargar información del grupo: {e}")

    def actualizar_estadisticas(self):
        """Actualizar las estadísticas en el header"""
        if not self.resumen_grupo:
            return

        stats = self.resumen_grupo['estadisticas']

        # Limpiar frame de estadísticas
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Capacidad total
        capacidad_label = ttk.Label(self.stats_frame,
                                    text=f"Capacidad: {self.grupo_info[2]}",
                                    style="estadistica.TLabel")
        capacidad_label.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=(0, 5))

        # Estudiantes inscritos
        estudiantes_label = ttk.Label(self.stats_frame,
                                      text=f"Estudiantes: {stats['total_estudiantes']}",
                                      style="estadistica.TLabel")
        estudiantes_label.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=(0, 5))

        # Espacios disponibles
        espacios_label = ttk.Label(self.stats_frame,
                                   text=f"Espacios libres: {stats['espacios_disponibles']}",
                                   style="estadistica.TLabel")
        espacios_label.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=(0, 5))

        # Cursos asignados
        cursos_label = ttk.Label(self.stats_frame,
                                 text=f"Cursos: {stats['total_cursos']}",
                                 style="estadistica.TLabel")
        cursos_label.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=(0, 5))

        # Porcentaje de ocupación
        ocupacion_label = ttk.Label(self.stats_frame,
                                    text=f"Ocupación: {stats['porcentaje_ocupacion']}%",
                                    style="estadistica.TLabel")
        ocupacion_label.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(0, 5))

    def cargar_cursos(self):
        """Cargar los cursos en la tabla"""
        # Limpiar tabla
        for item in self.tree_cursos.get_children():
            self.tree_cursos.delete(item)

        # Cargar cursos
        cursos = self.resumen_grupo['cursos']
        for curso in cursos:
            # Estructura: (id_curso, nombre_curso, dia, hora_inicio, hora_fin, nombre_profesor, id_profesor)
            self.tree_cursos.insert("", "end", values=(
                curso[1],  # nombre_curso
                curso[2].capitalize(),  # dia
                curso[3],  # hora_inicio
                curso[4],  # hora_fin
                curso[5]  # nombre_profesor
            ))

    def cargar_estudiantes(self):
        """Cargar los estudiantes en la tabla"""
        # Limpiar tabla
        for item in self.tree_estudiantes.get_children():
            self.tree_estudiantes.delete(item)

        # Cargar estudiantes
        estudiantes = self.resumen_grupo['estudiantes']
        self.estudiantes_filtrados = estudiantes

        for estudiante in estudiantes:
            # Estructura: (id_estudiante, nombre_completo, area_academica, tipo_documento, nro_documento, fecha_inscripcion, id_inscripcion)
            fecha_inscripcion = estudiante[5].strftime("%d/%m/%Y") if estudiante[5] else "N/A"

            self.tree_estudiantes.insert("", "end", values=(
                estudiante[1],  # nombre_completo
                estudiante[2].upper() if estudiante[2] else "N/A",  # area_academica
                estudiante[3] if estudiante[3] else "N/A",  # tipo_documento
                estudiante[4] if estudiante[4] else "N/A",  # nro_documento
                fecha_inscripcion
            ))

    def cargar_areas_filtro(self):
        """Cargar las áreas académicas disponibles en el filtro"""
        try:
            # Obtener áreas únicas de los estudiantes del grupo
            areas_estudiantes = set()
            for estudiante in self.resumen_grupo['estudiantes']:
                if estudiante[2]:  # area_academica
                    areas_estudiantes.add(estudiante[2].upper())

            # Preparar lista de opciones
            opciones = ["Todas"] + sorted(list(areas_estudiantes))

            # Configurar combobox
            self.combo_areas['values'] = opciones
            self.combo_areas.set("Todas")

        except Exception as e:
            print(f"❌ Error al cargar áreas para filtro: {e}")

    def aplicar_filtro_area(self, event=None):
        """Aplicar filtro por área académica"""
        area_seleccionada = self.area_filtro.get()

        # Limpiar tabla
        for item in self.tree_estudiantes.get_children():
            self.tree_estudiantes.delete(item)

        # Filtrar estudiantes
        if area_seleccionada == "Todas":
            estudiantes_mostrar = self.resumen_grupo['estudiantes']
        else:
            estudiantes_mostrar = [
                est for est in self.resumen_grupo['estudiantes']
                if est[2] and est[2].upper() == area_seleccionada
            ]

        # Mostrar estudiantes filtrados
        for estudiante in estudiantes_mostrar:
            fecha_inscripcion = estudiante[5].strftime("%d/%m/%Y") if estudiante[5] else "N/A"

            self.tree_estudiantes.insert("", "end", values=(
                estudiante[1],  # nombre_completo
                estudiante[2].upper() if estudiante[2] else "N/A",  # area_academica
                estudiante[3] if estudiante[3] else "N/A",  # tipo_documento
                estudiante[4] if estudiante[4] else "N/A",  # nro_documento
                fecha_inscripcion
            ))

    def limpiar_filtro(self):
        """Limpiar el filtro y mostrar todos los estudiantes"""
        self.area_filtro.set("Todas")
        self.aplicar_filtro_area()

    def on_frame_configure(self, event):
        """Configurar scroll cuando cambia el frame"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Configurar canvas cuando cambia de tamaño"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def on_mousewheel(self, event):
        """Manejar scroll con rueda del mouse"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_closing(self):
        """Cerrar la ventana"""
        self.destroy()


def mostrar_informacion_grupo(parent, grupo_info):
    """
    Función para mostrar la ventana de información del grupo

    """
    try:
        ventana = VistaInformacionGrupo(parent, grupo_info)
        return ventana
    except Exception as e:
        messagebox.showerror("Error", f"Error al mostrar información del grupo: {str(e)}")
        print(f" Error al mostrar información del grupo: {e}")
        return None