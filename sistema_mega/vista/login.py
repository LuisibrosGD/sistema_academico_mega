import tkinter as tk
from tkinter import messagebox
from sistema_mega.modelo.login_modelo import verificar_cuenta

class LoginVentana(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("350x300")
        self.resizable(False, False)
        self.centrar_ventana()

        # Título
        tk.Label(self, text="Iniciar Sesión", font=("Arial", 16, "bold")).pack(pady=10)

        # Usuario
        tk.Label(self, text="Usuario:", anchor="w").pack(fill="x", padx=30)
        self.usuario_entry = tk.Entry(self)
        self.usuario_entry.pack(padx=30, pady=5, fill="x")

        # Contraseña
        tk.Label(self, text="Contraseña:", anchor="w").pack(fill="x", padx=30)
        self.contrasena_entry = tk.Entry(self, show="*")
        self.contrasena_entry.pack(padx=30, pady=5, fill="x")

        # Botón Ingresar
        self.boton_ingresar = tk.Button(self, text="Ingresar", bg="#2196F3", fg="white", command=self.verificar_login)
        self.boton_ingresar.pack(pady=10)

        # Advertencia
        tk.Label(self, text="No compartas tus credenciales", fg="gray").pack()

        # Botón Invitado
        self.boton_invitado = tk.Button(self, text="Entrar como invitado", command=self.entrar_como_invitado)
        self.boton_invitado.pack(pady=10)

    def centrar_ventana(self):
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        contrasena = self.contrasena_entry.get()

        datos_usuario = verificar_cuenta(usuario,contrasena)
        self.id = None
        self.rol = None
        self.nombre = None
        if datos_usuario:
            self.id, self.nombre, correo, contra, fecha_cre, estado, self.rol = datos_usuario
            self.abrir_menu(self.rol)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

    def abrir_menu(self, rol):
        self.withdraw()
        if rol == "administrador":
            self.abrir_interfaz_administrador(self.id, self.nombre)
        elif rol == "colaborador":
            self.abrir_interfaz_colaborador(self.id, self.nombre)
        elif rol == "estudiante":
            self.abrir_interfaz_estudiante(self.id, self.nombre)
        elif rol == "profesor":
            self.abrir_interfaz_profesor(self.id, self.nombre)

    def abrir_interfaz_administrador(self, id, nombre):
        from sistema_mega.vista.administrador.MenuAdministrador import MenuAdministrador
        app = MenuAdministrador(id,nombre)
        app.mainloop()

    def abrir_interfaz_colaborador (self, id_usuario, nombre_usuario):
        from sistema_mega.modelo.colaborador_modelo import FuncionesColaborador
        id_colab = FuncionesColaborador.obtener_id_colaborador_por_usuario(id_usuario)

        if id_colab is None:
            messagebox.showerror("Error", "No se encontró el colaborador asociado a esta cuenta")
            return

        from sistema_mega.vista.colaborador.MenuColaborador import MenuColaborador
        app = MenuColaborador(nombre_usuario, id_colab)  # ← nombre primero, id segundo
        app.mainloop()

    def abrir_interfaz_estudiante(self, id, nombre):
        from sistema_mega.vista.estudiante.MenuEstudiante import MenuEstudiante
        app = MenuEstudiante(id, nombre)
        app.mainloop()

    def abrir_interfaz_profesor(self, id, nombre):
        from sistema_mega.vista.profesor.MenuProfesor import MenuProfesor
        app = MenuProfesor(id,nombre)
        app.mainloop()

    def entrar_como_invitado(self):
        from sistema_mega.vista.invitado.ventana_invitado import MenuInvitado
        app = MenuInvitado()
        app.mainloop()


# Ejecutar interfaz
if __name__ == "__main__":
    app1 = LoginVentana()
    app1.mainloop()









