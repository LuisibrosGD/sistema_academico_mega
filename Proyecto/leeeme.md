El codigo de la base de datos es lo que entregamos para el primer entregable, osea sin la retroalimentacion y correcciones solicitadas.

Hice la base de datos en mysql workbench desde cero y ahora parece que si funciona

LLENADO DE DATOS:
1. Tablas Independientes (sin claves foráneas)
Comienza con las tablas que no dependen de otras:

```sql
  -- Insertar datos en CURSOS
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
```

```sql
-- Insertar datos en SEDES
INSERT INTO SEDES (nombre, distrito) VALUES 
('Sede Central', 'Lima'),
('Sede Norte', 'Los Olivos'),
('Sede Sur', 'Chorrillos'),
('Sede Este', 'Ate'),
('Sede Oeste', 'Breña');
```

```sql
-- Insertar datos en USUARIOS (para todos los roles)
INSERT INTO USUARIOS (correo, contrasenia, estado, rol) VALUES 
-- Administradores
('admin1@email.com', 'adminpass1', 1, 'administrador'),
('admin2@email.com', 'adminpass2', 1, 'administrador'),
-- Profesores
('prof1@email.com', 'profpass1', 1, 'profesor'),
('prof2@email.com', 'profpass2', 1, 'profesor'),
('prof3@email.com', 'profpass3', 1, 'profesor'),
-- Estudiantes
('est1@email.com', 'estpass1', 1, 'estudiante'),
('est2@email.com', 'estpass2', 1, 'estudiante'),
('est3@email.com', 'estpass3', 1, 'estudiante'),
('est4@email.com', 'estpass4', 1, 'estudiante');
```

```sql
-- Insertar datos en CICLOS
INSERT INTO CICLOS (nombre_ciclo, modalidad, costo, fecha_inicio, fecha_fin) VALUES 
('Ciclo 2025-1', 'Presencial', 1200.00, '2025-03-01', '2025-07-15'),
('Ciclo 2025-2', 'Virtual', 1000.00, '2025-08-01', '2025-12-15'),
('Ciclo Verano 2025', 'Intensivo', 800.00, '2026-01-05', '2026-02-20');
```
2. Tablas que dependen de USUARIOS

```sql
-- Insertar datos en ADMINISTRADORES
INSERT INTO ADMINISTRADORES (nombre, apellido, dni, USUARIOS_id_usuario) VALUES 
('Juan', 'Pérez', '12345678', 1),
('María', 'Gómez', '87654321', 2);
```

```sql
-- Insertar datos en PROFESORES
INSERT INTO PROFESORES (id_profesores, nombre, apellido, dni, USUARIOS_id_usuario, SEDES_id_sede) VALUES 
(1, 'Carlos', 'Ruiz', '11112222', 3, 1),
(2, 'Ana', 'Torres', '22223333', 4, 2),
(3, 'Luis', 'Mendoza', '33334444', 5, 3);
```

```sql
-- Insertar datos en ESTUDIANTES
INSERT INTO ESTUDIANTES (nombre, apellido, dni, USUARIOS_id_usuario) VALUES 
('Pedro', 'García', '44445555', 6),
('Lucía', 'Fernández', '55556666', 7),
('Miguel', 'Díaz', '66667777', 8),
('Sofía', 'Vargas', '77778888', 9);
```
3. Tablas de relación muchos-a-muchos
```sql
-- Insertar datos en CURSOS_has_PROFESORES (asignar cursos a profesores)
INSERT INTO CURSOS_has_PROFESORES (CURSOS_id_curso, PROFESORES_id_profesores) VALUES 
(1, 1), -- Matemáticas con Carlos
(2, 1), -- Comunicación con Carlos
(3, 2), -- Ciencias con Ana
(4, 3), -- Historia con Luis
(5, 3); -- Inglés con Luis
```

```sql
-- Insertar datos en SEDES_has_CICLOS (asignar ciclos a sedes)
INSERT INTO SEDES_has_CICLOS (SEDES_id_sede, CICLOS_id_ciclo) VALUES 
(1, 1), -- Sede Central con Ciclo 2025-1
(1, 2), -- Sede Central con Ciclo 2025-2
(2, 1), -- Sede Norte con Ciclo 2025-1
(3, 3), -- Sede Sur con Ciclo Verano 2025
(4, 2); -- Sede Este con Ciclo 2025-2
```
4. Tablas que dependen de otras relaciones
```sql
-- Insertar datos en INSCRIPCIONES (estudiantes en ciclos)
INSERT INTO INSCRIPCIONES (ESTUDIANTES_id_estudiantes, CICLOS_id_ciclo) VALUES 
(1, 1), -- Pedro en Ciclo 2025-1
(2, 1), -- Lucía en Ciclo 2025-1
(3, 2), -- Miguel en Ciclo 2025-2
(4, 3); -- Sofía en Ciclo Verano 2025
```

```sql
-- Insertar datos en PAGOS (pagos de inscripciones)
INSERT INTO PAGOS (monto, fecha_pago, INSCRIPCIONES_id_inscripciones) VALUES 
(1200.00, '2025-02-15', 1), -- Pago completo de Pedro
(600.00, '2025-02-20', 2),  -- Primer pago de Lucía
(600.00, '2025-03-10', 2),  -- Segundo pago de Lucía
(1000.00, '2025-07-25', 3), -- Pago completo de Miguel
(400.00, '2025-12-20', 4),  -- Primer pago de Sofía
(400.00, '2026-01-10', 4);  -- Segundo pago de Sofía
```

```sql
-- Insertar datos en ASISTENCIAS (asistencias de profesores)
INSERT INTO ASISTENCIAS (fecha, presente, PROFESORES_id_profesores) VALUES 
('2025-05-01', 1, 1), -- Carlos presente
('2025-05-01', 0, 2), -- Ana ausente
('2025-05-02', 1, 1), -- Carlos presente
('2025-05-02', 1, 3), -- Luis presente
('2025-05-03', 1, 2); -- Ana presente
```

