from sistema_mega.modelo.administrador_modelo import *
from sistema_mega.modelo.estudiante_modelo import *
class Login_Estudiante:
    def consola_menestudiante(self):
        while(True):
            print("Bienvenido al sistema de estudiantes")
            print("1. Ver oferta de ciclos")
            print("2. Ver pagos realizados")
            print("3. Ver notas")
            print("0. Salir")

            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                print("Menu oferta ciclos")
                self.ver_cicloprogramado()
            elif opcion == 2:
                print("Menu pagos realizados")
                self.ver_pagos()
            elif opcion == 3:
                print("Menu notas")
                self.ver_notas()
            elif opcion == 0:
                print("Salir")
                break
            else:
                print("Opcion invalida")
                break

    def ver_cicloprogramado(self):
        ciclos_datos = ver_cicloprogramado()

        for dato in ciclos_datos:
            print(f"Nombre ciclo: {dato[0]}")
            print(f"Modalidad: {dato[1]}")
            print(f"Precio: {dato[2]}")
            print(f"Fecha inicio: {dato[3]}")
            print(f"Fecha final: {dato[4]}")
            print("------------------------------")

    def ver_pagos(self):

        id_estudiante = int(input("Ingrese su id de estudiante: "))

        pagos_datos = ver_pagos(id_estudiante)

        if pagos_datos is None:
            print("No hay pagos realizados")
            return

        contador = 0
        for dato in pagos_datos:
            print(f"Pago {contador+1}")
            print(f"Ciclo: {dato[0]}")
            print(f"Fecha_inscripcion: {dato[1]}")
            print(f"Monto: S/.{dato[2]}")
            print(f"Fecha pago: {dato[3]}")
            print("----------------------------------------")
            contador = contador + 1

    def ver_notas(self):
        id_estudiante = int(input("Ingrese su id de estudiante: "))
        notas_datos = ver_notas(id_estudiante)
        if notas_datos is None:
            print("No hay notas de examenes realizados")
            return

        contador = 0
        for dato in notas_datos:
            print(f"Examen {contador+1}:")
            print(f"Puntaje: {dato[0]}")
            print(f"Fecha realizacion: {dato[1]}")
            print("-----------------------------------------")
            contador = contador + 1


