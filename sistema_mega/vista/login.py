#cargando modelo
from sistema_mega.modelo.login_modelo import verificar_cuenta
#cargando vistas
from sistema_mega.vista.menadmin import Login_admin
from sistema_mega.vista.mencolaborador import Login_colab
from sistema_mega.vista.menestudiante import Login_Estudiante
from sistema_mega.vista.menprofesor import Login_profesor

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










