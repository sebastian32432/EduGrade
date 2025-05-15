# Instrucciones para la Base de Datos de EduGrade

Este documento proporciona instrucciones sobre cómo utilizar los scripts de base de datos para el sistema EduGrade.

## Archivos Disponibles

1. `edugrade_db_schema.sql` - Script completo para crear la base de datos MySQL, incluyendo tablas, procedimientos almacenados, vistas y datos iniciales.
2. `db_diagram.md` - Diagrama entidad-relación que visualiza la estructura de la base de datos.

## Requisitos Previos

Para utilizar estos scripts, necesitarás:

- Servidor MySQL 5.7 o superior instalado
- Cliente MySQL o herramienta como MySQL Workbench, phpMyAdmin, etc.
- Permisos de administrador en el servidor de base de datos

## Instrucciones para Crear la Base de Datos

### Opción 1: Usando la línea de comandos MySQL

1. Abre una terminal/consola
2. Inicia sesión en tu servidor MySQL:
   ```
   mysql -u root -p
   ```
3. Ejecuta el script:
   ```
   source /ruta/a/edugrade_db_schema.sql
   ```

### Opción 2: Usando MySQL Workbench

1. Abre MySQL Workbench
2. Conéctate a tu servidor MySQL
3. Ve a File > Open SQL Script... y selecciona `edugrade_db_schema.sql`
4. Haz clic en el botón "Execute" (el rayo) para ejecutar todo el script

### Opción 3: Usando phpMyAdmin

1. Abre phpMyAdmin en tu navegador
2. Inicia sesión en tu servidor MySQL
3. Ve a la pestaña "Import"
4. Navega y selecciona el archivo `edugrade_db_schema.sql`
5. Haz clic en "Go" para ejecutar el script

## Configuración de la Aplicación

Una vez creada la base de datos, debes configurar la aplicación para que se conecte correctamente:

1. En el archivo `config.py`, asegúrate de que la variable `SQLALCHEMY_DATABASE_URI` tenga la cadena de conexión correcta:

```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://usuario:contraseña@host/edugrade'
```

Reemplaza:
- `usuario`: El nombre de usuario de MySQL
- `contraseña`: La contraseña del usuario
- `host`: La dirección del servidor MySQL (localhost si es local)

## Procedimientos Almacenados Disponibles

El script crea varios procedimientos almacenados útiles:

1. `GetStudentAverageGrade(studentId)`: Obtiene el promedio de calificaciones de un estudiante.
2. `GetCourseGrades(courseId)`: Obtiene todas las calificaciones de un curso.
3. `GetStudentGradeReport(studentId)`: Genera un reporte completo de calificaciones para un estudiante.

Para usar estos procedimientos desde MySQL:

```sql
CALL GetStudentAverageGrade(1);
CALL GetCourseGrades(1);
CALL GetStudentGradeReport(1);
```

## Vistas Disponibles

El script también crea varias vistas útiles:

1. `course_enrollment_counts`: Muestra el número de estudiantes en cada curso.
2. `course_grade_averages`: Muestra estadísticas de calificaciones por asignación y curso.
3. `student_performance_summary`: Muestra un resumen del desempeño de cada estudiante.

Para consultar estas vistas:

```sql
SELECT * FROM course_enrollment_counts;
SELECT * FROM course_grade_averages;
SELECT * FROM student_performance_summary;
```

## Credenciales de Usuario Demo

El script crea tres usuarios de demostración:

1. Administrador:
   - Username: admin
   - Contraseña: admin123

2. Profesor:
   - Username: profesor
   - Contraseña: profesor123

3. Estudiante:
   - Username: estudiante
   - Contraseña: estudiante123

## Estructura de Tablas

La estructura completa de la base de datos se puede visualizar en el archivo `db_diagram.md`. Incluye las siguientes tablas principales:

- `users`: Información básica de todos los usuarios
- `teachers`, `students`, `admins`: Información específica según el rol del usuario
- `courses`: Información de los cursos
- `assignments`: Tareas y asignaciones
- `enrollments`: Inscripciones de estudiantes en cursos
- `grades`: Calificaciones de estudiantes en asignaciones