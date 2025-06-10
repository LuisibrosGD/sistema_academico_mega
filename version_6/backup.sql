-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: academia_mega
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `administradores`
--

DROP TABLE IF EXISTS `administradores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `administradores` (
  `id_administrador` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `ap_paterno` varchar(45) NOT NULL,
  `ap_materno` varchar(45) NOT NULL,
  `tipo_documento` enum('dni','pasaporte') NOT NULL,
  `nro_documento` varchar(20) NOT NULL,
  `id_usuario` int NOT NULL,
  PRIMARY KEY (`id_administrador`),
  KEY `fk_ADMINISTRADORES_USUARIOS1_idx` (`id_usuario`),
  CONSTRAINT `fk_ADMINISTRADORES_USUARIOS1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `administradores`
--

LOCK TABLES `administradores` WRITE;
/*!40000 ALTER TABLE `administradores` DISABLE KEYS */;
INSERT INTO `administradores` VALUES (1,'Luis','Bizarro','Ortiz','dni','12345678',1),(2,'Alex','Soto','Hidalgo','dni','11223344',2),(3,'LuisS','Bizarro','Ortiz','dni','12312333',7);
/*!40000 ALTER TABLE `administradores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `asistencias`
--

DROP TABLE IF EXISTS `asistencias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `asistencias` (
  `id_asistencia` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('presente','tarde','ausente') NOT NULL,
  `id_profesor` int NOT NULL,
  PRIMARY KEY (`id_asistencia`),
  KEY `fk_ASISTENCIAS_PROFESORES1_idx` (`id_profesor`),
  CONSTRAINT `fk_ASISTENCIAS_PROFESORES1` FOREIGN KEY (`id_profesor`) REFERENCES `profesores` (`id_profesor`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `asistencias`
--

LOCK TABLES `asistencias` WRITE;
/*!40000 ALTER TABLE `asistencias` DISABLE KEYS */;
INSERT INTO `asistencias` VALUES (1,'2025-06-08 23:19:59','presente',1),(2,'2025-06-08 23:36:58','presente',1);
/*!40000 ALTER TABLE `asistencias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ciclos_cursos`
--

DROP TABLE IF EXISTS `ciclos_cursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ciclos_cursos` (
  `id_cc` int NOT NULL AUTO_INCREMENT,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `dia` varchar(25) NOT NULL,
  `id_ciclo` int NOT NULL,
  `id_curso` int NOT NULL,
  `id_profesor` int NOT NULL,
  PRIMARY KEY (`id_cc`),
  KEY `fk_SEDES_CICLOS_PROFESORES_CURSOS_CURSOS1_idx` (`id_curso`),
  KEY `fk_CICLOS_CURSOS_CICLOS_PROGRAMADOS1_idx` (`id_ciclo`),
  KEY `fk_profesores_cic_curs_idx` (`id_profesor`),
  CONSTRAINT `fk_CICLOS_CURSOS_CICLOS_PROGRAMADOS1` FOREIGN KEY (`id_ciclo`) REFERENCES `ciclos_programados` (`id_ciclo`),
  CONSTRAINT `fk_profesores_ciclos_cursos` FOREIGN KEY (`id_profesor`) REFERENCES `profesores` (`id_profesor`),
  CONSTRAINT `fk_SEDES_CICLOS_PROFESORES_CURSOS_CURSOS1` FOREIGN KEY (`id_curso`) REFERENCES `cursos` (`id_curso`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ciclos_cursos`
--

LOCK TABLES `ciclos_cursos` WRITE;
/*!40000 ALTER TABLE `ciclos_cursos` DISABLE KEYS */;
INSERT INTO `ciclos_cursos` VALUES (1,'08:00:00','10:00:00','lunes',9,1,1);
/*!40000 ALTER TABLE `ciclos_cursos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ciclos_programados`
--

DROP TABLE IF EXISTS `ciclos_programados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ciclos_programados` (
  `id_ciclo` int NOT NULL AUTO_INCREMENT,
  `nombre_ciclo` varchar(100) NOT NULL,
  `modalidad` varchar(45) NOT NULL,
  `costo` decimal(10,2) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `estado` enum('en curso','finalizado') NOT NULL DEFAULT 'en curso',
  PRIMARY KEY (`id_ciclo`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ciclos_programados`
--

LOCK TABLES `ciclos_programados` WRITE;
/*!40000 ALTER TABLE `ciclos_programados` DISABLE KEYS */;
INSERT INTO `ciclos_programados` VALUES (1,'Ciclo Verano 2024','Presencial',750.00,'2024-01-10','2024-03-30','en curso'),(2,'Ciclo Regular 2024-I','Virtual',900.00,'2024-04-01','2024-07-15','en curso'),(3,'Ciclo Intensivo 2024','Presencial',1100.00,'2024-05-05','2024-06-30','en curso'),(4,'Ciclo Invierno 2024','Virtual',850.00,'2024-07-20','2024-09-30','en curso'),(5,'Ciclo Regular 2024-II','Presencial',950.00,'2024-08-01','2024-12-15','en curso'),(6,'Ciclo Verano 2025','Virtual',780.00,'2025-01-08','2025-03-28','en curso'),(7,'Ciclo Regular 2025-I','Presencial',1000.00,'2025-04-01','2025-07-20','en curso'),(8,'Ciclo Intensivo 2025','Virtual',1200.00,'2025-05-10','2025-07-05','en curso'),(9,'Ciclo de Repaso','Virtual',600.00,'2025-06-01','2025-07-10','en curso'),(10,'Ciclo de Actualización','Presencial',700.00,'2025-06-03','2025-08-15','en curso'),(11,'Ciclo Invierno 2025','virtual',300.00,'2025-07-01','2025-10-01','en curso');
/*!40000 ALTER TABLE `ciclos_programados` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `colaboradores`
--

DROP TABLE IF EXISTS `colaboradores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `colaboradores` (
  `id_colaborador` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `ap_paterno` varchar(45) NOT NULL,
  `ap_materno` varchar(45) NOT NULL,
  `tipo_documento` enum('dni','pasaporte') NOT NULL,
  `nro_documento` varchar(20) NOT NULL,
  `id_usuario` int NOT NULL,
  PRIMARY KEY (`id_colaborador`),
  KEY `id_usuario_idx` (`id_usuario`),
  CONSTRAINT `id_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `colaboradores`
--

LOCK TABLES `colaboradores` WRITE;
/*!40000 ALTER TABLE `colaboradores` DISABLE KEYS */;
INSERT INTO `colaboradores` VALUES (1,'Anderson','Tataje','Rodriguez','dni','21212121',3),(2,'Luis Junior','Bizarro','Ortiz','dni','14141312',8);
/*!40000 ALTER TABLE `colaboradores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cursos`
--

DROP TABLE IF EXISTS `cursos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cursos` (
  `id_curso` int NOT NULL AUTO_INCREMENT,
  `nombre_curso` varchar(100) NOT NULL,
  PRIMARY KEY (`id_curso`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cursos`
--

LOCK TABLES `cursos` WRITE;
/*!40000 ALTER TABLE `cursos` DISABLE KEYS */;
INSERT INTO `cursos` VALUES (1,'Razonamiento Matemático'),(2,'Razonamiento Verbal'),(3,'Álgebra'),(4,'Aritmética'),(5,'Geometría'),(6,'Trigonometría'),(7,'Física'),(8,'Quimica inorganica'),(9,'Biología'),(10,'Historia del Perú'),(11,'Historia Universal'),(12,'Geografía'),(13,'Economía'),(14,'Lenguaje'),(15,'Literatura'),(16,'Cívica'),(17,'Psicología'),(18,'Filosofía'),(19,'Anatomia');
/*!40000 ALTER TABLE `cursos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `especialidades`
--

DROP TABLE IF EXISTS `especialidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `especialidades` (
  `id_especialidad` int NOT NULL AUTO_INCREMENT,
  `nombre_especialidad` varchar(45) NOT NULL,
  PRIMARY KEY (`id_especialidad`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `especialidades`
--

LOCK TABLES `especialidades` WRITE;
/*!40000 ALTER TABLE `especialidades` DISABLE KEYS */;
INSERT INTO `especialidades` VALUES (1,'Ciencias de la Salud'),(2,'Ingeniería'),(3,'Matemática'),(4,'Ciencias Económicas'),(5,'Humanidades'),(6,'Ciencias Sociales'),(7,'Educación'),(8,'Derecho'),(9,'Psicología'),(10,'Arquitectura'),(11,'Administración'),(12,'Comunicacion empresarial'),(13,'Computacion');
/*!40000 ALTER TABLE `especialidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `estudiantes`
--

DROP TABLE IF EXISTS `estudiantes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `estudiantes` (
  `id_estudiante` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `ap_paterno` varchar(45) NOT NULL,
  `ap_materno` varchar(45) NOT NULL,
  `tipo_documento` enum('dni','pasaporte') NOT NULL,
  `nro_documento` varchar(20) NOT NULL,
  `area_academica` enum('a','b','c','d','e') NOT NULL,
  `id_usuario` int NOT NULL,
  PRIMARY KEY (`id_estudiante`),
  KEY `fk_ESTUDIANTES_USUARIOS1_idx` (`id_usuario`),
  CONSTRAINT `fk_ESTUDIANTES_USUARIOS1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `estudiantes`
--

LOCK TABLES `estudiantes` WRITE;
/*!40000 ALTER TABLE `estudiantes` DISABLE KEYS */;
INSERT INTO `estudiantes` VALUES (1,'Fernando','Saire','Tello','dni','14141414','c',5);
/*!40000 ALTER TABLE `estudiantes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `examenes`
--

DROP TABLE IF EXISTS `examenes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `examenes` (
  `id_examen` int NOT NULL AUTO_INCREMENT,
  `puntaje` decimal(10,2) NOT NULL,
  `fecha_realizacion` date NOT NULL,
  `id_estudiante` int NOT NULL,
  PRIMARY KEY (`id_examen`),
  KEY `fk_EXAMENES_ESTUDIANTES1_idx` (`id_estudiante`),
  CONSTRAINT `fk_EXAMENES_ESTUDIANTES1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `examenes`
--

LOCK TABLES `examenes` WRITE;
/*!40000 ALTER TABLE `examenes` DISABLE KEYS */;
INSERT INTO `examenes` VALUES (1,1000.00,'2025-06-08',1);
/*!40000 ALTER TABLE `examenes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grupos_por_ciclo`
--

DROP TABLE IF EXISTS `grupos_por_ciclo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grupos_por_ciclo` (
  `id_grupo` int NOT NULL AUTO_INCREMENT,
  `nombre_grupo` varchar(45) NOT NULL,
  `id_cc` int NOT NULL,
  `id_colaborador` int NOT NULL,
  PRIMARY KEY (`id_grupo`),
  KEY `fk_GRUPOS_POR_CICLO_CICLOS_CURSOS1_idx` (`id_cc`),
  KEY `fk_grupos_por_ciclo_colaboradores1_idx` (`id_colaborador`),
  CONSTRAINT `fk_GRUPOS_POR_CICLO_CICLOS_CURSOS1` FOREIGN KEY (`id_cc`) REFERENCES `ciclos_cursos` (`id_cc`),
  CONSTRAINT `fk_grupos_por_ciclo_colaboradores1` FOREIGN KEY (`id_colaborador`) REFERENCES `colaboradores` (`id_colaborador`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grupos_por_ciclo`
--

LOCK TABLES `grupos_por_ciclo` WRITE;
/*!40000 ALTER TABLE `grupos_por_ciclo` DISABLE KEYS */;
INSERT INTO `grupos_por_ciclo` VALUES (1,'Ciclo Ciencias',1,1);
/*!40000 ALTER TABLE `grupos_por_ciclo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inscripciones`
--

DROP TABLE IF EXISTS `inscripciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inscripciones` (
  `id_inscripcion` int NOT NULL AUTO_INCREMENT,
  `fecha_inscripcion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_ciclo` int NOT NULL,
  `id_estudiante` int NOT NULL,
  PRIMARY KEY (`id_inscripcion`),
  KEY `fk_INSCRIPCIONES_CICLOS_PROGRAMADOS1_idx` (`id_ciclo`),
  KEY `fk_INSCRIPCIONES_ESTUDIANTES1_idx` (`id_estudiante`),
  CONSTRAINT `fk_INSCRIPCIONES_CICLOS_PROGRAMADOS1` FOREIGN KEY (`id_ciclo`) REFERENCES `ciclos_programados` (`id_ciclo`),
  CONSTRAINT `fk_INSCRIPCIONES_ESTUDIANTES1` FOREIGN KEY (`id_estudiante`) REFERENCES `estudiantes` (`id_estudiante`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inscripciones`
--

LOCK TABLES `inscripciones` WRITE;
/*!40000 ALTER TABLE `inscripciones` DISABLE KEYS */;
INSERT INTO `inscripciones` VALUES (1,'2025-06-09 00:27:43',9,1);
/*!40000 ALTER TABLE `inscripciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagos`
--

DROP TABLE IF EXISTS `pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagos` (
  `id_pago` int NOT NULL AUTO_INCREMENT,
  `monto` decimal(10,2) NOT NULL,
  `fecha_pago` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `id_inscripcion` int NOT NULL,
  PRIMARY KEY (`id_pago`),
  KEY `fk_inscripciones_pagos_idx` (`id_inscripcion`),
  CONSTRAINT `fk_inscripciones_pagos` FOREIGN KEY (`id_inscripcion`) REFERENCES `inscripciones` (`id_inscripcion`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagos`
--

LOCK TABLES `pagos` WRITE;
/*!40000 ALTER TABLE `pagos` DISABLE KEYS */;
INSERT INTO `pagos` VALUES (1,600.00,'2025-06-09 00:58:10',1);
/*!40000 ALTER TABLE `pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profesores`
--

DROP TABLE IF EXISTS `profesores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profesores` (
  `id_profesor` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `ap_paterno` varchar(45) NOT NULL,
  `ap_materno` varchar(45) NOT NULL,
  `tipo_documento` enum('dni','pasaporte') NOT NULL,
  `nro_documento` varchar(20) NOT NULL,
  `id_usuario` int NOT NULL,
  PRIMARY KEY (`id_profesor`),
  KEY `fk_PROFESORES_USUARIOS1_idx` (`id_usuario`),
  CONSTRAINT `fk_PROFESORES_USUARIOS1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profesores`
--

LOCK TABLES `profesores` WRITE;
/*!40000 ALTER TABLE `profesores` DISABLE KEYS */;
INSERT INTO `profesores` VALUES (1,'Roberto','Vegas','Villalva','dni','12121212',4);
/*!40000 ALTER TABLE `profesores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `profesores_especialidades`
--

DROP TABLE IF EXISTS `profesores_especialidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `profesores_especialidades` (
  `id_especialidad` int NOT NULL,
  `id_profesor` int NOT NULL,
  KEY `fk_PROFESORES_has_ESPECIALIDADES_ESPECIALIDADES1_idx` (`id_especialidad`),
  KEY `fk_PROFESORES_has_ESPECIALIDADES_PROFESORES1_idx` (`id_profesor`),
  CONSTRAINT `fk_PROFESORES_has_ESPECIALIDADES_ESPECIALIDADES1` FOREIGN KEY (`id_especialidad`) REFERENCES `especialidades` (`id_especialidad`),
  CONSTRAINT `fk_PROFESORES_has_ESPECIALIDADES_PROFESORES1` FOREIGN KEY (`id_profesor`) REFERENCES `profesores` (`id_profesor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `profesores_especialidades`
--

LOCK TABLES `profesores_especialidades` WRITE;
/*!40000 ALTER TABLE `profesores_especialidades` DISABLE KEYS */;
INSERT INTO `profesores_especialidades` VALUES (1,1),(2,1);
/*!40000 ALTER TABLE `profesores_especialidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sedes`
--

DROP TABLE IF EXISTS `sedes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sedes` (
  `id_sede` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `distrito` varchar(45) NOT NULL,
  PRIMARY KEY (`id_sede`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sedes`
--

LOCK TABLES `sedes` WRITE;
/*!40000 ALTER TABLE `sedes` DISABLE KEYS */;
INSERT INTO `sedes` VALUES (1,'Sede Central','Miraflores'),(2,'Sede Norte','Los Olivos'),(3,'Sede Sur','Chorrillos'),(4,'Sede Ate','Ate'),(5,'Sede Oeste','Callao'),(6,'Sede San Juan','San Juan de Lurigancho'),(7,'Sede Villa','Villa El Salvador'),(8,'Sede La Molina','La Molina'),(9,'Sede San Miguel','San Miguel'),(10,'Sede Independencia','Independencia'),(11,'Sede SJM','San Juan De Miraflores');
/*!40000 ALTER TABLE `sedes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sedes_ciclos`
--

DROP TABLE IF EXISTS `sedes_ciclos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sedes_ciclos` (
  `id_sede` int NOT NULL,
  `id_ciclo` int NOT NULL,
  KEY `fk_SEDES_CICLOS_PROFESORES_SEDES1_idx` (`id_sede`),
  KEY `fk_SEDES_CICLOS_PROFESORES_CICLOS_PROGRAMADOS1_idx` (`id_ciclo`),
  CONSTRAINT `fk_SEDES_CICLOS_PROFESORES_CICLOS_PROGRAMADOS1` FOREIGN KEY (`id_ciclo`) REFERENCES `ciclos_programados` (`id_ciclo`),
  CONSTRAINT `fk_SEDES_CICLOS_PROFESORES_SEDES1` FOREIGN KEY (`id_sede`) REFERENCES `sedes` (`id_sede`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sedes_ciclos`
--

LOCK TABLES `sedes_ciclos` WRITE;
/*!40000 ALTER TABLE `sedes_ciclos` DISABLE KEYS */;
/*!40000 ALTER TABLE `sedes_ciclos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(50) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `contrasenia` varchar(45) NOT NULL,
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `estado` tinyint NOT NULL COMMENT '"False" para cuando la cuenta esta inactiva\\\\\\\\n"True" cuando la cuenta esta activa',
  `rol` enum('estudiante','administrador','profesor','colaborador') NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `correo_UNIQUE` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
INSERT INTO `usuarios` VALUES (1,'luis','luis@gmail.com','admin123','2025-06-08 18:57:53',1,'administrador'),(2,'alex','alex@gmail.com','admin321','2025-06-08 19:01:24',1,'administrador'),(3,'anderson','anderson@gmail.com','colab123','2025-06-08 21:06:09',1,'colaborador'),(4,'roberto','roberto@gmail.com','profe123','2025-06-08 21:06:09',1,'profesor'),(5,'fernando','fernando@gmail.com','estud123','2025-06-08 21:06:09',1,'estudiante'),(6,'juniorA','juniorAAgmail.com','juniorAdmin','2025-06-08 22:12:28',0,'administrador'),(7,'luisus','luisusAgmail.com','luisus123','2025-06-08 22:16:38',1,'administrador'),(8,'luisColab','luisColabAgmail.com','luisColab123','2025-06-09 03:45:45',1,'colaborador');
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `vista_estudiantes`
--

DROP TABLE IF EXISTS `vista_estudiantes`;
/*!50001 DROP VIEW IF EXISTS `vista_estudiantes`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `vista_estudiantes` AS SELECT 
 1 AS `id_estudiante`,
 1 AS `nombre`,
 1 AS `ap_paterno`,
 1 AS `ap_materno`,
 1 AS `tipo_documento`,
 1 AS `nro_documento`,
 1 AS `area_academica`,
 1 AS `id_usuario`*/;
SET character_set_client = @saved_cs_client;

--
-- Final view structure for view `vista_estudiantes`
--

/*!50001 DROP VIEW IF EXISTS `vista_estudiantes`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `vista_estudiantes` AS select `estudiantes`.`id_estudiante` AS `id_estudiante`,`estudiantes`.`nombre` AS `nombre`,`estudiantes`.`ap_paterno` AS `ap_paterno`,`estudiantes`.`ap_materno` AS `ap_materno`,`estudiantes`.`tipo_documento` AS `tipo_documento`,`estudiantes`.`nro_documento` AS `nro_documento`,`estudiantes`.`area_academica` AS `area_academica`,`estudiantes`.`id_usuario` AS `id_usuario` from `estudiantes` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-06-09 22:42:03
