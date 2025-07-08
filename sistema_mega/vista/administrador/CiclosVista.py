import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime
from sistema_mega.modelo.ModeloCiclos import *
from sistema_mega.vista.administrador.vista_gestionar_grupos import VistaGestionarGrupos

class VentanaEditarCiclo(tk.Toplevel):
    """Ventana para editar un ciclo existente"""

    def __init__(self, parent, ciclo_data, callback_actualizar=None):
        super().__init__(parent)
        self.parent = parent
        self.ciclo_data = ciclo_data  # Datos del ciclo a editar
        self.callback_actualizar = callback_actualizar

        self.title("Editar Ciclo Programado")
        self.geometry("500x650")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        # Hacer la ventana modal
        self.transient(parent)
        self.grab_set()

        # Centrar la ventana
        self.center_window()

        # Configurar el protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.cancelar)

        self.crear_widgets()
        self.cargar_datos_ciclo()

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def crear_widgets(self):
        """Crear los widgets de la ventana"""
        # Frame principal
        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame, text="Editar Ciclo Programado",
                                font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 30))

        # Frame para los campos
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.X, pady=(0, 20))

        # Información del ciclo (solo lectura)
        info_frame = ttk.LabelFrame(fields_frame, text="Información del Ciclo", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 15))

        # ID del ciclo (solo lectura)
        ttk.Label(info_frame, text="ID del ciclo:",
                  font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.label_id = ttk.Label(info_frame, text="", font=("Arial", 10))
        self.label_id.pack(anchor=tk.W, pady=(0, 10))

        # Nombre del ciclo
        ttk.Label(fields_frame, text="Nombre del ciclo:",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.entry_nombre = ttk.Entry(fields_frame, font=("Arial", 12))
        self.entry_nombre.pack(fill=tk.X, pady=(0, 15))

        # Modalidad
        ttk.Label(fields_frame, text="Modalidad:",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.combo_modalidad = ttk.Combobox(fields_frame,
                                            values=["Presencial", "Virtual", "Híbrida"],
                                            state="readonly",
                                            font=("Arial", 12))
        self.combo_modalidad.pack(fill=tk.X, pady=(0, 15))

        # Costo
        ttk.Label(fields_frame, text="Costo (S/.):",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.entry_costo = ttk.Entry(fields_frame, font=("Arial", 12))
        self.entry_costo.pack(fill=tk.X, pady=(0, 15))

        # Fecha de inicio
        ttk.Label(fields_frame, text="Fecha de inicio:",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.date_inicio = DateEntry(fields_frame,
                                     width=12,
                                     background='darkblue',
                                     foreground='white',
                                     borderwidth=2,
                                     font=("Arial", 12),
                                     date_pattern='yyyy-mm-dd')
        self.date_inicio.pack(fill=tk.X, pady=(0, 15))

        # Fecha de fin
        ttk.Label(fields_frame, text="Fecha de fin:",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.date_fin = DateEntry(fields_frame,
                                  width=12,
                                  background='darkblue',
                                  foreground='white',
                                  borderwidth=2,
                                  font=("Arial", 12),
                                  date_pattern='yyyy-mm-dd')
        self.date_fin.pack(fill=tk.X, pady=(0, 15))

        # Frame para botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))

        # Botón Guardar
        self.btn_guardar = ttk.Button(buttons_frame,
                                      text="Guardar Cambios",
                                      command=self.guardar_cambios,
                                      style="Accent.TButton")
        self.btn_guardar.pack(side=tk.LEFT, padx=(0, 10))

        # Botón Cancelar
        self.btn_cancelar = ttk.Button(buttons_frame,
                                       text="Cancelar",
                                       command=self.cancelar)
        self.btn_cancelar.pack(side=tk.LEFT)

        # Configurar estilos
        self.configurar_estilos()

    def configurar_estilos(self):
        """Configurar estilos para la ventana"""
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))

    def cargar_datos_ciclo(self):
        """Cargar los datos del ciclo en los campos"""
        if not self.ciclo_data:
            return

        try:
            # Extraer datos del ciclo
            id_ciclo = self.ciclo_data[0]
            nombre = self.ciclo_data[1]
            modalidad = self.ciclo_data[2]
            costo = self.ciclo_data[3]
            fecha_inicio = self.ciclo_data[4]
            fecha_fin = self.ciclo_data[5]

            # Llenar los campos
            self.label_id.config(text=f"#{id_ciclo}")
            self.entry_nombre.insert(0, nombre)
            self.combo_modalidad.set(modalidad)
            self.entry_costo.insert(0, str(costo))

            # Configurar fechas
            if isinstance(fecha_inicio, str):
                fecha_inicio_obj = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            else:
                fecha_inicio_obj = fecha_inicio

            if isinstance(fecha_fin, str):
                fecha_fin_obj = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            else:
                fecha_fin_obj = fecha_fin

            self.date_inicio.set_date(fecha_inicio_obj)
            self.date_fin.set_date(fecha_fin_obj)

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos del ciclo: {str(e)}")
            print(f"❌ Error al cargar datos: {e}")

    def validar_campos(self):
        """Validar que todos los campos estén completos"""
        errores = []

        # Validar nombre
        if not self.entry_nombre.get().strip():
            errores.append("El nombre del ciclo es obligatorio")

        # Validar modalidad
        if not self.combo_modalidad.get():
            errores.append("Debe seleccionar una modalidad")

        # Validar costo
        try:
            costo = float(self.entry_costo.get())
            if costo <= 0:
                errores.append("El costo debe ser mayor a 0")
        except ValueError:
            errores.append("El costo debe ser un número válido")

        # Validar fechas
        if self.date_fin.get_date() <= self.date_inicio.get_date():
            errores.append("La fecha de fin debe ser posterior a la fecha de inicio")

        return errores

    def guardar_cambios(self):
        """Guardar los cambios del ciclo en la base de datos"""
        try:
            # Validar campos
            errores = self.validar_campos()
            if errores:
                mensaje_error = "Por favor corrija los siguientes errores:\n\n"
                mensaje_error += "\n".join(f"• {error}" for error in errores)
                messagebox.showerror("Errores de validación", mensaje_error)
                return

            # Obtener datos del formulario
            id_ciclo = self.ciclo_data[0]
            nombre = self.entry_nombre.get().strip()
            modalidad = self.combo_modalidad.get()
            costo = float(self.entry_costo.get())
            fecha_inicio = self.date_inicio.get_date().strftime('%Y-%m-%d')
            fecha_fin = self.date_fin.get_date().strftime('%Y-%m-%d')

            # Confirmar los cambios
            resultado = messagebox.askyesno("Confirmar cambios",
                                            f"¿Está seguro que desea guardar los cambios del ciclo '{nombre}'?")
            if not resultado:
                return

            # Editar el ciclo
            exito = editar_ciclo(
                id_ciclo,
                nombre,
                modalidad,
                costo,
                fecha_inicio,
                fecha_fin
            )

            if exito:
                messagebox.showinfo("Éxito", "Ciclo editado exitosamente")

                # Llamar callback para actualizar la vista principal
                if self.callback_actualizar:
                    self.callback_actualizar()

                self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo editar el ciclo")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")
            print(f"❌ Error al guardar cambios: {e}")

    def cancelar(self):
        """Cancelar la edición del ciclo"""
        resultado = messagebox.askyesno("Confirmar",
                                        "¿Está seguro que desea cancelar?\n"
                                        "Se perderán los cambios realizados.")
        if resultado:
            self.destroy()


class VentanaCrearCiclo(tk.Toplevel):
    """Ventana para crear un nuevo ciclo"""

    def __init__(self, parent, id_sede, callback_actualizar=None):
        super().__init__(parent)
        self.parent = parent
        self.id_sede = id_sede
        self.callback_actualizar = callback_actualizar

        self.title("Crear Ciclo Programado")
        self.geometry("500x600")
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        # Hacer la ventana modal
        self.transient(parent)
        self.grab_set()

        # Centrar la ventana
        self.center_window()

        # Configurar el protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.cancelar)

        self.crear_widgets()

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def crear_widgets(self):
        """Crear los widgets de la ventana"""
        # Frame principal
        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame, text="Crear Ciclo Programado",
                                font=("Arial", 18, "bold"))
        title_label.pack(pady=(0, 30))

        # Frame para los campos
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill=tk.X, pady=(0, 20))

        # Nombre del ciclo
        ttk.Label(fields_frame, text="Nombre del ciclo:",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.entry_nombre = ttk.Entry(fields_frame, font=("Arial", 12))
        self.entry_nombre.pack(fill=tk.X, pady=(0, 15))

        # Modalidad
        ttk.Label(fields_frame, text="Modalidad:",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.combo_modalidad = ttk.Combobox(fields_frame,
                                            values=["Presencial", "Virtual", "Híbrida"],
                                            state="readonly",
                                            font=("Arial", 12))
        self.combo_modalidad.pack(fill=tk.X, pady=(0, 15))
        self.combo_modalidad.set("Presencial")  # Valor por defecto

        # Costo
        ttk.Label(fields_frame, text="Costo (S/.):",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.entry_costo = ttk.Entry(fields_frame, font=("Arial", 12))
        self.entry_costo.pack(fill=tk.X, pady=(0, 15))

        # Fecha de inicio
        ttk.Label(fields_frame, text="Fecha de inicio:",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.date_inicio = DateEntry(fields_frame,
                                     width=12,
                                     background='darkblue',
                                     foreground='white',
                                     borderwidth=2,
                                     font=("Arial", 12),
                                     date_pattern='yyyy-mm-dd',
                                     mindate=datetime.now().date())
        self.date_inicio.pack(fill=tk.X, pady=(0, 15))

        # Fecha de fin
        ttk.Label(fields_frame, text="Fecha de fin:",
                  font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.date_fin = DateEntry(fields_frame,
                                  width=12,
                                  background='darkblue',
                                  foreground='white',
                                  borderwidth=2,
                                  font=("Arial", 12),
                                  date_pattern='yyyy-mm-dd',
                                  mindate=datetime.now().date())
        self.date_fin.pack(fill=tk.X, pady=(0, 15))

        # Frame para botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))

        # Botón Guardar
        self.btn_guardar = ttk.Button(buttons_frame,
                                      text="Guardar",
                                      command=self.guardar_ciclo,
                                      style="Accent.TButton")
        self.btn_guardar.pack(side=tk.LEFT, padx=(0, 10))

        # Botón Cancelar
        self.btn_cancelar = ttk.Button(buttons_frame,
                                       text="Cancelar",
                                       command=self.cancelar)
        self.btn_cancelar.pack(side=tk.LEFT)

        # Configurar estilos
        self.configurar_estilos()

    def configurar_estilos(self):
        """Configurar estilos para la ventana"""
        style = ttk.Style()
        style.configure("Accent.TButton", font=("Arial", 12, "bold"))

    def validar_campos(self):
        """Validar que todos los campos estén completos"""
        errores = []

        # Validar nombre
        if not self.entry_nombre.get().strip():
            errores.append("El nombre del ciclo es obligatorio")

        # Validar modalidad
        if not self.combo_modalidad.get():
            errores.append("Debe seleccionar una modalidad")

        # Validar costo
        try:
            costo = float(self.entry_costo.get())
            if costo <= 0:
                errores.append("El costo debe ser mayor a 0")
        except ValueError:
            errores.append("El costo debe ser un número válido")

        # Validar fechas
        if self.date_fin.get_date() <= self.date_inicio.get_date():
            errores.append("La fecha de fin debe ser posterior a la fecha de inicio")

        return errores

    def guardar_ciclo(self):
        """Guardar el ciclo en la base de datos"""
        try:
            # Validar campos
            errores = self.validar_campos()
            if errores:
                mensaje_error = "Por favor corrija los siguientes errores:\n\n"
                mensaje_error += "\n".join(f"• {error}" for error in errores)
                messagebox.showerror("Errores de validación", mensaje_error)
                return

            # Obtener datos del formulario
            nombre = self.entry_nombre.get().strip()
            modalidad = self.combo_modalidad.get()
            costo = float(self.entry_costo.get())
            fecha_inicio = self.date_inicio.get_date().strftime('%Y-%m-%d')
            fecha_fin = self.date_fin.get_date().strftime('%Y-%m-%d')

            # Crear el ciclo
            exito = agregar_ciclo(
                self.id_sede,
                nombre,
                modalidad,
                costo,
                fecha_inicio,
                fecha_fin
            )

            if exito:
                messagebox.showinfo("Éxito", "Ciclo creado exitosamente")

                # Llamar callback para actualizar la vista principal
                if self.callback_actualizar:
                    self.callback_actualizar()

                self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo crear el ciclo")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar el ciclo: {str(e)}")
            print(f"❌ Error al guardar ciclo: {e}")

    def cancelar(self):
        """Cancelar la creación del ciclo"""
        resultado = messagebox.askyesno("Confirmar",
                                        "¿Está seguro que desea cancelar?\n"
                                        "Se perderán los datos ingresados.")
        if resultado:
            self.destroy()


class CiclosVista(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Gestionar Ciclos")
        self.geometry("1200x800")
        self.configure(bg="#f0f0f0")

        # Configurar el protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Hacer que la ventana sea modal
        self.transient(parent)
        self.grab_set()

        # Variables
        self.ciclos_data = []
        self.ciclo_seleccionado = None
        self.sede_info = None

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
        self.estilo.configure("tituloCiclos.TLabel",
                              background="#f0f0f0",
                              foreground="#333333",
                              font=("Arial", 24, "bold"))

        # Estilo para las tarjetas de ciclos
        self.estilo.configure("cicloCard.TFrame",
                              background="#4a90e2",
                              relief="raised",
                              borderwidth=2)

        # Estilo para tarjeta seleccionada
        self.estilo.configure("cicloCardSeleccionada.TFrame",
                              background="#2c5282",
                              relief="raised",
                              borderwidth=3)

        # Estilo para el texto de los ciclos
        self.estilo.configure("cicloNombre.TLabel",
                              background="#4a90e2",
                              foreground="white",
                              font=("Arial", 14, "bold"))

        self.estilo.configure("cicloInfo.TLabel",
                              background="#4a90e2",
                              foreground="white",
                              font=("Arial", 12))

        # Estilo para el texto de ciclo seleccionado
        self.estilo.configure("cicloNombreSeleccionado.TLabel",
                              background="#2c5282",
                              foreground="white",
                              font=("Arial", 14, "bold"))

        self.estilo.configure("cicloInfoSeleccionado.TLabel",
                              background="#2c5282",
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
                        background=[("pressed", "#218838"), ("active", "#34ce57")])

        self.estilo.configure("botonEditar.TButton",
                              background="#ffc107",
                              foreground="black",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonEditar.TButton",
                        background=[("pressed", "#e0a800"), ("active", "#ffcd39")])

        # Estilo para botón Ver Grupos
        self.estilo.configure("botonVerGrupos.TButton",
                              background="#17a2b8",
                              foreground="white",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonVerGrupos.TButton",
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

        # Crear área de ciclos
        self.crear_area_ciclos()

        # Crear botones de acción
        self.crear_botones_accion()

        # Crear botón de regresar
        self.crear_boton_regresar()

    def crear_header(self):
        """Crear el header con título"""
        header_frame = ttk.Frame(self.frame_principal, style="framePrincipal.TFrame")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(0, weight=1)

        # Título
        titulo_label = ttk.Label(header_frame,
                                 text="Ciclos Programados",
                                 style="tituloCiclos.TLabel")
        titulo_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

    def crear_area_ciclos(self):
        """Crear el área scrollable para mostrar los ciclos"""
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
        self.frame_ciclos = ttk.Frame(self.canvas, style="framePrincipal.TFrame")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.frame_ciclos, anchor="nw")

        # Configurar el scroll
        self.frame_ciclos.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        # Bind del mouse wheel
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)

    def crear_botones_accion(self):
        """Crear los botones de acción (Crear, Editar y Ver Grupos)"""
        botones_frame = ttk.Frame(self.frame_principal, style="framePrincipal.TFrame")
        botones_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        botones_frame.columnconfigure(0, weight=1)
        botones_frame.columnconfigure(1, weight=1)
        botones_frame.columnconfigure(2, weight=1)

        # Botón Crear ciclo
        self.boton_crear = ttk.Button(botones_frame,
                                      text="Crear ciclo",
                                      style="botonCrear.TButton",
                                      command=self.crear_ciclo)
        self.boton_crear.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=5)

        # Botón Editar ciclo
        self.boton_editar = ttk.Button(botones_frame,
                                       text="Editar ciclo",
                                       style="botonEditar.TButton",
                                       command=self.editar_ciclo)
        self.boton_editar.grid(row=0, column=1, sticky="ew", padx=(5, 5), pady=5)

        # Botón Ver Grupos
        self.boton_ver_grupos = ttk.Button(botones_frame,
                                           text="Ver grupos",
                                           style="botonVerGrupos.TButton",
                                           command=self.ver_grupos)
        self.boton_ver_grupos.grid(row=0, column=2, sticky="ew", padx=(5, 0), pady=5)

    def crear_boton_regresar(self):
        """Crear el botón de regresar"""
        self.boton_regresar = ttk.Button(self.frame_principal,
                                         text="Regresar a Sedes Disponibles",
                                         style="botonRegresar.TButton",
                                         command=self.regresar_sedes)
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

    def mostrar_ciclos_sede(self, sede_info):
        """
        Mostrar ciclos de una sede específica

        Args:
            sede_info (tuple): Información de la sede (id, nombre, distrito)
        """
        self.sede_info = sede_info
        self.title(f"Ciclos Programados - {sede_info[1]}")
        self.cargar_ciclos()

    def cargar_ciclos(self):
        """Cargar los ciclos desde la base de datos"""
        if not self.sede_info:
            messagebox.showerror("Error", "No se ha seleccionado una sede")
            return

        try:
            self.ciclos_data = obtener_ciclos_por_sede(self.sede_info[0])
            self.mostrar_ciclos()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar ciclos: {str(e)}")
            print(f"❌ Error al cargar ciclos: {e}")

    def mostrar_ciclos(self):
        """Mostrar los ciclos en el área de ciclos"""
        # Limpiar frame actual
        for widget in self.frame_ciclos.winfo_children():
            widget.destroy()

        if not self.ciclos_data:
            # Mostrar mensaje si no hay ciclos
            no_ciclos_label = ttk.Label(self.frame_ciclos,
                                        text="No hay ciclos programados",
                                        style="tituloCiclos.TLabel")
            no_ciclos_label.grid(row=0, column=0, pady=50)
            return

        # Configurar grid para mostrar ciclos en filas
        columnas_por_fila = 4
        for i, ciclo in enumerate(self.ciclos_data):
            fila = i // columnas_por_fila
            columna = i % columnas_por_fila

            # Configurar columnas del grid
            self.frame_ciclos.columnconfigure(columna, weight=1)

            # Crear tarjeta de ciclo
            self.crear_tarjeta_ciclo(self.frame_ciclos, ciclo, fila, columna)

        # Actualizar scroll region
        self.frame_ciclos.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def crear_tarjeta_ciclo(self, parent, ciclo, fila, columna):
        """Crear una tarjeta individual para un ciclo"""
        # Extraer información del ciclo
        id_ciclo = ciclo[0]
        nombre_ciclo = ciclo[1]
        modalidad = ciclo[2] if len(ciclo) > 2 else "N/A"
        costo = ciclo[3] if len(ciclo) > 3 else 0.0
        fecha_inicio = ciclo[4] if len(ciclo) > 4 else "N/A"
        fecha_fin = ciclo[5] if len(ciclo) > 5 else "N/A"

        # Frame de la tarjeta
        card_frame = ttk.Frame(parent, style="cicloCard.TFrame")
        card_frame.grid(row=fila, column=columna, sticky="ew", padx=10, pady=10)
        card_frame.configure(padding=(15, 10))

        # Configurar grid de la tarjeta
        card_frame.columnconfigure(0, weight=1)

        # Nombre del ciclo
        nombre_label = ttk.Label(card_frame,
                                 text=nombre_ciclo,
                                 style="cicloNombre.TLabel")
        nombre_label.grid(row=0, column=0, sticky="w", pady=(0, 5))

        # Modalidad
        modalidad_label = ttk.Label(card_frame,
                                    text=f"Modalidad: {modalidad}",
                                    style="cicloInfo.TLabel")
        modalidad_label.grid(row=1, column=0, sticky="w", pady=(0, 5))

        # Costo
        costo_label = ttk.Label(card_frame,
                                text=f"Costo: S/. {costo:.2f}",
                                style="cicloInfo.TLabel")
        costo_label.grid(row=2, column=0, sticky="w", pady=(0, 5))

        # Fechas
        fechas_label = ttk.Label(card_frame,
                                 text=f"Inicio: {fecha_inicio}",
                                 style="cicloInfo.TLabel")
        fechas_label.grid(row=3, column=0, sticky="w", pady=(0, 10))

        # Hacer la tarjeta clickeable para seleccionar
        def seleccionar_ciclo(event):
            self.ciclo_seleccionado = ciclo
            self.resaltar_ciclo_seleccionado()

        card_frame.bind("<Button-1>", seleccionar_ciclo)
        nombre_label.bind("<Button-1>", seleccionar_ciclo)
        modalidad_label.bind("<Button-1>", seleccionar_ciclo)
        costo_label.bind("<Button-1>", seleccionar_ciclo)
        fechas_label.bind("<Button-1>", seleccionar_ciclo)

        # Guardar referencia para resaltar
        card_frame.id_ciclo = id_ciclo

    def resaltar_ciclo_seleccionado(self):
        """Resaltar el ciclo seleccionado"""
        if not self.ciclo_seleccionado:
            return

        # Restaurar el estilo de todas las tarjetas
        for widget in self.frame_ciclos.winfo_children():
            if hasattr(widget, 'id_ciclo'):
                widget.configure(style="cicloCard.TFrame")
                # Actualizar estilo de los labels hijos
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label):
                        if "Nombre" in str(child.cget("style")):
                            child.configure(style="cicloNombre.TLabel")
                        else:
                            child.configure(style="cicloInfo.TLabel")

        # Resaltar la tarjeta seleccionada
        for widget in self.frame_ciclos.winfo_children():
            if hasattr(widget, 'id_ciclo') and widget.id_ciclo == self.ciclo_seleccionado[0]:
                widget.configure(style="cicloCardSeleccionada.TFrame")
                # Actualizar estilo de los labels hijos
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label):
                        if "Nombre" in str(child.cget("style")):
                            child.configure(style="cicloNombreSeleccionado.TLabel")
                        else:
                            child.configure(style="cicloInfoSeleccionado.TLabel")

    def crear_ciclo(self):
        """Abrir ventana para crear un nuevo ciclo"""
        if not self.sede_info:
            messagebox.showerror("Error", "No se ha seleccionado una sede")
            return

        # Crear ventana de creación de ciclo
        ventana_crear = VentanaCrearCiclo(self, self.sede_info[0], self.cargar_ciclos)

    def editar_ciclo(self):
        """Editar el ciclo seleccionado"""
        if not self.ciclo_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un ciclo para editar")
            return

        # Crear ventana de edición de ciclo
        ventana_editar = VentanaEditarCiclo(self, self.ciclo_seleccionado, self.cargar_ciclos)

    def ver_grupos(self):
        """Ver los grupos del ciclo seleccionado"""
        if not self.ciclo_seleccionado:
            messagebox.showwarning("Advertencia", "Debe seleccionar un ciclo para ver sus grupos")
            return

        try:
            ventana_grupos = VistaGestionarGrupos(self, self.ciclo_seleccionado)
            ventana_grupos.mostrar_grupos(self.ciclo_seleccionado)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir la gestión de grupos: {str(e)}")

    def regresar_sedes(self):
        """Regresar a la vista de sedes"""
        self.destroy()

    def on_closing(self):
        """Manejar el cierre de la ventana"""
        self.destroy()