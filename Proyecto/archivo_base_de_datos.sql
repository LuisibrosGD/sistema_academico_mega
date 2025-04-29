-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS USUARIOS (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    correo VARCHAR(255) NOT NULL,
    contrasenia VARCHAR(255) NOT NULL, -- Contraseña cifrada
    estado BOOLEAN
);

-- Crear tabla de administradores
CREATE TABLE IF NOT EXISTS ADMINISTRADORES (
    id_administrador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    dni INT NOT NULL,
    id_usuario INT, -- Clave foránea
    FOREIGN KEY (id_usuario) REFERENCES USUARIOS(id_usuario)
);

-- Crear tabla de estudiantes
CREATE TABLE IF NOT EXISTS ESTUDIANTES (
    id_estudiantes INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    dni INT NOT NULL,
    id_usuario INT, -- Clave foránea
    FOREIGN KEY (id_usuario) REFERENCES USUARIOS(id_usuario)
);

-- Crear tabla de sedes
CREATE TABLE IF NOT EXISTS SEDES (
    id_sede INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    distrito VARCHAR(255) NOT NULL
);

-- Crear tabla de profesores (ahora debería funcionar)
CREATE TABLE IF NOT EXISTS PROFESORES (
    id_profesor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellido VARCHAR(255) NOT NULL,
    dni INT NOT NULL,
    id_usuario INT, -- Clave foránea
    id_sede INT, -- Clave foránea
    FOREIGN KEY (id_usuario) REFERENCES USUARIOS(id_usuario),
    FOREIGN KEY (id_sede) REFERENCES SEDES(id_sede)
);


-- Crear tabla de ciclos
CREATE TABLE IF NOT EXISTS CICLOS (
    id_ciclo INT AUTO_INCREMENT PRIMARY KEY,
    nombreciclo VARCHAR(255) NOT NULL,
    modalidad VARCHAR(255) NOT NULL,
    costo INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    id_sede INT, -- Clave foránea
    FOREIGN KEY (id_sede) REFERENCES SEDES(id_sede)
);

-- Crear tabla de cursos
CREATE TABLE IF NOT EXISTS CURSOS (
    id_curso INT AUTO_INCREMENT PRIMARY KEY,
    nombre_curso VARCHAR(255) NOT NULL,
    id_profesor INT, -- Clave foránea
    id_sede INT, -- Clave foránea
    FOREIGN KEY (id_profesor) REFERENCES PROFESORES(id_profesor),
    FOREIGN KEY (id_sede) REFERENCES SEDES(id_sede)
);

-- Crear tabla de asistencias
CREATE TABLE IF NOT EXISTS ASISTENCIAS (
    id_asistencia INT AUTO_INCREMENT PRIMARY KEY,
    id_profesor INT, -- Clave foránea
    fecha DATE NOT NULL,
    presente BOOLEAN, -- SI/NO
    FOREIGN KEY (id_profesor) REFERENCES PROFESORES(id_profesor)
);

-- Crear tabla de inscripciones
CREATE TABLE IF NOT EXISTS INSCRIPCIONES (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT, -- Clave foránea
    id_ciclo INT, -- Clave foránea
    FOREIGN KEY (id_estudiante) REFERENCES ESTUDIANTES(id_estudiantes),
    FOREIGN KEY (id_ciclo) REFERENCES CICLOS(id_ciclo)
);

-- Crear tabla de pagos
CREATE TABLE IF NOT EXISTS PAGOS (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_inscripcion INT, -- Clave foránea
    monto INT NOT NULL,
    fecha_pago DATE NOT NULL,
    FOREIGN KEY (id_inscripcion) REFERENCES INSCRIPCIONES(id_inscripcion)
);

