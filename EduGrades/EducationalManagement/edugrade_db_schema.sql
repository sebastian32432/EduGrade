-- Script para crear la base de datos EduGrade en MySQL
-- Este script crea la estructura completa para el sistema EduGrade
-- con tablas para usuarios, profesores, estudiantes, cursos, calificaciones, etc.

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS edugrade;
USE edugrade;

-- Eliminar tablas existentes si existen (en orden inverso debido a las claves foráneas)
DROP TABLE IF EXISTS grades;
DROP TABLE IF EXISTS assignments;
DROP TABLE IF EXISTS enrollments;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS admins;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS users;

-- Tabla de usuarios
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    role VARCHAR(20) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de administradores
CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de profesores
CREATE TABLE teachers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    title VARCHAR(64),
    department VARCHAR(64),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de estudiantes
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL UNIQUE,
    grade_level VARCHAR(32),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de cursos
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    teacher_id INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (teacher_id) REFERENCES teachers(id) ON DELETE SET NULL,
    INDEX idx_code (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de inscripciones
CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    UNIQUE KEY unique_enrollment (student_id, course_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de asignaciones
CREATE TABLE assignments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    course_id INT NOT NULL,
    due_date DATETIME,
    max_points FLOAT DEFAULT 100.0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de calificaciones
CREATE TABLE grades (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    assignment_id INT NOT NULL,
    score FLOAT,
    comments TEXT,
    graded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (assignment_id) REFERENCES assignments(id) ON DELETE CASCADE,
    UNIQUE KEY unique_grade (student_id, assignment_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insertar datos de usuario de demostración
-- Las contraseñas están en texto plano aquí, pero se guardarán hasheadas en la aplicación

-- Creación de usuario administrador
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active) VALUES 
('admin', 'admin@edugrade.com', 'pbkdf2:sha256:600000$YO2NRnlmTM9YnFBO$f9e0caf1b2222ef28f0d7f580a8afe86d7a764e74b114ef7d42afd9da51e9f07', 'Administrador', 'Principal', 'admin', 1);

-- Creación del registro en la tabla admins
INSERT INTO admins (user_id) VALUES (LAST_INSERT_ID());

-- Creación de usuario profesor
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active) VALUES 
('profesor', 'profesor@edugrade.com', 'pbkdf2:sha256:600000$CZZAqmmmkrXLQxYy$4c0ab3d2efee62663d640e60bf1a17bccac43897f0d92e5e8dd9bd57e08ca85c', 'Juan', 'Pérez', 'teacher', 1);

-- Obtenemos el ID de usuario creado
SET @teacher_user_id = LAST_INSERT_ID();

-- Creación del registro en la tabla teachers
INSERT INTO teachers (user_id, title, department) VALUES (@teacher_user_id, 'Doctor en Educación', 'Matemáticas');

-- Obtenemos el ID del profesor creado
SET @teacher_id = LAST_INSERT_ID();

-- Creación de usuario estudiante
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active) VALUES 
('estudiante', 'estudiante@edugrade.com', 'pbkdf2:sha256:600000$YfhdTqYV5oSj8HBL$ccdba20c3b8cec33c27e10daa4d0d19c5801de5e91b5dd7a5a9b0487cbbb4eca', 'María', 'López', 'student', 1);

-- Obtenemos el ID de usuario creado
SET @student_user_id = LAST_INSERT_ID();

-- Creación del registro en la tabla students
INSERT INTO students (user_id, grade_level) VALUES (@student_user_id, 'Segundo Año');

-- Obtenemos el ID del estudiante creado
SET @student_id = LAST_INSERT_ID();

-- Creación de cursos
INSERT INTO courses (name, code, description, teacher_id) VALUES 
('Matemáticas Avanzadas', 'MAT101', 'Curso avanzado de cálculo y álgebra', @teacher_id),
('Programación Básica', 'PRG101', 'Introducción a la programación con Python', @teacher_id);

-- Obtenemos los IDs de los cursos creados
SET @course1_id = LAST_INSERT_ID();
SET @course2_id = @course1_id + 1;

-- Inscribir al estudiante en los cursos
INSERT INTO enrollments (student_id, course_id) VALUES 
(@student_id, @course1_id),
(@student_id, @course2_id);

-- Crear asignaciones
INSERT INTO assignments (title, description, course_id, max_points) VALUES 
('Examen Parcial 1', 'Primer examen parcial de matemáticas', @course1_id, 100.0),
('Proyecto Final', 'Proyecto final de programación', @course2_id, 100.0);

-- Obtenemos los IDs de las asignaciones creadas
SET @assignment1_id = LAST_INSERT_ID();
SET @assignment2_id = @assignment1_id + 1;

-- Crear calificaciones
INSERT INTO grades (student_id, assignment_id, score, comments) VALUES 
(@student_id, @assignment1_id, 85.5, 'Buen trabajo, pero necesita mejorar en derivadas.'),
(@student_id, @assignment2_id, 92.0, 'Excelente proyecto, funcionalidad completa.');

-- Creación de procedimientos almacenados

-- Procedimiento para obtener el promedio de calificaciones de un estudiante
DELIMITER $$
CREATE PROCEDURE GetStudentAverageGrade(IN studentId INT)
BEGIN
    SELECT s.id, CONCAT(u.first_name, ' ', u.last_name) AS student_name, 
           AVG(g.score) AS average_grade
    FROM students s
    JOIN users u ON s.user_id = u.id
    JOIN grades g ON g.student_id = s.id
    WHERE s.id = studentId
    GROUP BY s.id, student_name;
END$$
DELIMITER ;

-- Procedimiento para obtener todas las calificaciones de un curso
DELIMITER $$
CREATE PROCEDURE GetCourseGrades(IN courseId INT)
BEGIN
    SELECT c.name AS course_name, 
           CONCAT(u.first_name, ' ', u.last_name) AS student_name,
           a.title AS assignment_title, 
           g.score, 
           g.comments,
           g.graded_at
    FROM grades g
    JOIN students s ON g.student_id = s.id
    JOIN users u ON s.user_id = u.id
    JOIN assignments a ON g.assignment_id = a.id
    JOIN courses c ON a.course_id = c.id
    WHERE c.id = courseId
    ORDER BY u.last_name, u.first_name, a.title;
END$$
DELIMITER ;

-- Procedimiento para obtener el reporte de calificaciones de un estudiante
DELIMITER $$
CREATE PROCEDURE GetStudentGradeReport(IN studentId INT)
BEGIN
    SELECT c.name AS course_name, 
           c.code AS course_code,
           a.title AS assignment_title, 
           a.max_points,
           g.score, 
           (g.score / a.max_points * 100) AS percentage,
           g.graded_at
    FROM grades g
    JOIN assignments a ON g.assignment_id = a.id
    JOIN courses c ON a.course_id = c.id
    WHERE g.student_id = studentId
    ORDER BY c.name, a.title;
END$$
DELIMITER ;

-- Vistas útiles para reportes

-- Vista para el conteo de estudiantes por curso
CREATE VIEW course_enrollment_counts AS
SELECT c.id AS course_id, c.name AS course_name, c.code AS course_code,
       COUNT(e.id) AS student_count
FROM courses c
LEFT JOIN enrollments e ON c.id = e.course_id
GROUP BY c.id, c.name, c.code;

-- Vista para el promedio de calificaciones por curso
CREATE VIEW course_grade_averages AS
SELECT c.id AS course_id, c.name AS course_name, c.code AS course_code,
       a.id AS assignment_id, a.title AS assignment_title,
       AVG(g.score) AS average_score,
       MIN(g.score) AS min_score,
       MAX(g.score) AS max_score,
       COUNT(g.id) AS graded_count
FROM courses c
JOIN assignments a ON c.id = a.course_id
LEFT JOIN grades g ON a.id = g.assignment_id
GROUP BY c.id, c.name, c.code, a.id, a.title;

-- Vista para el resumen de desempeño de estudiantes
CREATE VIEW student_performance_summary AS
SELECT s.id AS student_id, 
       CONCAT(u.first_name, ' ', u.last_name) AS student_name,
       COUNT(DISTINCT e.course_id) AS enrolled_courses,
       COUNT(DISTINCT g.assignment_id) AS completed_assignments,
       AVG(g.score) AS average_score
FROM students s
JOIN users u ON s.user_id = u.id
LEFT JOIN enrollments e ON s.id = e.student_id
LEFT JOIN grades g ON s.id = g.student_id
GROUP BY s.id, student_name;