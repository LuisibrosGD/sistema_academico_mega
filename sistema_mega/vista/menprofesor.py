from sistema_mega.modelo.profesor_modelo import *

class Login_profesor:

    def consola_menprofesor(self):
        while(True):
            print("Menu Profesores")
            print("1.Ver Grupos Asignados")
            print("2.Ver Asistencias")
            print("0. Salir")

            respuesta = int(input('Seleccione la respuesta que quiere: '))

            if respuesta == 1:
                print("Ver Grupos Asignados")
                self.ver_grupos_asignados()
            elif respuesta == 2:
                print("Ver Asistencias")
                self.ver_asistencias()
            elif respuesta == 0:
                print("Saliendo del programa")
                break
            else:
                print("respuesta no valido")

    def ver_grupos_asignados(self):
        ver_grupos_asignados()

    def ver_asistencias(self):
        id_profesor = int(input("Ingrese su ID de profesor: "))
        # Consultar ID profesor (futura entrega)
        ver_asistencias(id_profesor)


