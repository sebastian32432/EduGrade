# Diagrama Entidad-Relación de EduGrade

```mermaid
erDiagram
    USERS ||--o| TEACHERS : "tiene"
    USERS ||--o| STUDENTS : "tiene"
    USERS ||--o| ADMINS : "tiene"
    TEACHERS ||--o{ COURSES : "enseña"
    STUDENTS ||--o{ ENROLLMENTS : "tiene"
    COURSES ||--o{ ENROLLMENTS : "tiene"
    COURSES ||--o{ ASSIGNMENTS : "tiene"
    STUDENTS ||--o{ GRADES : "recibe"
    ASSIGNMENTS ||--o{ GRADES : "tiene"

    USERS {
        int id PK
        string username UK
        string email UK
        string password_hash
        string first_name
        string last_name
        string role
        boolean is_active
        datetime created_at
    }

    TEACHERS {
        int id PK
        int user_id FK
        string title
        string department
    }

    STUDENTS {
        int id PK
        int user_id FK
        string grade_level
    }

    ADMINS {
        int id PK
        int user_id FK
    }

    COURSES {
        int id PK
        string name
        string code UK
        text description
        int teacher_id FK
        datetime created_at
    }

    ENROLLMENTS {
        int id PK
        int student_id FK
        int course_id FK
        datetime enrollment_date
    }

    ASSIGNMENTS {
        int id PK
        string title
        text description
        int course_id FK
        datetime due_date
        float max_points
        datetime created_at
    }

    GRADES {
        int id PK
        int student_id FK
        int assignment_id FK
        float score
        text comments
        datetime graded_at
    }
```

## Descripción de las tablas

1. **USERS**: Almacena la información básica de todos los usuarios del sistema, independientemente de su rol.
2. **TEACHERS**: Contiene información específica de los profesores, relacionada con un usuario.
3. **STUDENTS**: Contiene información específica de los estudiantes, relacionada con un usuario.
4. **ADMINS**: Contiene información específica de los administradores, relacionada con un usuario.
5. **COURSES**: Almacena la información de los cursos ofrecidos, asignados a un profesor.
6. **ENROLLMENTS**: Tabla de relación que registra la inscripción de estudiantes en cursos.
7. **ASSIGNMENTS**: Contiene las tareas o asignaciones que pertenecen a un curso específico.
8. **GRADES**: Almacena las calificaciones que los estudiantes reciben en las asignaciones.

## Relaciones principales

- Un usuario puede ser un profesor, un estudiante o un administrador (relación 1:0..1).
- Un profesor puede enseñar múltiples cursos (relación 1:N).
- Un estudiante puede inscribirse en múltiples cursos a través de la tabla de enrollments (relación M:N).
- Un curso puede tener múltiples asignaciones (relación 1:N).
- Un estudiante recibe calificaciones para asignaciones específicas (relación M:N a través de la tabla grades).

Este modelo de datos soporta todas las funcionalidades del sistema educativo, incluyendo la gestión de usuarios con diferentes roles, cursos, inscripciones, asignaciones y calificaciones.