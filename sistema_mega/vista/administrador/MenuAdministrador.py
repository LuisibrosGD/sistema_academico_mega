from tkinter import ttk
import tkinter as tk

from sistema_mega.vista.login import LoginVentana


# Realizado por Luis Bizarro
class MenuAdministrador(tk.Toplevel):
    def __init__(self, id_usuario, nombre_administrador):
        super().__init__()

        self.configurar_ventana()
        self.centrar_ventana()

        # obtencion de id y nombre
        self.id_usuario = id_usuario
        self.nombre_administrador = nombre_administrador

        self.agregar_mas_widgets()
        self.aplicar_estilos()

    def aplicar_estilos(self):
        estilo = ttk.Style()
        estilo.theme_use("clam")

        # Estilo general para los demás botones
        estilo.configure("BotonClaro.TButton",
                         background="#d0f0fd",
                         foreground="black",
                         font=("Segoe UI", 10, "bold"),
                         padding=8)
        estilo.map("BotonClaro.TButton",
                   background=[("active", "#b0e0f8")])

        # Estilo específico para el botón de salir
        estilo.configure("BotonRojo.TButton",
                         background="#f8d7da",  # rojo claro
                         foreground="black",
                         font=("Segoe UI", 10, "bold"),
                         padding=8)
        estilo.map("BotonRojo.TButton",
                   background=[("active", "#f5c2c7")])
        estilo.configure("FondoBlanco.TFrame", background="white")

    def configurar_ventana(self):
        self.title("Panel del Administrador")
        self.geometry("800x600")
        self.configure(bg="white")

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
        # Crear un frame principal
        frame_principal = ttk.Frame(self, padding = 20, style="FondoBlanco.TFrame")
        frame_principal.grid(row=0,column=0,sticky="nsew")

        # Configurar grillas del frame principal
        frame_principal.rowconfigure(0, weight=1)
        frame_principal.rowconfigure(1, weight=1)
        frame_principal.rowconfigure(2, weight=1)
        frame_principal.rowconfigure(3, weight=1)
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.columnconfigure(1, weight=1)
        frame_principal.columnconfigure(2, weight=1)

        # Agregacion de widgets al frame_principal
        label1 = ttk.Label(frame_principal, text=f"Bienvenido {self.nombre_administrador}",
                           font=("Segoe UI", 16, "bold"),
                           background="white")

        label1.grid(row=0, column=0, sticky="e")

        boton_salir = ttk.Button(frame_principal, text="Salir", style="BotonRojo.TButton", command=self.salir)
        boton_salir.grid(row=0, column=2, sticky="e")

        boton_g_admin = ttk.Button(frame_principal, text = "Gestionar administradores", style="BotonClaro.TButton", command=self.abrir_ventana_g_admin)
        boton_g_admin.grid(row=1, column=0, sticky="nsew", padx=10,pady=10)
        boton_g_colab = ttk.Button(frame_principal, text = "Gestionar colaboradores", style="BotonClaro.TButton", command=self.abrir_ventana_g_colab)
        boton_g_colab.grid(row=1,column=1,sticky="nsew", padx=10,pady=10)
        boton_g_prof = ttk.Button(frame_principal, text = "Gestionar profesores", style="BotonClaro.TButton", command=self.abrir_ventana_g_prof)
        boton_g_prof.grid(row=1,column=2,sticky="nsew", padx=10,pady=10)

        boton_g_ciclos = ttk.Button(frame_principal, text="Gestionar ciclos", style="BotonClaro.TButton", command=self.abrir_ventana_g_ciclos)
        boton_g_ciclos.grid(row=2, column=0, sticky="nsew", padx=10,pady=10)
        boton_g_especialidades = ttk.Button(frame_principal, text="Gestionar especialidades", style="BotonClaro.TButton", command=self.abrir_ventana_g_especialidades)
        boton_g_especialidades.grid(row=2, column=1, sticky="nsew", padx=10,pady=10)
        boton_asg_ciclos = ttk.Button(frame_principal, text="Asignar ciclos a profesores", style="BotonClaro.TButton", command=self.abrir_ventana_asg_ciclos)
        boton_asg_ciclos.grid(row=2, column=2, sticky="nsew", padx=10,pady=10)

        boton_r_estud = ttk.Button(frame_principal, text="Registro de estudiantes", style="BotonClaro.TButton", command=self.abrir_ventana_r_estud)
        boton_r_estud.grid(row=3, column=0, sticky="nsew", padx=10,pady=10)
        boton_n_estud = ttk.Button(frame_principal, text="Notas Estudiantes", style="BotonClaro.TButton", command=self.abrir_ventana_n_estud)
        boton_n_estud.grid(row=3, column=1, sticky="nsew", padx=10,pady=10)

    def abrir_ventana_g_admin(self):
        from sistema_mega.vista.administrador.GestionAdministradores import GestionAdministradores
        self.withdraw()  # Oculta esta ventana
        ventana = GestionAdministradores(self)
        ventana.grab_set()


    def abrir_ventana_g_colab(self):
        from sistema_mega.vista.administrador.GestionColaboradores import GestionColaboradores
        self.withdraw()
        ventana = GestionColaboradores(self)
        ventana.grab_set()

    def abrir_ventana_g_prof(self):
        from sistema_mega.vista.administrador.GestionProfesores import GestionProfesores
        self.withdraw()
        ventana = GestionProfesores(self)
        ventana.grab_set()

    def abrir_ventana_g_ciclos(self):
        from sistema_mega.vista.administrador.vista_gestionar_sedes import GestionarSedes
        self.withdraw()
        ventana = GestionarSedes(self)
        ventana.grab_set()  # Bloquea interacción con esta ventana

    def abrir_ventana_g_especialidades(self):
        from sistema_mega.vista.administrador.EspecialidadVista import EspecialidadVista
        self.withdraw()
        ventana = EspecialidadVista(self)
        ventana.grab_set()  # Bloquea interacción con esta ventana



    def abrir_ventana_asg_ciclos(self):
        from sistema_mega.vista.administrador.vista_asignar_profesor_ciclo import AsignarProfesorCiclo
        self.withdraw()  # Oculta esta ventana
        ventana = AsignarProfesorCiclo(self)
        ventana.grab_set()

    def abrir_ventana_r_estud(self):
        from sistema_mega.vista.administrador.Registrar_estudiante import VistaRegistroEstudiante
        self.withdraw()  # Oculta esta ventana
        ventana = VistaRegistroEstudiante(self)
        ventana.grab_set()

    def abrir_ventana_n_estud(self):
        from sistema_mega.vista.administrador.vista_ver_notas_e import VistaNotasEstudiantes
        self.withdraw()  # Oculta esta ventana
        ventana = VistaNotasEstudiantes(self)
        ventana.grab_set()


    def salir(self):
        self.destroy()
        app = LoginVentana()
        app.mainloop()



if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana raíz
    app1 = MenuAdministrador(1, "Luis")
    app1.mainloop()