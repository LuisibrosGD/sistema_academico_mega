> Tienes que copiar todo y listo
```sql
  -- Insertar cursos
INSERT INTO CURSOS (nombre_curso) VALUES
('Razonamiento Verbal'),
('Razonamiento Matemático'),
('Aritmética'),
('Geometría'),
('Álgebra'),
('Trigonometría'),
('Lenguaje'),
('Literatura'),
('Psicologia'),
('Educacion Cívica'),
('Historia del Peru'),
('Historia Universal'),
('Economía'),
('Geografía'),
('Filosofía'),
('Física'),
('Química'),
('Biología');

-- Insertar especialidades (asumiendo que son iguales a los cursos)
INSERT INTO ESPECIALIDADES (nombre_especialidad) VALUES
('Razonamiento Verbal'),
('Razonamiento Matemático'),
('Aritmética'),
('Geometría'),
('Álgebra'),
('Trigonometría'),
('Lenguaje'),
('Literatura'),
('Psicologia'),
('Educacion Cívica'),
('Historia del Peru'),
('Historia Universal'),
('Economía'),
('Geografía'),
('Filosofía'),
('Física'),
('Química'),
('Biología');

-- Insertar sedes
INSERT INTO SEDES (nombre, distrito) VALUES
('Sede Central', 'Lima'),
('Sede Norte', 'Los Olivos'),
('Sede Sur', 'Chorrillos');

-- Insertar usuarios (12 en total)
INSERT INTO USUARIOS (nombre_usuario, correo, contrasenia, estado, rol) VALUES
-- Administradores (2)
('admin1', 'admin1@academia.com', 'admin1pass', 1, 'administrador'),
('admin2', 'admin2@academia.com', 'admin2pass', 1, 'administrador'),
-- Profesores (3)
('profe_maria', 'maria@academia.com', 'mariapass', 1, 'profesor'),
('profe_carlos', 'carlos@academia.com', 'carlospass', 1, 'profesor'),
('profe_laura', 'laura@academia.com', 'laurapass', 1, 'profesor'),
-- Estudiantes (7)
('alumno_ana', 'ana@academia.com', 'anapass', 1, 'estudiante'),
('alumno_luis', 'luis@academia.com', 'luispass', 1, 'estudiante'),
('alumno_sofia', 'sofia@academia.com', 'sofiapass', 1, 'estudiante'),
('alumno_juan', 'juan@academia.com', 'juanpass', 1, 'estudiante'),
('alumno_maria', 'maria_est@academia.com', 'mariapass', 1, 'estudiante'),
('alumno_pedro', 'pedro@academia.com', 'pedropass', 1, 'estudiante'),
('alumno_lucia', 'lucia@academia.com', 'luciapass', 1, 'estudiante');

-- Detalles de administradores
INSERT INTO ADMINISTRADORES (id_usuario, nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, nacionalidad) VALUES
(1, 'Juan', 'Perez', 'Gomez', 'dni', '12345678', 'Peruano'),
(2, 'Marta', 'Rodriguez', 'Vega', 'dni', '87654321', 'Peruana');

-- Detalles de profesores
INSERT INTO PROFESORES (id_usuario, nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, nacionalidad) VALUES
(3, 'Maria', 'Lopez', 'Diaz', 'dni', '11223344', 'Peruana'),
(4, 'Carlos', 'Sanchez', 'Mendoza', 'pasaporte', 'PA123456', 'Argentino'),
(5, 'Laura', 'Garcia', 'Ruiz', 'dni', '44332211', 'Mexicana');

-- Detalles de estudiantes
INSERT INTO ESTUDIANTES (id_usuario, nombre, ap_paterno, ap_materno, tipo_documento, nro_documento, area_academica, id_sede) VALUES
(6, 'Ana', 'Gomez', 'Perez', 'dni', '55667788', 'a', 1),
(7, 'Luis', 'Martinez', 'Flores', 'dni', '99887766', 'b', 2),
(8, 'Sofia', 'Diaz', 'Vega', 'dni', '33445566', 'c', 3),
(9, 'Juan', 'Ramirez', 'Lopez', 'pasaporte', 'PA112233', 'd', 1),
(10, 'Maria', 'Torres', 'Santos', 'dni', '22334455', 'e', 2),
(11, 'Pedro', 'Gonzalez', 'Rios', 'dni', '66778899', 'a', 3),
(12, 'Lucia', 'Fernandez', 'Ortega', 'dni', '12341234', 'b', 1);

-- Insertar ciclos programados
INSERT INTO CICLOS_PROGRAMADOS (nombre_ciclo, modalidad, costo, fecha_inicio, fecha_fin) VALUES
('Ciclo 2025-I', 'Presencial', 600.00, '2025-03-10', '2025-07-20'),
('Ciclo 2025-II', 'Virtual', 550.00, '2025-08-05', '2025-12-15');

-- Asignar especialidades a profesores
INSERT INTO PROFESORES_has_ESPECIALIDADES (id_especialidad, id_usuario) VALUES
-- Profe Maria (Matemáticas)
(2, 3), (3, 3), (4, 3), 
-- Profe Carlos (Ciencias Sociales)
(10, 4), (11, 4), (12, 4),
-- Profe Laura (Ciencias Naturales)
(16, 5), (17, 5), (18, 5);

-- Inscripciones de estudiantes
INSERT INTO INSCRIPCIONES (fecha_inscripcion, id_ciclo, ESTUDIANTES_id_usuario) VALUES
('2025-03-01 09:00:00', 1, 6),
('2025-03-01 10:00:00', 1, 7),
('2025-03-02 11:00:00', 1, 8),
('2025-08-01 09:30:00', 2, 9),
('2025-08-02 10:15:00', 2, 10),
('2025-08-03 11:45:00', 2, 11),
('2025-08-04 12:00:00', 2, 12);

-- Pagos de inscripciones
INSERT INTO PAGOS (id_inscripcion, monto, fecha_pago) VALUES
(1, 600.00, '2025-03-01 09:05:00'),
(2, 600.00, '2025-03-01 10:05:00'),
(3, 600.00, '2025-03-02 11:05:00'),
(4, 550.00, '2025-08-01 09:35:00'),
(5, 550.00, '2025-08-02 10:20:00'),
(6, 550.00, '2025-08-03 11:50:00'),
(7, 550.00, '2025-08-04 12:05:00');

-- Asignar cursos a ciclos (ejemplo: Ciclo 1)
INSERT INTO CICLOS_CURSOS (hora_inicio, hora_fin, id_ciclo, id_curso) VALUES
('08:00:00', '10:00:00', 1, 1),   -- Razonamiento Verbal
('10:30:00', '12:30:00', 1, 2),   -- Razonamiento Matemático
('14:00:00', '16:00:00', 1, 16);  -- Física

-- Crear grupos con profesores
INSERT INTO GRUPOS_POR_CICLO (nombre_grupo, id_usuario, id_cc) VALUES
('Grupo RV-AM', 3, 1),   -- Profe Maria enseña Razonamiento Verbal
('Grupo RM-PM', 3, 2),   -- Profe Maria enseña Razonamiento Matemático
('Grupo Física', 5, 3);   -- Profe Laura enseña Física

-- Registrar asistencias de profesores
INSERT INTO ASISTENCIAS (fecha, hora, estado, id_usuario) VALUES
('2025-05-10', '08:00:00', 'presente', 3),
('2025-05-10', '10:30:00', 'presente', 3),
('2025-05-11', '14:00:00', 'tarde', 5);

-- Exámenes de estudiantes
INSERT INTO EXAMENES (id_usuario, fecha_realizacion, puntaje) VALUES
(6, '2025-07-15', 85.5),
(7, '2025-07-15', 78.0),
(8, '2025-07-16', 92.3);

INSERT INTO SEDES_CICLOS (id_sede, id_ciclo) VALUES
(1,1),
(1,2),
(2,1),
(2,2),
(3,1);
```
