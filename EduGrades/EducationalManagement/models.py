from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text, Enum
from sqlalchemy.orm import relationship

from app import db, login_manager

# User roles
class Role(Enum):
    ADMIN = 'admin'
    TEACHER = 'teacher'
    STUDENT = 'student'

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    role = Column(String(20), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    teacher = relationship("Teacher", back_populates="user", uselist=False, cascade="all, delete-orphan")
    student = relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")
    admin = relationship("Admin", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    def __init__(self, username, email, first_name, last_name, role, password=None):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        if password:
            self.set_password(password)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Teacher(db.Model):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    title = Column(String(64))
    department = Column(String(64))
    
    # Relationships
    user = relationship("User", back_populates="teacher")
    courses = relationship("Course", back_populates="teacher")
    
    def __repr__(self):
        return f'<Teacher {self.user.get_full_name()}>'

class Student(db.Model):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    grade_level = Column(String(32))
    
    # Relationships
    user = relationship("User", back_populates="student")
    enrollments = relationship("Enrollment", back_populates="student")
    grades = relationship("Grade", back_populates="student")
    
    def __repr__(self):
        return f'<Student {self.user.get_full_name()}>'

class Admin(db.Model):
    __tablename__ = 'admins'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="admin")
    
    def __repr__(self):
        return f'<Admin {self.user.get_full_name()}>'

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    description = Column(Text)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    teacher = relationship("Teacher", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")
    assignments = relationship("Assignment", back_populates="course")
    
    def __repr__(self):
        return f'<Course {self.name}>'

class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    enrollment_date = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
    def __repr__(self):
        return f'<Enrollment {self.student.user.username} in {self.course.name}>'

class Assignment(db.Model):
    __tablename__ = 'assignments'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    due_date = Column(DateTime)
    max_points = Column(Float, default=100.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    course = relationship("Course", back_populates="assignments")
    grades = relationship("Grade", back_populates="assignment")
    
    def __repr__(self):
        return f'<Assignment {self.title}>'

class Grade(db.Model):
    __tablename__ = 'grades'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    assignment_id = Column(Integer, ForeignKey('assignments.id'), nullable=False)
    score = Column(Float)
    comments = Column(Text)
    graded_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    student = relationship("Student", back_populates="grades")
    assignment = relationship("Assignment", back_populates="grades")
    
    def __repr__(self):
        return f'<Grade {self.student.user.username} - {self.assignment.title}: {self.score}>'
