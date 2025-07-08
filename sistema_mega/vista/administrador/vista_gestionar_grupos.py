import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from sistema_mega.modelo.modelo_grupos import *
from sistema_mega.vista.administrador.VistaCrearGrupo import *
from sistema_mega.vista.administrador.VistaEditarGrupo import *
from sistema_mega.vista.administrador.VistaInformacionGrupo import *
class VistaGestionarGrupos(tk.Toplevel):
    def __init__(self, parent, ciclo_info=None):
        super().__init__(parent)
        self.parent = parent
        self.ciclo_info = ciclo_info
        self.title("Gestionar Grupos")
        self.geometry("1200x800")
        self.configure(bg="#f0f0f0")

        # Configurar el protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Hacer que la ventana sea modal
        self.transient(parent)
        self.grab_set()

        # Variables
        self.grupos_data = []
        self.grupo_seleccionado = None

        # Configurar el grid principal
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.configurar_estilos()
        self.crear_widgets()

    def configurar_estilos(self):
        """Configurar los estilos de la interfaz"""
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")

        # Estilo para el frame principal
        self.estilo.configure("framePrincipal.TFrame",
                              background="#f0f0f0")

        # Estilo para el título
        self.estilo.configure("tituloGrupos.TLabel",
                              background="#f0f0f0",
                              foreground="#333333",
                              font=("Arial", 24, "bold"))

        # Estilo para el subtítulo
        self.estilo.configure("subtituloGrupos.TLabel",
                              background="#f0f0f0",
                              foreground="#666666",
                              font=("Arial", 14))

        # Estilo para las tarjetas de grupos
        self.estilo.configure("grupoCard.TFrame",
                              background="#28a745",
                              relief="raised",
                              borderwidth=2)

        # Estilo para tarjeta seleccionada
        self.estilo.configure("grupoCardSeleccionada.TFrame",
                              background="#1e7e34",
                              relief="raised",
                              borderwidth=3)

        # Estilo para el texto de los grupos
        self.estilo.configure("grupoNombre.TLabel",
                              background="#28a745",
                              foreground="white",
                              font=("Arial", 14, "bold"))

        self.estilo.configure("grupoInfo.TLabel",
                              background="#28a745",
                              foreground="white",
                              font=("Arial", 12))

        # Estilo para el texto de grupo seleccionado
        self.estilo.configure("grupoNombreSeleccionado.TLabel",
                              background="#1e7e34",
                              foreground="white",
                              font=("Arial", 14, "bold"))

        self.estilo.configure("grupoInfoSeleccionado.TLabel",
                              background="#1e7e34",
                              foreground="white",
                              font=("Arial", 12))

        # Estilo para botones principales
        self.estilo.configure("botonCrear.TButton",
                              background="#28a745",
                              foreground="white",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonCrear.TButton",
                        background=[("pressed", "#1e7e34"), ("active", "#34ce57")])

        self.estilo.configure("botonEditar.TButton",
                              background="#ffc107",
                              foreground="black",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonEditar.TButton",
                        background=[("pressed", "#e0a800"), ("active", "#ffcd39")])

        self.estilo.configure("botonInformacion.TButton",
                              background="#17a2b8",
                              foreground="white",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonInformacion.TButton",
                        background=[("pressed", "#138496"), ("active", "#1fc8e3")])

        # Estilo para botón de regresar
        self.estilo.configure("botonRegresar.TButton",
                              background="#6c757d",
                              foreground="white",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonRegresar.TButton",
                        background=[("pressed", "#5a6268"), ("active", "#78848b")])

        # Estilo para indicadores de estado
        self.estilo.configure("disponible.TLabel",
                              background="#28a745",
                              foreground="white",
                              font=("Arial", 10, "bold"))

        self.estilo.configure("completo.TLabel",
                              background="#dc3545",
                              foreground="white",
                              font=("Arial", 10, "bold"))

        self.estilo.configure("ocupado.TLabel",
                              background="#ffc107",
                              foreground="black",
                              font=("Arial", 10, "bold"))

    def crear_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        self.frame_principal = ttk.Frame(self, style="framePrincipal.TFrame")
        self.frame_principal.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        # Configurar grid del frame principal
        self.frame_principal.rowconfigure(1, weight=1)
        self.frame_principal.columnconfigure(0, weight=1)

        # Crear header
        self.crear_header()

        # Crear área de grupos
        self.crear_area_grupos()

        # Crear botones de acción
        self.crear_botones_accion()

        # Crear botón de regresar
        self.crear_boton_regresar()

    def crear_header(self):
        """Crear el header con título y subtítulo"""
        header_frame = ttk.Frame(self.frame_principal, style="framePrincipal.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)

        # Título
        titulo_label = ttk.Label(header_frame,
                                 text="Grupos por Ciclo",
                                 style="tituloGrupos.TLabel")
        titulo_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Subtítulo con información del ciclo
        if self.ciclo_info:
            subtitulo_text = f"Ciclo: {self.ciclo_info[1]}"
            if len(self.ciclo_info) > 2:
                subtitulo_text += f" - {self.ciclo_info[2]}"

            subtitulo_label = ttk.Label(header_frame,
                                        text=subtitulo_text,
                                        style="subtituloGrupos.TLabel")
            subtitulo_label.grid(row=1, column=0, sticky="w", pady=(0, 10))

    def crear_area_grupos(self):
        """Crear el área scrollable para mostrar los grupos"""
        # Frame contenedor con scrollbar
        container_frame = ttk.Frame(self.frame_principal, style="framePrincipal.TFrame")
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

        # Frame interno del canvas
        self.frame_grupos = ttk.Frame(self.canvas, style="framePrincipal.TFrame")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame_grupos, anchor="nw")

        # Configurar el scroll
        self.frame_grupos.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Bind del mouse wheel
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def crear_botones_accion(self):
        """Crear los botones de acción"""
        botones_frame = ttk.Frame(self.frame_principal, style="framePrincipal.TFrame")
        botones_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        botones_frame.columnconfigure(0, weight=1)
        botones_frame.columnconfigure(1, weight=1)
        botones_frame.columnconfigure(2, weight=1)

        # Botón Crear Grupo
        self.boton_crear = ttk.Button(botones_frame,
                                      text="Crear Grupo",
                                      style="botonCrear.TButton",
                                      command=self.crear_grupo)
        self.boton_crear.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=5)

        # Botón Editar Grupo
        self.boton_editar = ttk.Button(botones_frame,
                                       text="Editar Grupo",
                                       style="botonEditar.TButton",
                                       command=self.editar_grupo)
        self.boton_editar.grid(row=0, column=1, sticky="ew", padx=(5, 5), pady=5)

        # Botón Ver Información
        self.boton_informacion = ttk.Button(botones_frame,
                                            text="Ver Información",
                                            style="botonInformacion.TButton",
                                            command=self.ver_informacion)
        self.boton_informacion.grid(row=0, column=2, sticky="ew", padx=(5, 0), pady=5)

    def crear_boton_regresar(self):
        """Crear el botón de regresar"""
        self.boton_regresar = ttk.Button(self.frame_principal,
                                         text="Regresar a Ciclos",
                                         style="botonRegresar.TButton",
                                         command=self.regresar_ciclos)
        self.boton_regresar.grid(row=3, column=0, sticky="w", pady=(10, 0))

    def on_frame_configure(self, event):
        """Callback para configurar el scroll cuando el frame cambia de tamaño"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        """Callback para configurar el canvas cuando cambia de tamaño"""
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)

    def on_mousewheel(self, event):
        """Callback para manejar el scroll con la rueda del mouse"""
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def mostrar_grupos(self, ciclo_info):
        """
        Mostrar grupos de un ciclo específico

        Args:
            ciclo_info (tuple): Información del ciclo seleccionado
        """
        self.ciclo_info = ciclo_info
        self.title(f"Grupos - {ciclo_info[1]}")
        self.cargar_grupos()

    def cargar_grupos(self):
        """Cargar los grupos desde la base de datos"""
        if not self.ciclo_info:
            messagebox.showerror("Error", "No se ha seleccionado un ciclo")
            return

        try:
            # Obtener el ID del ciclo (primer elemento de la tupla)
            id_ciclo = self.ciclo_info[0]
            self.grupos_data = obtener_grupos_por_ciclo(id_ciclo)
            self.mostrar_grupos_en_vista()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar grupos: {str(e)}")
            print(f"❌ Error al cargar grupos: {e}")

    def mostrar_grupos_en_vista(self):
        """Mostrar los grupos en el área de grupos"""
        # Limpiar frame actual
        for widget in self.frame_grupos.winfo_children():
            widget.destroy()

        if not self.grupos_data:
            # Mostrar mensaje si no hay grupos
            no_grupos_label = ttk.Label(self.frame_grupos,
                                        text="No hay grupos registrados en este ciclo",
                                        style="tituloGrupos.TLabel")
            no_grupos_label.grid(row=0, column=0, pady=50)
            return

        # Configurar grid para mostrar grupos en filas
        columnas_por_fila = 3
        for i, grupo in enumerate(self.grupos_data):
            fila = i // columnas_por_fila
            columna = i % columnas_por_fila

            # Configurar columnas del grid
            self.frame_grupos.columnconfigure(columna, weight=1)

            # Crear tarjeta de grupo
            self.crear_tarjeta_grupo(self.frame_grupos, grupo, fila, columna)

        # Actualizar scroll region
        self.frame_grupos.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def crear_tarjeta_grupo(self, parent, grupo, fila, columna):
        """Crear una tarjeta individual para un grupo"""
        # Extraer información del grupo
        # Estructura: (id_grupo, nombre_grupo, capacidad, id_colaborador, id_ciclo, nombre_colaborador, nombre_ciclo)
        id_grupo = grupo[0]
        nombre_grupo = grupo[1]
        capacidad = grupo[2]
        id_colaborador = grupo[3]
        nombre_colaborador = grupo[5] if len(grupo) > 5 else "No asignado"

        # Frame de la tarjeta
        card_frame = ttk.Frame(parent, style="grupoCard.TFrame")
        card_frame.grid(row=fila, column=columna, sticky="ew", padx=10, pady=10)
        card_frame.configure(padding=(15, 10))

        # Configurar grid de la tarjeta
        card_frame.columnconfigure(0, weight=1)

        # Nombre del grupo
        nombre_label = ttk.Label(card_frame,
                                 text=nombre_grupo,
                                 style="grupoNombre.TLabel")
        nombre_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Capacidad
        capacidad_label = ttk.Label(card_frame,
                                    text=f"Capacidad: {capacidad} estudiantes",
                                    style="grupoInfo.TLabel")
        capacidad_label.grid(row=1, column=0, sticky="w", pady=(0, 5))

        # Colaborador asignado
        colaborador_label = ttk.Label(card_frame,
                                      text=f"Docente: {nombre_colaborador}",
                                      style="grupoInfo.TLabel")
        colaborador_label.grid(row=2, column=0, sticky="w", pady=(0, 5))

        # ID del grupo (para referencia)
        id_label = ttk.Label(card_frame,
                             text=f"ID: {id_grupo}",
                             style="grupoInfo.TLabel")
        id_label.grid(row=3, column=0, sticky="w", pady=(0, 10))

        # Hacer la tarjeta clickeable para seleccionar
        def seleccionar_grupo(event):
            self.grupo_seleccionado = grupo
            self.resaltar_grupo_seleccionado()

        # Bind de eventos de click
        widgets_clickeables = [card_frame, nombre_label, capacidad_label, colaborador_label, id_label]
        for widget in widgets_clickeables:
            widget.bind("<Button-1>", seleccionar_grupo)

        # Guardar referencia para resaltar
        card_frame.id_grupo = id_grupo

    def resaltar_grupo_seleccionado(self):
        """Resaltar el grupo seleccionado"""
        if not self.grupo_seleccionado:
            return

        # Restaurar el estilo de todas las tarjetas
        for widget in self.frame_grupos.winfo_children():
            if hasattr(widget, 'id_grupo'):
                widget.configure(style="grupoCard.TFrame")
                # Actualizar estilo de los labels hijos
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label):
                        if "Nombre" in str(child.cget("style")):
                            child.configure(style="grupoNombre.TLabel")
                        else:
                            child.configure(style="grupoInfo.TLabel")

        # Resaltar la tarjeta seleccionada
        for widget in self.frame_grupos.winfo_children():
            if hasattr(widget, 'id_grupo') and widget.id_grupo == self.grupo_seleccionado[0]:
                widget.configure(style="grupoCardSeleccionada.TFrame")
                # Actualizar estilo de los labels hijos
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label):
                        if "Nombre" in str(child.cget("style")):
                            child.configure(style="grupoNombreSeleccionado.TLabel")
                        else:
                            child.configure(style="grupoInfoSeleccionado.TLabel")

    def crear_grupo(self):
        """Función para crear un nuevo grupo"""
        try:
            # Verificar que haya un ciclo seleccionado
            if not self.ciclo_info:
                messagebox.showerror("Error", "No se ha seleccionado un ciclo")
                return

            # Abrir la ventana modal para crear grupo
            vista_crear = VistaCrearGrupo(
                parent=self,
                ciclo_info=self.ciclo_info,
                callback_actualizar=self.actualizar_vista_grupos
            )

            # Esperar a que se cierre la ventana modal
            self.wait_window(vista_crear)

        except Exception as e:
            print(f"❌ Error al abrir ventana crear grupo: {e}")
            messagebox.showerror("Error", f"Error al abrir ventana: {str(e)}")

    def actualizar_vista_grupos(self):
        """Actualizar la vista de grupos después de crear/editar"""
        try:
            # Recargar los grupos
            self.cargar_grupos()

            # Limpiar selección
            self.grupo_seleccionado = None

            print("✅ Vista de grupos actualizada correctamente")

        except Exception as e:
            print(f"❌ Error al actualizar vista de grupos: {e}")
            messagebox.showerror("Error", f"Error al actualizar vista: {str(e)}")

    def editar_grupo(self):
        """Función para editar un grupo existente"""
        if not self.grupo_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor selecciona un grupo para editar")
            return

        try:
            # Mostrar ventana de edición
            ventana_editar = mostrar_ventana_editar_grupo(self, self.grupo_seleccionado)

            if ventana_editar:
                # Esperar a que se cierre la ventana de edición
                self.wait_window(ventana_editar)

                # Actualizar la lista de grupos después de la edición
                self.cargar_grupos()

                # Limpiar selección
                self.grupo_seleccionado = None

                print(f"✅ Grupo editado exitosamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir ventana de edición: {str(e)}")
            print(f"❌ Error al editar grupo: {e}")

    def ver_informacion(self):
        """Función para ver información detallada de un grupo"""
        if not self.grupo_seleccionado:
            messagebox.showwarning("Advertencia", "Por favor selecciona un grupo para ver su información")
            return

        try:
            # Mostrar la ventana de información del grupo
            ventana_info = mostrar_informacion_grupo(self, self.grupo_seleccionado)

            if ventana_info:
                # Esperar a que se cierre la ventana
                self.wait_window(ventana_info)

                print(f"✅ Información del grupo mostrada correctamente")

        except Exception as e:
            messagebox.showerror("Error", f"Error al mostrar información del grupo: {str(e)}")
            print(f"❌ Error al mostrar información: {e}")

    def regresar_ciclos(self):
        """Regresar a la vista de ciclos"""
        self.destroy()

    def on_closing(self):
        """Manejar el cierre de la ventana"""
        self.destroy()