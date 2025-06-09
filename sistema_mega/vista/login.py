
class Login:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def consola_login(self):
        global rol

        while(True):
            print("Iniciar sesión")
            nombre_usuario = input("Usuario: ")
            contrasenia = input("Password: ")
            rol = input("rol: (administrador/colaborador/estudiante/profesor)")

            # necesito verificar la contrasenia y obtener el rol

