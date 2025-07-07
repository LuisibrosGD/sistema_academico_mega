import tkinter as tk
from tkinter import ttk, messagebox
from sistema_mega.modelo.modelo_grupos import *


class VistaCrearGrupo(tk.Toplevel):
    def __init__(self, parent, ciclo_info, callback_actualizar=None):
        super().__init__(parent)
        self.parent = parent
        self.ciclo_info = ciclo_info
        self.callback_actualizar = callback_actualizar

        self.title("Crear Grupo")
        self.geometry("450x400") 
        self.configure(bg="#f0f0f0")
        self.resizable(False, False)

        # Configurar el protocolo de cierre
        self.protocol("WM_DELETE_WINDOW", self.cancelar)

        # Hacer que la ventana sea modal
        self.transient(parent)
        self.grab_set()

        # Centrar la ventana
        self.center_window()

        # Variables
        self.nombre_grupo_var = tk.StringVar()
        self.capacidad_var = tk.StringVar()
        self.colaborador_var = tk.StringVar()
        self.colaboradores_data = []

        self.configurar_estilos()
        self.crear_widgets()
        self.cargar_colaboradores()

        # Focus en el primer campo
        self.entry_nombre.focus()

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
        self.estilo.configure("frameCrearGrupo.TFrame",
                              background="#f0f0f0")

        # Estilo para el título
        self.estilo.configure("tituloCrearGrupo.TLabel",
                              background="#f0f0f0",
                              foreground="#333333",
                              font=("Arial", 18, "bold"))

        # Estilo para labels
        self.estilo.configure("labelCrearGrupo.TLabel",
                              background="#f0f0f0",
                              foreground="#333333",
                              font=("Arial", 11))

        # Estilo para el subtítulo del ciclo
        self.estilo.configure("subtituloCrearGrupo.TLabel",
                              background="#f0f0f0",
                              foreground="#666666",
                              font=("Arial", 10))

        # Estilo para botón guardar
        self.estilo.configure("botonGuardar.TButton",
                              background="#28a745",
                              foreground="white",
                              font=("Arial", 11, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonGuardar.TButton",
                        background=[("pressed", "#1e7e34"), ("active", "#34ce57")])

        # Estilo para botón cancelar
        self.estilo.configure("botonCancelar.TButton",
                              background="#6c757d",
                              foreground="white",
                              font=("Arial", 11, "bold"),
                              borderwidth=0,
                              relief="flat")
        self.estilo.map("botonCancelar.TButton",
                        background=[("pressed", "#5a6268"), ("active", "#78848b")])

    def crear_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        self.frame_principal = ttk.Frame(self, style="frameCrearGrupo.TFrame")
        self.frame_principal.pack(fill="both", expand=True, padx=30, pady=30)

        # Título
        titulo_label = ttk.Label(self.frame_principal,
                                 text="Crear Grupo",
                                 style="tituloCrearGrupo.TLabel")
        titulo_label.pack(pady=(0, 10))

        # Subtítulo con información del ciclo
        if self.ciclo_info:
            subtitulo_text = f"Ciclo: {self.ciclo_info[1]}"
            subtitulo_label = ttk.Label(self.frame_principal,
                                        text=subtitulo_text,
                                        style="subtituloCrearGrupo.TLabel")
            subtitulo_label.pack(pady=(0, 20))

        # Campo Nombre del grupo
        self.crear_campo_nombre()

        # Campo Colaborador (Tutor)
        self.crear_campo_colaborador()

        # Campo Capacidad
        self.crear_campo_capacidad()

        # Botones
        self.crear_botones()

    def crear_campo_nombre(self):
        """Crear el campo para el nombre del grupo"""
        # Frame para el campo nombre
        frame_nombre = ttk.Frame(self.frame_principal, style="frameCrearGrupo.TFrame")
        frame_nombre.pack(fill="x", pady=(0, 15))

        # Label
        label_nombre = ttk.Label(frame_nombre,
                                 text="Nombre del grupo",
                                 style="labelCrearGrupo.TLabel")
        label_nombre.pack(anchor="w", pady=(0, 5))

        # Entry
        self.entry_nombre = ttk.Entry(frame_nombre,
                                      textvariable=self.nombre_grupo_var,
                                      font=("Arial", 11),
                                      width=40)
        self.entry_nombre.pack(fill="x")

        # Placeholder text
        self.entry_nombre.insert(0, "Grupo A")
        self.entry_nombre.bind('<FocusIn>', self.on_entry_focus_in)
        self.entry_nombre.bind('<FocusOut>', self.on_entry_focus_out)

    def crear_campo_colaborador(self):
        """Crear el campo para seleccionar colaborador"""
        # Frame para el campo colaborador
        frame_colaborador = ttk.Frame(self.frame_principal, style="frameCrearGrupo.TFrame")
        frame_colaborador.pack(fill="x", pady=(0, 15))

        # Label
        label_colaborador = ttk.Label(frame_colaborador,
                                      text="Colaborador (Tutor)",
                                      style="labelCrearGrupo.TLabel")
        label_colaborador.pack(anchor="w", pady=(0, 5))

        # Combobox
        self.combo_colaborador = ttk.Combobox(frame_colaborador,
                                              textvariable=self.colaborador_var,
                                              font=("Arial", 11),
                                              width=37,
                                              state="readonly")
        self.combo_colaborador.pack(fill="x")

        # Configurar placeholder
        self.combo_colaborador.set("-- Seleccionar --")

    def crear_campo_capacidad(self):
        """Crear el campo para la capacidad"""
        # Frame para el campo capacidad
        frame_capacidad = ttk.Frame(self.frame_principal, style="frameCrearGrupo.TFrame")
        frame_capacidad.pack(fill="x", pady=(0, 25))

        # Label
        label_capacidad = ttk.Label(frame_capacidad,
                                    text="Capacidad",
                                    style="labelCrearGrupo.TLabel")
        label_capacidad.pack(anchor="w", pady=(0, 5))

        # Entry
        self.entry_capacidad = ttk.Entry(frame_capacidad,
                                         textvariable=self.capacidad_var,
                                         font=("Arial", 11),
                                         width=40)
        self.entry_capacidad.pack(fill="x")

        # Validación para solo números
        self.entry_capacidad.bind('<KeyPress>', self.validar_solo_numeros)

        # Placeholder
        self.entry_capacidad.insert(0, "25")
        self.entry_capacidad.bind('<FocusIn>', self.on_capacidad_focus_in)
        self.entry_capacidad.bind('<FocusOut>', self.on_capacidad_focus_out)

    def crear_botones(self):
        """Crear los botones de acción"""
        # Frame para botones
        frame_botones = ttk.Frame(self.frame_principal, style="frameCrearGrupo.TFrame")
        frame_botones.pack(fill="x", pady=(10, 0))

        # Botón Guardar
        self.boton_guardar = ttk.Button(frame_botones,
                                        text="Guardar",
                                        style="botonGuardar.TButton",
                                        command=self.guardar_grupo)
        self.boton_guardar.pack(side="left", padx=(0, 10), ipadx=20, ipady=8)

        # Botón Cancelar
        self.boton_cancelar = ttk.Button(frame_botones,
                                         text="Cancelar",
                                         style="botonCancelar.TButton",
                                         command=self.cancelar)
        self.boton_cancelar.pack(side="left", ipadx=20, ipady=8)

    def cargar_colaboradores(self):
        """Cargar los colaboradores disponibles en el combobox"""
        try:
            self.colaboradores_data = obtener_colaboradores_activos()

            if self.colaboradores_data:
                # Preparar lista de nombres para el combobox
                nombres_colaboradores = [
                    f"{colaborador[1]}" for colaborador in self.colaboradores_data
                ]
                self.combo_colaborador['values'] = nombres_colaboradores
            else:
                self.combo_colaborador['values'] = ["No hay colaboradores disponibles"]
                self.combo_colaborador.set("No hay colaboradores disponibles")
                self.boton_guardar.configure(state="disabled")
                messagebox.showwarning("Advertencia",
                                       "No hay colaboradores disponibles para asignar al grupo")

        except Exception as e:
            print(f"❌ Error al cargar colaboradores: {e}")
            messagebox.showerror("Error", f"Error al cargar colaboradores: {str(e)}")
            self.combo_colaborador['values'] = ["Error al cargar colaboradores"]
            self.combo_colaborador.set("Error al cargar colaboradores")
            self.boton_guardar.configure(state="disabled")

    def validar_solo_numeros(self, event):
        """Validar que solo se ingresen números en el campo capacidad"""
        # Permitir teclas de control (backspace, delete, etc.)
        if event.keysym in ['BackSpace', 'Delete', 'Left', 'Right', 'Tab']:
            return True

        # Permitir solo números
        if not event.char.isdigit():
            return "break"

        return True

    def on_entry_focus_in(self, event):
        """Manejar el focus in del campo nombre"""
        if self.entry_nombre.get() == "Grupo A":
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.configure(foreground="black")

    def on_entry_focus_out(self, event):
        """Manejar el focus out del campo nombre"""
        if not self.entry_nombre.get().strip():
            self.entry_nombre.insert(0, "Grupo A")
            self.entry_nombre.configure(foreground="gray")

    def on_capacidad_focus_in(self, event):
        """Manejar el focus in del campo capacidad"""
        if self.entry_capacidad.get() == "25":
            self.entry_capacidad.delete(0, tk.END)
            self.entry_capacidad.configure(foreground="black")

    def on_capacidad_focus_out(self, event):
        """Manejar el focus out del campo capacidad"""
        if not self.entry_capacidad.get().strip():
            self.entry_capacidad.insert(0, "25")
            self.entry_capacidad.configure(foreground="gray")

    def obtener_id_colaborador_seleccionado(self):
        """Obtener el ID del colaborador seleccionado"""
        nombre_seleccionado = self.colaborador_var.get()

        if not nombre_seleccionado or nombre_seleccionado == "-- Seleccionar --":
            return None

        # Buscar el ID del colaborador por nombre
        for colaborador in self.colaboradores_data:
            if colaborador[1] == nombre_seleccionado:
                return colaborador[0]

        return None

    def validar_formulario(self):
        """Validar los datos del formulario"""
        errores = []

        # Validar nombre del grupo
        nombre = self.nombre_grupo_var.get().strip()
        if not nombre or nombre == "Grupo A":
            errores.append("El nombre del grupo es obligatorio")
        elif len(nombre) < 2:
            errores.append("El nombre del grupo debe tener al menos 2 caracteres")
        elif len(nombre) > 45:
            errores.append("El nombre del grupo no puede exceder 45 caracteres")

        # Validar colaborador
        id_colaborador = self.obtener_id_colaborador_seleccionado()
        if not id_colaborador:
            errores.append("Debe seleccionar un colaborador")

        # Validar capacidad
        capacidad = self.capacidad_var.get().strip()
        if not capacidad or capacidad == "25":
            errores.append("La capacidad es obligatoria")
        else:
            try:
                capacidad_int = int(capacidad)
                if capacidad_int <= 0:
                    errores.append("La capacidad debe ser mayor a 0")
                elif capacidad_int > 999:
                    errores.append("La capacidad no puede exceder 999 estudiantes")
            except ValueError:
                errores.append("La capacidad debe ser un número válido")

        return errores

    def guardar_grupo(self):
        """Guardar el nuevo grupo"""
        try:
            # Validar formulario
            errores = self.validar_formulario()
            if errores:
                mensaje_error = "Se encontraron los siguientes errores:\n\n"
                mensaje_error += "\n".join(f"• {error}" for error in errores)
                messagebox.showerror("Errores de validación", mensaje_error)
                return

            # Deshabilitar botón para evitar doble click
            self.boton_guardar.configure(state="disabled", text="Guardando...")

            # Obtener datos del formulario
            nombre_grupo = self.nombre_grupo_var.get().strip()
            capacidad = int(self.capacidad_var.get().strip())
            id_colaborador = self.obtener_id_colaborador_seleccionado()
            id_ciclo = self.ciclo_info[0]  # ID del ciclo

            # Llamar al modelo para crear el grupo
            resultado = agregar_grupo(nombre_grupo, capacidad, id_colaborador, id_ciclo)

            if resultado:
                # Éxito
                messagebox.showinfo("Éxito",
                                    f"El grupo '{nombre_grupo}' ha sido creado exitosamente")

                # Llamar callback para actualizar la vista principal
                if self.callback_actualizar:
                    self.callback_actualizar()

                # Cerrar la ventana
                self.destroy()
            else:
                # Error
                messagebox.showerror("Error",
                                     "No se pudo crear el grupo. Verifique los datos e intente nuevamente.")
                # Rehabilitar botón
                self.boton_guardar.configure(state="normal", text="Guardar")

        except Exception as e:
            print(f"❌ Error al guardar grupo: {e}")
            messagebox.showerror("Error", f"Error inesperado al guardar: {str(e)}")
            # Rehabilitar botón
            self.boton_guardar.configure(state="normal", text="Guardar")

    def cancelar(self):
        """Cancelar y cerrar la ventana"""
        self.destroy()

    def destroy(self):
        """Override del método destroy para limpiar recursos"""
        # Remover bindings del mousewheel si existen
        try:
            self.unbind_all("<MouseWheel>")
        except:
            pass

        super().destroy()