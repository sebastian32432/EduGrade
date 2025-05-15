from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import func

from app import db
from models import Student, Course, Enrollment, Assignment, Grade

# Create blueprint
student_bp = Blueprint('student', __name__, url_prefix='/student')

# Middleware to check if user is a student
@student_bp.before_request
def check_student():
    if not current_user.is_authenticated or current_user.role != 'student':
        flash('No tienes permiso para acceder a esta página', 'danger')
        return redirect(url_for('auth.login'))

@student_bp.route('/')
@student_bp.route('/dashboard')
@login_required
def dashboard():
    student = Student.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Get enrolled courses
    enrolled_courses = db.session.query(Course).join(
        Enrollment, Course.id == Enrollment.course_id
    ).filter(
        Enrollment.student_id == student.id
    ).all()
    
    # Get upcoming assignments
    upcoming_assignments = db.session.query(Assignment, Course).join(
        Course, Assignment.course_id == Course.id
    ).join(
        Enrollment, Course.id == Enrollment.course_id
    ).filter(
        Enrollment.student_id == student.id,
        Assignment.due_date >= func.current_date()
    ).order_by(Assignment.due_date).limit(5).all()
    
    # Get recent grades
    recent_grades = db.session.query(Grade, Assignment, Course).join(
        Assignment, Grade.assignment_id == Assignment.id
    ).join(
        Course, Assignment.course_id == Course.id
    ).filter(
        Grade.student_id == student.id
    ).order_by(Grade.graded_at.desc()).limit(5).all()
    
    # Calculate average grade
    avg_grade = db.session.query(func.avg(Grade.score)).filter(
        Grade.student_id == student.id
    ).scalar() or 0
    
    return render_template(
        'student/dashboard.html',
        student=student,
        enrolled_courses=enrolled_courses,
        upcoming_assignments=upcoming_assignments,
        recent_grades=recent_grades,
        avg_grade=avg_grade,
        courses_count=len(enrolled_courses)
    )

@student_bp.route('/courses')
@login_required
def courses():
    student = Student.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Get all enrolled courses
    enrolled_courses = db.session.query(Course, Enrollment).join(
        Enrollment, Course.id == Enrollment.course_id
    ).filter(
        Enrollment.student_id == student.id
    ).all()
    
    return render_template('student/courses.html', enrolled_courses=enrolled_courses)

@student_bp.route('/courses/<int:course_id>')
@login_required
def course_details(course_id):
    student = Student.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Check if student is enrolled
    enrollment = Enrollment.query.filter_by(
        student_id=student.id,
        course_id=course_id
    ).first_or_404()
    
    course = Course.query.get_or_404(course_id)
    
    # Get assignments and grades for this course
    assignments_with_grades = []
    assignments = Assignment.query.filter_by(course_id=course.id).order_by(Assignment.due_date).all()
    
    for assignment in assignments:
        grade = Grade.query.filter_by(
            student_id=student.id,
            assignment_id=assignment.id
        ).first()
        
        assignments_with_grades.append({
            'assignment': assignment,
            'grade': grade
        })
    
    # Calculate course average
    course_grades = []
    for ag in assignments_with_grades:
        if ag['grade']:
            course_grades.append(ag['grade'].score)
    
    course_avg = sum(course_grades) / len(course_grades) if course_grades else 0
    
    return render_template(
        'student/course_details.html',
        course=course,
        assignments_with_grades=assignments_with_grades,
        course_avg=course_avg
    )

@student_bp.route('/grades')
@login_required
def grades():
    student = Student.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Get all grades grouped by course
    courses_with_grades = []
    
    enrolled_courses = db.session.query(Course).join(
        Enrollment, Course.id == Enrollment.course_id
    ).filter(
        Enrollment.student_id == student.id
    ).all()
    
    for course in enrolled_courses:
        course_assignments = Assignment.query.filter_by(course_id=course.id).all()
        assignments_with_grades = []
        
        for assignment in course_assignments:
            grade = Grade.query.filter_by(
                student_id=student.id,
                assignment_id=assignment.id
            ).first()
            
            assignments_with_grades.append({
                'assignment': assignment,
                'grade': grade
            })
        
        # Calculate course average
        course_grades = []
        for ag in assignments_with_grades:
            if ag['grade']:
                course_grades.append(ag['grade'].score)
        
        course_avg = sum(course_grades) / len(course_grades) if course_grades else 0
        
        courses_with_grades.append({
            'course': course,
            'assignments_with_grades': assignments_with_grades,
            'average': course_avg
        })
    
    # Calculate overall average
    all_grades = []
    for cwg in courses_with_grades:
        for ag in cwg['assignments_with_grades']:
            if ag['grade']:
                all_grades.append(ag['grade'].score)
    
    overall_avg = sum(all_grades) / len(all_grades) if all_grades else 0
    
    return render_template(
        'student/grades.html',
        courses_with_grades=courses_with_grades,
        overall_avg=overall_avg
    )

@student_bp.route('/profile')
@login_required
def profile():
    student = Student.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Count enrolled courses
    courses_count = Enrollment.query.filter_by(student_id=student.id).count()
    
    # Calculate GPA
    avg_grade = db.session.query(func.avg(Grade.score)).filter(
        Grade.student_id == student.id
    ).scalar() or 0
    
    # Convert to 4.0 scale (assuming grades are on a 100-point scale)
    gpa = min(4.0, avg_grade / 25.0) if avg_grade else 0
    
    # Get recently completed assignments
    completed_assignments = db.session.query(Grade, Assignment, Course).join(
        Assignment, Grade.assignment_id == Assignment.id
    ).join(
        Course, Assignment.course_id == Course.id
    ).filter(
        Grade.student_id == student.id
    ).order_by(Grade.graded_at.desc()).limit(5).all()
    
    return render_template(
        'student/profile.html',
        student=student,
        courses_count=courses_count,
        avg_grade=avg_grade,
        gpa=gpa,
        completed_assignments=completed_assignments
    )
