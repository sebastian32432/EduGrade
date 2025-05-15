import os
import sys
from app import db, create_app
from models import User, Student, Teacher, Admin, Course, Assignment, Grade

def seed_database():
    """Populate the database with sample data."""
    app = create_app()
    with app.app_context():
        # Crear usuarios de prueba
        print("Creando usuarios de prueba...")
        # 1. Admin
        admin_user = User(
            username="admin",
            email="admin@edugrade.com",
            first_name="Administrador",
            last_name="Principal",
            role="admin"
        )
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        db.session.flush()  # Para obtener el ID
        
        admin = Admin(user_id=admin_user.id)
        db.session.add(admin)

        # 2. Profesor
        teacher_user = User(
            username="profesor",
            email="profesor@edugrade.com",
            first_name="Juan",
            last_name="Pérez",
            role="teacher"
        )
        teacher_user.set_password("profesor123")
        db.session.add(teacher_user)
        db.session.flush()  # Para obtener el ID
        
        teacher = Teacher(
            user_id=teacher_user.id,
            title="Doctor en Educación",
            department="Matemáticas"
        )
        db.session.add(teacher)

        # 3. Estudiante
        student_user = User(
            username="estudiante",
            email="estudiante@edugrade.com",
            first_name="María",
            last_name="López",
            role="student"
        )
        student_user.set_password("estudiante123")
        db.session.add(student_user)
        db.session.flush()  # Para obtener el ID
        
        student = Student(
            user_id=student_user.id,
            grade_level="Segundo Año"
        )
        db.session.add(student)

        # Crear algunos cursos
        print("Creando cursos...")
        course1 = Course(
            name="Matemáticas Avanzadas",
            code="MAT101",
            description="Curso avanzado de cálculo y álgebra",
            teacher_id=teacher.id
        )
        course2 = Course(
            name="Programación Básica",
            code="PRG101",
            description="Introducción a la programación con Python",
            teacher_id=teacher.id
        )
        db.session.add_all([course1, course2])
        db.session.flush()

        # Crear algunas tareas
        print("Creando tareas...")
        assignment1 = Assignment(
            title="Examen Parcial 1",
            description="Primer examen parcial de matemáticas",
            course_id=course1.id,
            max_points=100.0
        )
        assignment2 = Assignment(
            title="Proyecto Final",
            description="Proyecto final de programación",
            course_id=course2.id,
            max_points=100.0
        )
        db.session.add_all([assignment1, assignment2])
        db.session.flush()

        # Guardar todos los cambios
        db.session.commit()
        print("Datos de prueba creados exitosamente!")

if __name__ == "__main__":
    seed_database()