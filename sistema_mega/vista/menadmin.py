# Modelos
from sistema_mega.modelo.administrador_modelo import *
from sistema_mega.modelo.usuarios_modelo import *

#Conexion BD
from sistema_mega.database.conexion import ejecutar_select, ejecutar_modificacion

class Login_admin:
    def consola_menadmin(self):
        while(True):
            print("Menu administrador")
            print("1. Gestionar usuarios")
            print("2. Gestionar ciclos programados")
            print("3. Gestionar cursos y especialidades")
            print("4. Asignar profesores a ciclos")
            print("5. Generar reportes")
            print("6. Gestionar sedes")
            print("0. Salir")

            respuesta = int(input('Seleccione la respuesta que quiere: '))

            if respuesta == 1:
                print("Menu Gestionar usuarios")
                self.gestionar_usuarios()
            elif respuesta == 2:
                print("Menu Gestionar ciclos")
                self.gestionar_ciclosprogramados()
            elif respuesta == 3:
                print("Menu Gestionar cursos y especialidades")
                self.gestionar_cursos_y_especialidades()
            elif respuesta == 4:
                print("Menu Asignar profesores a ciclos")
            elif respuesta == 5:
                print("Menu Generar Reportes")
            elif respuesta == 6:
                print("Menu Gestionar sedes")
                self.gestionar_sedes()
            elif respuesta == 0:
                print("Saliendo del programa")
                break
            else:
                print("respuesta no valido")


    def gestionar_ciclosprogramados(self):
        while(True):
            print("Menu Gestionar Ciclos Programados")
            print("1.Crear Ciclos Programados")
            print("2.Modificar Ciclos Programados")
            print("3.Desactivar Ciclos Programados")
            print("4.Ver los ciclos programados")
            print("0. Salir")
            opc= int(input('Seleccione la opcion que quiere: '))

            if opc == 1:
                print("CREE SU CICLO -------------------------")
                nombre_ciclo = input("Ingrese su nombre de ciclo: ")
                modalidad = input("Ingrese modalidad: ")
                costo = input("Ingrese su costo (Incluya decimal): ")
                fecha_inicio=input("Ingrese fecha de inicio: ")
                fecha_fin=input("Ingrese fecha de fin: ")
                crear_ciclo_programado(nombre_ciclo, modalidad, costo, fecha_inicio, fecha_fin)
            elif opc == 2:
                print("MODIFIQUE SU CICLO -------------------------")
            elif opc == 3:
                print("DESACTIVE SU CICLO")
            elif opc == 4:
                 ver_cicloprogramado()
            elif opc == 5:
                print("SALIR")
            else:
                print("Opcion no valida")
                break

    # ---------------------------------------------------------------
    def gestionar_usuarios(self):
        while(True):
            print("Menu Gestionar usuarios")
            print("1.Gestionar Administradores")
            print("2.Gestionar Colaboradores")
            print("3.Gestionar Profesores")
            print("4.Gestionar Estudiantes")
            print("0. Salir")

            opcion = int(input('Seleccione la opcion que quiere: '))

            if opcion == 1:
                print("Menu Gestionar Administradores")
                self.gestionar_administradores()
            elif opcion == 2:
                print("Menu Gestionar Colaboradores")
                self.gestionar_colaboradores()
            elif opcion == 3:
                print("Menu Gestionar Profesores")
                self.gestionar_profesores()
            elif opcion == 4:
                print("Menu Gestionar Estudiantes")
                self.gestionar_estudiantes()
            elif opcion == 0:
                print("Volviendo a menu administrador")
                break
            else:
                print("opcion no valido")
                break


    def gestionar_administradores(self):
        while(True):
            print("1. Crear administrador")
            print("2. Editar administrador")
            print("3. Ver administradores")
            print("0. Salir")
            opcion = int(input('Seleccione la opcion que quiere: '))
            if opcion == 1:
                print("CREE SU USUARIO -------------------------")
                nombre_usuario = input("Ingrese su nombre de usuario: ")
                correo = input("Ingrese su nombre de correo: ")
                contrasena = input("Ingrese su contrasena (>8 caracteres): ")

                print("INGRESE SUS DATOS --------------------------")
                nombre = input("Ingrese su nombre: ")
                ap_paterno = input("Ingrese su apellido paterno: ")
                ap_materno = input("Ingrese su apellido materno: ")
                tipo_dcmto = input("Tipo de documento (dni/carnet): ")
                nro_dcmto = input("Nro de documento: ")

                crear_administrador(nombre_usuario,correo,contrasena,nombre,ap_paterno,ap_materno,tipo_dcmto,nro_dcmto)
            elif opcion == 2:
                ver_administradores()
                id_admin = int(input('Seleccione ID del administrador:           (0 para cancelar)'))

                if id_admin == 0:
                    print("Operacion cancelada")
                    continue
                else:

                    sql = """
                                        SELECT p.nombre, p.ap_paterno, p.ap_materno, p.tipo_documento, p.nro_documento,
                                            u.nombre_usuario, u.correo, u.contrasenia
                                        FROM profesores p
                                        JOIN usuarios u
                                        ON p.id_usuario = u.id_usuario
                                        WHERE id_profesor = %s
                                    """
                    tupla_admin = (id_admin,)
                    datos_admin = ejecutar_select(sql, tupla_admin)
                    print(datos_admin)
                    nuevo_nombre = input(f"Ingrese su nombre (Nombre anterior {datos_admin[0][0]}): ")
                    nuevo_ap_pat = input(f"Ingrese su apellido paterno (Ap paterno anterior {datos_admin[0][1]}): ")
                    nuevo_ap_mat = input(f"Ingrese su apellido materno (Ap materno anterior {datos_admin[0][2]}): ")
                    nuevo_tip_dcmto = input(
                        f"Ingrese el nuevo tipo de documento (dni/carnet) (anterior {datos_admin[0][3]}): ")
                    nuevo_nro_dcmto = input(f"Ingrese el nuevo # de documento (anterior {datos_admin[0][4]}): ")
                    nuevo_correo = input(f"Ingrese el nuevo correo (anterior {datos_admin[0][5]}): ")
                    nuevo_contrasena = input(f"Ingrese nueva contrasenia (anterior {datos_admin[0][6]}): ")

                    editar_administrador(id_admin, nuevo_nombre, nuevo_ap_pat, nuevo_ap_mat, nuevo_tip_dcmto,
                                    nuevo_nro_dcmto, nuevo_correo, nuevo_contrasena)
            elif opcion == 3:
                ver_administradores()
            elif opcion == 0:
                print("Saliendo")
                break
            else:
                print("opcion incorrecta")

    def gestionar_profesores(self):
        while(True):
            print("Menu Gestionar Profesores")
            print("1. Crear profesores")
            print("2. Editar profesores")
            print("3. Ver profesores")
            print("4. Desactivar/activar cuentas")
            print("5. Agregar especialidades a profesor")
            print("0. Salir")
            opciones = int(input('Seleccione la opcion que quiere: '))
            if opciones == 1:
                print("CREE SU USUARIO -------------------------")
                nombre_usuario = input("Ingrese su nombre de usuario: ")
                correo = input("Ingrese su nombre de correo: ")
                contrasena = input("Ingrese su contrasena (>8 caracteres): ")

                print("INGRESE SUS DATOS --------------------------")
                nombre = input("Ingrese su nombre: ")
                ap_paterno = input("Ingrese su apellido paterno: ")
                ap_materno = input("Ingrese su apellido materno: ")
                tipo_dcmto = input("Tipo de documento (dni/carnet): ")
                nro_dcmto = input("Nro de documento: ")

                crear_profesor(nombre_usuario,correo,contrasena,nombre,ap_paterno,ap_materno,tipo_dcmto,nro_dcmto)
            elif opciones == 2:
                ver_profesores()
                id_profe = int(input('Seleccione ID del profesor:           (0 para cancelar)'))

                if id_profe == 0:
                    print("Operacion cancelada")
                    continue
                else:

                    sql = """
                        SELECT p.nombre, p.ap_paterno, p.ap_materno, p.tipo_documento, p.nro_documento,
                            u.nombre_usuario, u.correo, u.contrasenia
                        FROM profesores p
                        JOIN usuarios u
                        ON p.id_usuario = u.id_usuario
                        WHERE id_profesor = %s
                    """
                    tupla_profe = (id_profe,)
                    datos_profe = ejecutar_select(sql,tupla_profe)
                    print(datos_profe)
                    nuevo_nombre = input(f"Ingrese su nombre (Nombre anterior {datos_profe[0][0]}): ")
                    nuevo_ap_pat = input(f"Ingrese su apellido paterno (Ap paterno anterior {datos_profe[0][1]}): ")
                    nuevo_ap_mat = input(f"Ingrese su apellido materno (Ap materno anterior {datos_profe[0][2]}): ")
                    nuevo_tip_dcmto = input(f"Ingrese el nuevo tipo de documento (dni/carnet) (anterior {datos_profe[0][3]}): ")
                    nuevo_nro_dcmto = input(f"Ingrese el nuevo # de documento (anterior {datos_profe[0][4]}): ")
                    nuevo_correo = input(f"Ingrese el nuevo correo (anterior {datos_profe[0][5]}): ")
                    nuevo_contrasena = input(f"Ingrese nueva contrasenia (anterior {datos_profe[0][6]}): ")

                    editar_profesor(id_profe, nuevo_nombre, nuevo_ap_pat,nuevo_ap_mat, nuevo_tip_dcmto, nuevo_nro_dcmto, nuevo_correo, nuevo_contrasena)

            elif opciones == 3:
                ver_profesores()


            elif opciones == 4:
                ver_profesores()
                id_profesor = int(input("Elija una ID: "))
                print("-------")
                print("1. Activar")
                print("0. Desactivar")
                opcion = int(input('Seleccione la opcion que quiere: '))
                activar_desactivar_cuenta_profesor(id_profesor,opcion)

            elif opciones == 5:
                ver_profesores()
                id_profesor = int(input("Elija una ID: "))
                ver_especialidades()
                id_especialidades = int(input("Elija una ID: "))
                agregar_especialidad_profesor(id_profesor, id_especialidades)

            else:
                print("Opcion no existe")




    def gestionar_colaboradores(self):
        while(True):

            print("1. Crear colaborador")
            print("2. Editar colaborador")
            print("3. Ver colaboradores")
            print("4. Desactivar o activar colaborador")
            print("0. Volver")

            opcion = int(input('Seleccione la opcion que quiere: '))
            if opcion == 1:
                print("CREE SU USUARIO -------------------------")
                nombre_usuario = input("Ingrese su nombre de usuario: ")
                correo = input("Ingrese su nombre de correo: ")
                contrasena = input("Ingrese su contrasena (>8 caracteres): ")

                print("INGRESE SUS DATOS --------------------------")
                nombre = input("Ingrese su nombre: ")
                ap_paterno = input("Ingrese su apellido paterno: ")
                ap_materno = input("Ingrese su apellido materno: ")
                tipo_dcmto = input("Tipo de documento (dni/carnet): ")
                nro_dcmto = input("Nro de documento: ")

                crear_colaborador(nombre_usuario, correo, contrasena, nombre,ap_paterno,ap_materno,tipo_dcmto,nro_dcmto)
            elif opcion == 2:
                ver_colaboradores()
                id_colab = int(input('Seleccione ID del colaborador:           (0 para cancelar)'))

                if id_colab == 0:
                    print("Operacion cancelada")
                    continue
                else:

                    sql = """
                                        SELECT p.nombre, p.ap_paterno, p.ap_materno, p.tipo_documento, p.nro_documento,
                                            u.nombre_usuario, u.correo, u.contrasenia
                                        FROM colaboradores p
                                        JOIN usuarios u
                                        ON p.id_usuario = u.id_usuario
                                        WHERE id_colaborador = %s
                                    """
                    tupla_colab = (id_colab,)
                    datos_colab = ejecutar_select(sql, tupla_colab)
                    print(datos_colab)
                    nuevo_nombre = input(f"Ingrese su nombre (Nombre anterior {datos_colab[0][0]}): ")
                    nuevo_ap_pat = input(f"Ingrese su apellido paterno (Ap paterno anterior {datos_colab[0][1]}): ")
                    nuevo_ap_mat = input(f"Ingrese su apellido materno (Ap materno anterior {datos_colab[0][2]}): ")
                    nuevo_tip_dcmto = input(
                        f"Ingrese el nuevo tipo de documento (dni/carnet) (anterior {datos_colab[0][3]}): ")
                    nuevo_nro_dcmto = input(f"Ingrese el nuevo # de documento (anterior {datos_colab[0][4]}): ")
                    nuevo_correo = input(f"Ingrese el nuevo correo (anterior {datos_colab[0][5]}): ")
                    nuevo_contrasena = input(f"Ingrese nueva contrasenia (anterior {datos_colab[0][6]}): ")

                    editar_colaborador(id_colab, nuevo_nombre, nuevo_ap_pat, nuevo_ap_mat, nuevo_tip_dcmto,
                                    nuevo_nro_dcmto, nuevo_correo, nuevo_contrasena)
            elif opcion == 3:
                ver_colaboradores()

            elif opcion == 0:
                print("Volviendo al menu")
                break
            else:
                print("Opcion incorrecta")




    def gestionar_estudiantes(self):

        while(True):
            print("1. Crear Estudiante") # El estudiante crea su cuenta y necesita de la autorizacion de un administrador (cuenta del admin)
            print("2. Editar Estudiante")
            print("3. Ver Estudiantes")
            print("4. Desactivar o activar Estudiante")
            print("0. Volver")

            opcion = int(input("Elija opcion: "))

            if opcion == 1:
                print("CREE SU USUARIO -------------------------")
                nombre_usuario = input("Ingrese su nombre de usuario: ")
                correo = input("Ingrese su nombre de correo: ")
                contrasena = input("Ingrese su contrasena (>8 caracteres): ")

                print("INGRESE SUS DATOS --------------------------")
                nombre = input("Ingrese su nombre: ")
                ap_paterno = input("Ingrese su apellido paterno: ")
                ap_materno = input("Ingrese su apellido materno: ")
                tipo_dcmto = input("Tipo de documento (dni/carnet): ")
                nro_dcmto = input("Nro de documento: ")
                area_academica = input("Area academica (a/b/c/d/e): ")

                crear_estudiante(nombre_usuario, correo, contrasena, nombre, ap_paterno, ap_materno, tipo_dcmto,
                                  nro_dcmto, area_academica)

            elif opcion == 2:
                ver_colaboradores()
                id_colab = int(input('Seleccione ID del estudiante:           (0 para cancelar)'))

                if id_colab == 0:
                    print("Operacion cancelada")
                    continue
                else:

                    sql = """
                                                        SELECT p.nombre, p.ap_paterno, p.ap_materno, p.tipo_documento, p.nro_documento,
                                                            u.nombre_usuario, u.correo, u.contrasenia
                                                        FROM estudiantes p
                                                        JOIN usuarios u
                                                        ON p.id_usuario = u.id_usuario
                                                        WHERE id_estudiante = %s
                                                    """
                    tupla_colab = (id_colab,)
                    datos_colab = ejecutar_select(sql, tupla_colab)
                    print(datos_colab)
                    nuevo_nombre = input(f"Ingrese su nombre (Nombre anterior {datos_colab[0][0]}): ")
                    nuevo_ap_pat = input(f"Ingrese su apellido paterno (Ap paterno anterior {datos_colab[0][1]}): ")
                    nuevo_ap_mat = input(f"Ingrese su apellido materno (Ap materno anterior {datos_colab[0][2]}): ")
                    nuevo_tip_dcmto = input(
                        f"Ingrese el nuevo tipo de documento (dni/carnet) (anterior {datos_colab[0][3]}): ")
                    nuevo_nro_dcmto = input(f"Ingrese el nuevo # de documento (anterior {datos_colab[0][4]}): ")
                    nuevo_correo = input(f"Ingrese el nuevo correo (anterior {datos_colab[0][5]}): ")
                    nuevo_contrasena = input(f"Ingrese nueva contrasenia (anterior {datos_colab[0][6]}): ")
                    nueva_area = input(f"Ingrese nueva area (anterior {datos_colab[0][7]}): ")
                    editar_colaborador(id_colab, nuevo_nombre, nuevo_ap_pat, nuevo_ap_mat, nuevo_tip_dcmto,
                                       nuevo_nro_dcmto,nueva_area ,nuevo_correo, nuevo_contrasena)

            elif opcion == 3:
                ver_estudiantes()
            elif opcion == 4:
                pass
            elif opcion == 5:
                ver_examenes()


    # -------------------------------------------------------------------------

    def asignar_profesores_a_ciclos(self):
        pass

    # --------------------------------------------------------------------------

    def gestionar_sedes(self):

        while(True):
            print("1. Crear sede")
            print("2. Editar sede")
            print("3. Ver sedes")
            print("0. Volver")

            opcion = int(input("Digite una opcion: "))
            if opcion == 1:
                print("Opcion 1: Crear sede")
                nombre=input("Coloque el nombre de la sede: ")
                distrito=input("Coloque el distrito: ")
                crear_sede(nombre,distrito)
            elif opcion == 2:
                print("Opcion 2: Editar sede")
                ver_sedes()
                id_sede = int(input("Coloque el id de la sede: "))
                valor_logico, sede = buscar_sede(id_sede)
                int(valor_logico)
                if valor_logico == 1:
                    nombre = input(f"Ingrese el nuevo nombre (Nombre anterior: {sede[1]}): ")
                    distrito = input(f"Coloque el distrito (Distrito anterior {sede[2]}): ")
                    actualizar_sede(id_sede,nombre,distrito)
                elif valor_logico == 0:
                    break
            elif opcion == 3:
                print("Opcion 3: Ver sedes")
                ver_sedes()
            elif opcion == 0:
                print("Volver al menu")
                break


    def gestionar_cursos_y_especialidades(self):

        while(True):

            print("1. Crear curso")
            print("2. Editar curso")
            print("3. Ver cursos")
            print("4. Crear especialidad")
            print("5. Editar especialidad")
            print("6. Ver especialidades")
            print("0. Volver al menu")

            opcion = int(input("Digite una opcion: "))
            if opcion == 1:
                print("Opcion 1: Crear curso")
                nombre = input("Coloque el nombre del curso: ")
                crear_curso(nombre)
            elif opcion == 2:
                print("Opcion 2: Editar curso")
                ver_cursos()
                id_curso = int(input("Coloque el id del curso: "))
                valor_logico, curso = buscar_curso(id_curso)
                int(valor_logico)
                if valor_logico == 1:
                    nombre = input(f"Ingrese el nuevo nombre (Nombre anterior: {curso[1]}): ")
                    actualizar_curso(id_curso, nombre)
                elif valor_logico == 0:
                    print("no se encuentra ese dato")
                    break
            elif opcion == 3:
                print("Opcion 3: Ver cursos")
                ver_cursos()
            elif opcion == 4:
                print("Opcion 4: Crear especialidad")
                nombre = input("Coloque el nombre de la especialidad: ")
                crear_especialidad(nombre)
            elif opcion == 5:
                print("Opcion 5: Editar especialidad")
                ver_especialidades()
                id_especialidad = int(input("Coloque el id de la especialidad: "))
                valor_logico, especialidad = buscar_especialidad(id_especialidad)
                int(valor_logico)
                if valor_logico == 1:
                    nombre = input(f"Ingrese el nuevo nombre (Nombre anterior: {especialidad[1]}): ")
                    actualizar_especialidad(id_especialidad, nombre)
                elif valor_logico == 0:
                    break
            elif opcion == 6:
                print("Opcion 6: Ver especialidades")
                ver_especialidades()
            elif opcion == 0:
                print("Volviendo al menu")
                break
            else:
                print("Opcion no existe")

