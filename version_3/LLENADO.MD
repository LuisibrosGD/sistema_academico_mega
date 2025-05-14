-- Insertar usuarios (7 estudiantes, 5 profesores, 3 administradores)
INSERT INTO `usuarios` (`nombre_usuario`, `correo`, `contrasenia`, `estado`, `rol`) VALUES
-- Estudiantes
('jperez', 'juan.perez@email.com', 'estudiante123', 1, 'estudiante'),
('mgomez', 'maria.gomez@email.com', 'estudiante123', 1, 'estudiante'),
('crodrig', 'carlos.rodriguez@email.com', 'estudiante123', 1, 'estudiante'),
('lfernand', 'laura.fernandez@email.com', 'estudiante123', 1, 'estudiante'),
('amartin', 'ana.martinez@email.com', 'estudiante123', 1, 'estudiante'),
('psanchez', 'pedro.sanchez@email.com', 'estudiante123', 1, 'estudiante'),
('dgonzalez', 'diego.gonzalez@email.com', 'estudiante123', 1, 'estudiante'),

-- Profesores
('proflopez', 'prof.lopez@email.com', 'profesor123', 1, 'profesor'),
('proframirez', 'prof.ramirez@email.com', 'profesor123', 1, 'profesor'),
('profgarcia', 'prof.garcia@email.com', 'profesor123', 1, 'profesor'),
('profherrera', 'prof.herrera@email.com', 'profesor123', 1, 'profesor'),
('profcastro', 'prof.castro@email.com', 'profesor123', 1, 'profesor'),

-- Administradores
('admin1', 'admin.principal@email.com', 'admin123', 1, 'administrador'),
('admin2', 'admin.secundario@email.com', 'admin123', 1, 'administrador'),
('admin3', 'admin.tercero@email.com', 'admin123', 1, 'administrador');

-- Insertar estudiantes (7 estudiantes)
INSERT INTO `estudiantes` (`id_usuario`, `nombre`, `ap_paterno`, `ap_materno`, `tipo_documento`, `nro_documento`, `area_academica`) VALUES
(1, 'Juan', 'Pérez', 'Gómez', 'dni', '71234567', 'a'),
(2, 'María', 'Gómez', 'López', 'dni', '71234568', 'b'),
(3, 'Carlos', 'Rodríguez', 'Martínez', 'dni', '71234569', 'c'),
(4, 'Laura', 'Fernández', 'Díaz', 'dni', '71234570', 'd'),
(5, 'Ana', 'Martínez', 'Ruiz', 'dni', '71234571', 'e'),
(6, 'Pedro', 'Sánchez', 'Hernández', 'dni', '71234572', 'a'),
(7, 'Diego', 'González', 'Moreno', 'dni', '71234573', 'b');

-- Insertar profesores (5 profesores)
INSERT INTO `profesores` (`id_usuario`, `nombre`, `ap_paterno`, `ap_materno`, `tipo_documento`, `nro_documento`, `nacionalidad`) VALUES
(8, 'Roberto', 'López', 'Vargas', 'dni', '51234567', 'peruano'),
(9, 'Miguel', 'Ramírez', 'Silva', 'dni', '51234568', 'argentino'),
(10, 'Jorge', 'García', 'Mendoza', 'dni', '51234569', 'mexicano'),
(11, 'Luis', 'Herrera', 'Castro', 'dni', '51234570', 'chileno'),
(12, 'Fernando', 'Castro', 'Rojas', 'dni', '51234571', 'colombiano');

-- Insertar administradores (3 administradores)
INSERT INTO `administradores` (`id_usuario`, `nombre`, `ap_paterno`, `ap_materno`, `tipo_documento`, `nro_documento`, `nacionalidad`) VALUES
(13, 'Alberto', 'Suárez', 'Pérez', 'dni', '31234567', 'peruano'),
(14, 'Ricardo', 'Mendoza', 'Gómez', 'dni', '31234568', 'peruano'),
(15, 'Enrique', 'Torres', 'López', 'dni', '31234569', 'peruano');

-- Insertar sedes (3 sedes)
INSERT INTO `sedes` (`nombre`, `distrito`) VALUES
('Mega Academia Lima Centro', 'Lima'),
('Mega Academia San Isidro', 'San Isidro'),
('Mega Academia Miraflores', 'Miraflores');

-- SEPARADOR

-- Insertar las especialidades especificadas (iguales a los cursos)
INSERT INTO `especialidades` (`nombre_especialidad`) VALUES
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

-- Insertar los cursos especificados
INSERT INTO `cursos` (`nombre_curso`) VALUES
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

-- Insertar ciclos programados (2 ciclos)
INSERT INTO `ciclos_programados` (`nombre_ciclo`, `modalidad`, `costo`, `fecha_inicio`, `fecha_fin`) VALUES
('Ciclo 2025-I', 'Presencial', 1200.00, '2025-03-15', '2025-07-20'),
('Ciclo 2025-II', 'Virtual', 1000.00, '2025-08-10', '2025-12-15');

-- Asignar sedes a ciclos
INSERT INTO `sedes_ciclos` (`id_sede`, `id_ciclo`) VALUES
(1, 1), (2, 1), (3, 1),  -- Todas las sedes para ciclo 2025-I
(1, 2), (3, 2);           -- Solo Lima Centro y Miraflores para ciclo 2025-II (virtual)

-- Reasignar especialidades a profesores según los nuevos cursos
INSERT INTO `profesores_has_especialidades` (`id_especialidad`, `id_usuario`) VALUES
-- Profesor López (Matemáticas y Ciencias)
(2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (16, 8), (17, 8), (18, 8),

-- Profesor Ramírez (Humanidades)
(1, 9), (7, 9), (8, 9), (10, 9), (11, 9), (12, 9), (14, 9), (15, 9),

-- Profesor García (Razonamiento y Lenguaje)
(1, 10), (2, 10), (7, 10), (8, 10), (9, 10),

-- Profesor Herrera (Ciencias Sociales)
(10, 11), (11, 11), (12, 11), (13, 11), (14, 11), (15, 11),

-- Profesor Castro (Ciencias Naturales)
(16, 12), (17, 12), (18, 12);

-- Crear cursos por ciclo
INSERT INTO `ciclos_cursos` (`hora_inicio`, `hora_fin`, `id_ciclo`, `id_curso`) VALUES
-- Ciclo 2025-I (Presencial)
('08:00:00', '10:00:00', 1, 2),  -- Razonamiento Matemático
('10:00:00', '12:00:00', 1, 5),  -- Álgebra
('14:00:00', '16:00:00', 1, 16), -- Física
('16:00:00', '18:00:00', 1, 1),  -- Razonamiento Verbal

-- Ciclo 2025-II (Virtual)
('09:00:00', '11:00:00', 2, 3),  -- Aritmética
('11:00:00', '13:00:00', 2, 7),  -- Lenguaje
('15:00:00', '17:00:00', 2, 11); -- Historia del Perú

-- Crear grupos por ciclo
INSERT INTO `grupos_por_ciclo` (`nombre_grupo`, `id_usuario`, `id_cc`) VALUES
('Grupo RV-2025', 9, 4),       -- Prof. Ramírez enseña Razonamiento Verbal
('Grupo RM-2025', 8, 1),       -- Prof. López enseña Razonamiento Matemático
('Grupo Física-2025', 8, 3);   -- Prof. López enseña Física

-- Inscripciones de estudiantes
INSERT INTO `inscripciones` (`fecha_inscripcion`, `id_ciclo`, `ESTUDIANTES_id_usuario`) VALUES
-- Ciclo 2025-I
('2025-02-10 10:00:00', 1, 1),
('2025-02-11 11:00:00', 1, 2),
('2025-02-12 09:00:00', 1, 3),
('2025-02-13 14:00:00', 1, 4),

-- Ciclo 2025-II
('2025-07-05 10:00:00', 2, 5),
('2025-07-06 11:00:00', 2, 6),
('2025-07-07 09:00:00', 2, 7);

-- Registrar pagos
INSERT INTO `pagos` (`id_inscripcion`, `monto`, `fecha_pago`) VALUES
(1, 1200.00, '2025-02-10 10:30:00'),
(2, 1200.00, '2025-02-11 11:30:00'),
(3, 1200.00, '2025-02-12 09:30:00'),
(4, 1200.00, '2025-02-13 14:30:00'),
(5, 1000.00, '2025-07-05 10:30:00'),
(6, 1000.00, '2025-07-06 11:30:00'),
(7, 1000.00, '2025-07-07 09:30:00');

-- Registrar asistencias de profesores
INSERT INTO `asistencias` (`fecha`, `hora`, `estado`, `id_usuario`) VALUES
-- Profesor López
('2025-03-16', '07:50:00', 'presente', 8),
('2025-03-17', '07:55:00', 'presente', 8),
('2025-03-18', '08:10:00', 'tarde', 8),
('2025-03-19', '07:45:00', 'presente', 8),

-- Profesor García
('2025-03-16', '13:50:00', 'presente', 10),
('2025-03-17', '13:55:00', 'presente', 10),
('2025-03-18', '14:15:00', 'tarde', 10);

-- Registrar exámenes de estudiantes
INSERT INTO `examenes` (`id_usuario`, `fecha_realizacion`, `puntaje`) VALUES
(1, '2025-04-15', 85.50),
(1, '2025-05-20', 78.00),
(2, '2025-04-15', 92.00),
(3, '2025-04-15', 65.50),
(4, '2025-04-15', 88.00),
(5, '2025-09-10', 76.50),
(6, '2025-09-10', 81.00);
