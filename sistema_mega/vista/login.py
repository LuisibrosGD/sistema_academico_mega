#cargando modelo
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

class Login:

    def consola_login(self):

        while(True):
            global rol
            global encontrar
            print("Iniciar sesión")
            nombre_usuario = input("Usuario: ")
            contrasenia = input("Password: ")
            rol = input("rol (administrador/colaborador/estudiante/profesor): ")

            # necesito verificar la contrasenia y obtener el rol
            respuesta = verificar_cuenta(nombre_usuario, contrasenia, rol)

            if respuesta is None:
                print("El usuario no existe")

            else:
                print("Usuario encontrado")
                encontrar = True
                break

        if encontrar:
            if rol == "administrador":
                print("Menu administrador")
                objetoAdmin = Login_admin()
                objetoAdmin.consola_menadmin()
            elif rol == "colaborador":
                print("Menu colaborador")
                objetoColab = Login_colab()
                objetoColab.consola_mencolab()
            elif rol == "estudiante":
                print("Menu estudiante")
                objetoEstudiante = Login_Estudiante()
                objetoEstudiante.consola_menestudiante()
            elif rol == "profesor":
                print("Menu profesor")
                objetoProfe = Login_profesor()
                objetoProfe.consola_menprofesor()
            else:
                print("rol no valido")










