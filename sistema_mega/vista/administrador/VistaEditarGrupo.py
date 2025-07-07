import tkinter as tk
from tkinter import ttk, messagebox
from sistema_mega.modelo.modelo_grupos import *


class VistaEditarGrupo(tk.Toplevel):
    def __init__(self, parent, grupo_info=None):
        super().__init__(parent)
        self.parent = parent
        self.grupo_info = grupo_info
        self.title("Editar Grupo")
        self.geometry("500x400")
        self.configure(bg="#f0f0f0")

        # Configurar el protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Hacer que la ventana sea modal
        self.transient(parent)
        self.grab_set()

        # Centrar la ventana
        self.center_window()

        # Variables
        self.colaboradores_data = []
        self.var_nombre_grupo = tk.StringVar()
        self.var_capacidad = tk.StringVar()
        self.var_colaborador_seleccionado = tk.StringVar()

        # Configurar estilos
        self.configurar_estilos()

        # Crear widgets
        self.crear_widgets()

        # Cargar datos
        self.cargar_datos_iniciales()

    def center_window(self):
        """Centrar la ventana en la pantalla"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def configurar_estilos(self):
        """Configurar los estilos de la interfaz"""
        self.estilo = ttk.Style()
        self.estilo.theme_use("clam")

        # Estilo para el frame principal
        self.estilo.configure("frameEditarGrupo.TFrame",
                              background="#f0f0f0")

        # Estilo para el título
        self.estilo.configure("tituloEditarGrupo.TLabel",
                              background="#f0f0f0",
                              foreground="#333333",
                              font=("Arial", 18, "bold"))

        # Estilo para labels
        self.estilo.configure("labelEditarGrupo.TLabel",
                              background="#f0f0f0",
                              foreground="#333333",
                              font=("Arial", 12))

        # Estilo para campos de entrada
        self.estilo.configure("entryEditarGrupo.TEntry",
                              fieldbackground="white",
                              font=("Arial", 12))

        # Estilo para combobox
        self.estilo.configure("comboEditarGrupo.TCombobox",
                              fieldbackground="white",
                              font=("Arial", 12))

        # Estilo para botón guardar
        self.estilo.configure("botonGuardarEditar.TButton",
                              background="#28a745",
                              foreground="white",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonGuardarEditar.TButton",
                        background=[("pressed", "#1e7e34"), ("active", "#34ce57")])

        # Estilo para botón cancelar
        self.estilo.configure("botonCancelarEditar.TButton",
                              background="#6c757d",
                              foreground="white",
                              font=("Arial", 12, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonCancelarEditar.TButton",
                        background=[("pressed", "#5a6268"), ("active", "#78848b")])

    def crear_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        self.frame_principal = ttk.Frame(self, style="frameEditarGrupo.TFrame")
        self.frame_principal.pack(fill="both", expand=True, padx=30, pady=30)

        # Título
        titulo_label = ttk.Label(self.frame_principal,
                                 text="Editar Grupo",
                                 style="tituloEditarGrupo.TLabel")
        titulo_label.pack(pady=(0, 30))

        # Frame para los campos
        campos_frame = ttk.Frame(self.frame_principal, style="frameEditarGrupo.TFrame")
        campos_frame.pack(fill="x", pady=(0, 30))

        # Campo: Nombre del grupo
        ttk.Label(campos_frame,
                  text="Nombre del grupo:",
                  style="labelEditarGrupo.TLabel").pack(anchor="w", pady=(0, 5))

        self.entry_nombre = ttk.Entry(campos_frame,
                                      textvariable=self.var_nombre_grupo,
                                      style="entryEditarGrupo.TEntry",
                                      width=40)
        self.entry_nombre.pack(fill="x", pady=(0, 20))

        # Campo: Capacidad
        ttk.Label(campos_frame,
                  text="Capacidad:",
                  style="labelEditarGrupo.TLabel").pack(anchor="w", pady=(0, 5))

        self.entry_capacidad = ttk.Entry(campos_frame,
                                         textvariable=self.var_capacidad,
                                         style="entryEditarGrupo.TEntry",
                                         width=40)
        self.entry_capacidad.pack(fill="x", pady=(0, 20))

        # Campo: Colaborador (Tutor)
        ttk.Label(campos_frame,
                  text="Colaborador (Tutor):",
                  style="labelEditarGrupo.TLabel").pack(anchor="w", pady=(0, 5))

        self.combo_colaborador = ttk.Combobox(campos_frame,
                                              textvariable=self.var_colaborador_seleccionado,
                                              style="comboEditarGrupo.TCombobox",
                                              state="readonly",
                                              width=37)
        self.combo_colaborador.pack(fill="x", pady=(0, 20))

        # Frame para botones
        botones_frame = ttk.Frame(self.frame_principal, style="frameEditarGrupo.TFrame")
        botones_frame.pack(fill="x")

        # Configurar grid para botones
        botones_frame.columnconfigure(0, weight=1)
        botones_frame.columnconfigure(1, weight=1)

        # Botón Guardar
        self.boton_guardar = ttk.Button(botones_frame,
                                        text="Guardar",
                                        style="botonGuardarEditar.TButton",
                                        command=self.guardar_cambios)
        self.boton_guardar.grid(row=0, column=0, sticky="ew", padx=(0, 10), pady=10)

        # Botón Cancelar
        self.boton_cancelar = ttk.Button(botones_frame,
                                         text="Cancelar",
                                         style="botonCancelarEditar.TButton",
                                         command=self.cancelar)
        self.boton_cancelar.grid(row=0, column=1, sticky="ew", padx=(10, 0), pady=10)

    def cargar_datos_iniciales(self):
        """Cargar los datos iniciales del grupo y colaboradores"""
        if not self.grupo_info:
            messagebox.showerror("Error", "No se ha proporcionado información del grupo")
            self.destroy()
            return

        try:
            # Cargar colaboradores
            self.colaboradores_data = obtener_colaboradores_activos()

            # Configurar combobox de colaboradores
            colaboradores_nombres = [f"{col[1]}" for col in self.colaboradores_data]
            self.combo_colaborador['values'] = colaboradores_nombres

            # Cargar datos del grupo
            # Estructura del grupo: (id_grupo, nombre_grupo, capacidad, id_colaborador, id_ciclo, nombre_colaborador, nombre_ciclo)
            self.var_nombre_grupo.set(self.grupo_info[1])  # nombre_grupo
            self.var_capacidad.set(str(self.grupo_info[2]))  # capacidad

            # Buscar y seleccionar el colaborador actual
            id_colaborador_actual = self.grupo_info[3]
            for i, colaborador in enumerate(self.colaboradores_data):
                if colaborador[0] == id_colaborador_actual:
                    self.combo_colaborador.current(i)
                    break

            print(f"✅ Datos cargados para grupo: {self.grupo_info[1]}")

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
            print(f"❌ Error al cargar datos iniciales: {e}")

    def validar_datos(self):
        """Validar los datos ingresados"""
        errores = []

        # Validar nombre del grupo
        nombre = self.var_nombre_grupo.get().strip()
        if not nombre:
            errores.append("El nombre del grupo es obligatorio")
        elif len(nombre) < 2:
            errores.append("El nombre del grupo debe tener al menos 2 caracteres")
        elif len(nombre) > 45:
            errores.append("El nombre del grupo no puede exceder 45 caracteres")

        # Validar capacidad
        capacidad_str = self.var_capacidad.get().strip()
        if not capacidad_str:
            errores.append("La capacidad es obligatoria")
        else:
            try:
                capacidad = int(capacidad_str)
                if capacidad <= 0:
                    errores.append("La capacidad debe ser mayor a 0")
                elif capacidad > 999:
                    errores.append("La capacidad no puede exceder 999 estudiantes")
            except ValueError:
                errores.append("La capacidad debe ser un número entero válido")

        # Validar colaborador seleccionado
        if not self.var_colaborador_seleccionado.get():
            errores.append("Debe seleccionar un colaborador")

        return errores

    def obtener_id_colaborador_seleccionado(self):
        """Obtener el ID del colaborador seleccionado"""
        colaborador_nombre = self.var_colaborador_seleccionado.get()

        for colaborador in self.colaboradores_data:
            if colaborador[1] == colaborador_nombre:
                return colaborador[0]

        return None

    def guardar_cambios(self):
        """Guardar los cambios realizados en el grupo"""
        try:
            # Validar datos
            errores = self.validar_datos()
            if errores:
                mensaje_error = "Se encontraron los siguientes errores:\n\n" + "\n".join(
                    f"• {error}" for error in errores)
                messagebox.showerror("Errores de validación", mensaje_error)
                return

            # Obtener valores
            id_grupo = self.grupo_info[0]
            nombre_grupo = self.var_nombre_grupo.get().strip()
            capacidad = int(self.var_capacidad.get().strip())
            id_colaborador = self.obtener_id_colaborador_seleccionado()
            id_ciclo = self.grupo_info[4]  # El ciclo no cambia

            # Confirmar cambios
            respuesta = messagebox.askyesno(
                "Confirmar cambios",
                f"¿Está seguro de que desea guardar los cambios en el grupo '{nombre_grupo}'?",
                icon='question'
            )

            if not respuesta:
                return

            # Ejecutar la edición
            if editar_grupo(id_grupo, nombre_grupo, capacidad, id_colaborador, id_ciclo):
                messagebox.showinfo("Éxito", "Grupo editado exitosamente")

                # Notificar a la ventana padre para que actualice la lista
                if hasattr(self.parent, 'cargar_grupos'):
                    self.parent.cargar_grupos()

                self.destroy()
            else:
                messagebox.showerror("Error", "No se pudo editar el grupo")

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cambios: {str(e)}")
            print(f"❌ Error al guardar cambios: {e}")

    def cancelar(self):
        """Cancelar la edición"""
        self.destroy()

    def on_closing(self):
        """Manejar el cierre de la ventana"""
        self.destroy()


# Función para mostrar la ventana de editar grupo
def mostrar_ventana_editar_grupo(parent, grupo_info):
    """
    Función para mostrar la ventana de editar grupo

    Args:
        parent: Ventana padre
        grupo_info: Información del grupo a editar
    """
    try:
        ventana = VistaEditarGrupo(parent, grupo_info)
        return ventana
    except Exception as e:
        messagebox.showerror("Error", f"Error al abrir ventana de edición: {str(e)}")
        print(f"❌ Error al mostrar ventana editar grupo: {e}")
        return None