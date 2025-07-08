from sistema_mega.modelo.colaborador_modelo import *

class Login_colab:

    def consola_mencolab(self):
        while (True):
            print("1. Registrar asistencia")
            print("2. Registrar calificaciones")
            print("3. Ver calificaciones")
            print("4. Salir")

            opcion = int(input('Seleccione la opcion que quiere: '))

            if opcion == 1:
                id_profesor = int(input("Ingrese el ID del profesor: "))
                estado = input("Ingrese el estado (presente/tarde/ausente): ")
                registrar_asistencia(estado, id_profesor)
                nombre_profesor = obtener_nombre_profesor(id_profesor)
                fecha= obtener_fecha(id_profesor)
                print(f"✅ Asistencia registrada correctamente.")
                print(f"👨‍🏫 Profesor: {nombre_profesor}")
                print(f"📅 Fecha: {fecha}")

            elif opcion == 2:
                id_estudiante = int(input("Ingrese el ID del estudiante: "))
                puntaje = float(input("Ingrese el puntaje(en decimal): "))
                fecha_realizacion = input("Ingrese la fecha de realización (YYYY-MM-DD): ")
                registrar_calificacion(id_estudiante, puntaje, fecha_realizacion)
                print("✅ Calificación registrada correctamente.")

            elif opcion == 3:
                id_estudiante = int(input("Ingrese el ID del estudiante: "))
                ver_calificaciones(id_estudiante)

            elif opcion == 4:
                print("👋 Saliendo del sistema.")
                break
            else:
                print("❌ Opción no válida. Intente nuevamente.")