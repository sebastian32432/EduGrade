from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func

from app import db
from models import Teacher, Course, Student, Enrollment, Assignment, Grade
from forms import CourseForm, AssignmentForm, GradeForm

# Create blueprint
teacher_bp = Blueprint('teacher', __name__, url_prefix='/teacher')

# Middleware to check if user is a teacher
@teacher_bp.before_request
def check_teacher():
    if not current_user.is_authenticated or current_user.role != 'teacher':
        flash('No tienes permiso para acceder a esta página', 'danger')
        return redirect(url_for('auth.login'))

@teacher_bp.route('/')
@teacher_bp.route('/dashboard')
@login_required
def dashboard():
    # Get the teacher profile
    teacher = Teacher.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Get courses taught by this teacher
    courses = Course.query.filter_by(teacher_id=teacher.id).all()
    
    # Count students per course
    course_stats = []
    for course in courses:
        students_count = Enrollment.query.filter_by(course_id=course.id).count()
        course_stats.append({
            'course': course,
            'students_count': students_count
        })
    
    # Get total students (unique)
    total_students = db.session.query(func.count(func.distinct(Enrollment.student_id))).join(
        Course, Course.id == Enrollment.course_id
    ).filter(Course.teacher_id == teacher.id).scalar() or 0
    
    # Get recent grades
    recent_grades = db.session.query(Grade, Student, Assignment, Course).join(
        Student, Grade.student_id == Student.id
    ).join(
        Assignment, Grade.assignment_id == Assignment.id
    ).join(
        Course, Assignment.course_id == Course.id
    ).filter(
        Course.teacher_id == teacher.id
    ).order_by(Grade.graded_at.desc()).limit(5).all()
    
    # Calculate average grade across all courses
    avg_grade = db.session.query(func.avg(Grade.score)).join(
        Assignment, Grade.assignment_id == Assignment.id
    ).join(
        Course, Assignment.course_id == Course.id
    ).filter(
        Course.teacher_id == teacher.id
    ).scalar() or 0
    
    # Get upcoming assignments
    upcoming_assignments = db.session.query(Assignment, Course).join(
        Course, Assignment.course_id == Course.id
    ).filter(
        Course.teacher_id == teacher.id,
        Assignment.due_date >= func.current_date()
    ).order_by(Assignment.due_date).limit(5).all()
    
    return render_template(
        'teacher/dashboard.html',
        teacher=teacher,
        course_stats=course_stats,
        total_students=total_students,
        recent_grades=recent_grades,
        avg_grade=avg_grade,
        upcoming_assignments=upcoming_assignments
    )

@teacher_bp.route('/courses')
@login_required
def courses():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first_or_404()
    courses = Course.query.filter_by(teacher_id=teacher.id).all()
    
    # Get student counts for each course
    for course in courses:
        course.student_count = Enrollment.query.filter_by(course_id=course.id).count()
    
    return render_template('teacher/courses.html', courses=courses)

@teacher_bp.route('/courses/add', methods=['GET', 'POST'])
@login_required
def add_course():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first_or_404()
    form = CourseForm()
    
    if form.validate_on_submit():
        course = Course(
            name=form.name.data,
            code=form.code.data,
            description=form.description.data,
            teacher_id=teacher.id
        )
        db.session.add(course)
        db.session.commit()
        
        flash('Curso creado exitosamente', 'success')
        return redirect(url_for('teacher.courses'))
    
    return render_template('teacher/course_form.html', form=form, title='Agregar Curso')

@teacher_bp.route('/courses/<int:course_id>')
@login_required
def course_details(course_id):
    teacher = Teacher.query.filter_by(user_id=current_user.id).first_or_404()
    course = Course.query.filter_by(id=course_id, teacher_id=teacher.id).first_or_404()
    
    # Get enrolled students
    enrolled_students = db.session.query(Student, User).join(
        User, Student.user_id == User.id
    ).join(
        Enrollment, Student.id == Enrollment.student_id
    ).filter(
        Enrollment.course_id == course.id
    ).all()
    
    # Get assignments for this course
    assignments = Assignment.query.filter_by(course_id=course.id).order_by(Assignment.due_date).all()
    
    return render_template(
        'teacher/course_details.html',
        course=course,
        enrolled_students=enrolled_students,
        assignments=assignments
    )

@teacher_bp.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    teacher = Teacher.query.filter_by(user_id=current_user.id).first_or_404()
    course = Course.query.filter_by(id=course_id, teacher_id=teacher.id).first_or_404()
    
    form = CourseForm()
    if form.validate_on_submit():
        course.name = form.name.data
        course.code = form.code.data
        course.description = form.description.data
        
        db.session.commit()
        flash('Curso actualizado exitosamente', 'success')
        return redirect(url_for('teacher.course_details', course_id=course.id))
    
    # Pre-populate form
    if request.method == 'GET':
        form.name.data = course.name
        form.code.data = course.code
        form.description.data = course.description
    
    return render_template('teacher/course_form.html', form=form, title='Editar Curso')

@teacher_bp.route('/assignments')
@login_required
def assignments():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Get all assignments for teacher's courses
    assignments_with_courses = db.session.query(Assignment, Course).join(
        Course, Assignment.course_id == Course.id
    ).filter(
        Course.teacher_id == teacher.id
    ).order_by(Assignment.due_date.desc()).all()
    
    return render_template('teacher/assignments.html', assignments_with_courses=assignments_with_courses)

@teacher_bp.route('/courses/<int:course_id>/assignments/add', methods=['GET', 'POST'])
@login_required
def add_assignment(course_id):
    teacher = Teacher.query.filter_by(user_id=current_user.id).first_or_404()
    course = Course.query.filter_by(id=course_id, teacher_id=teacher.id).first_or_404()
    
    form = AssignmentForm()
    if form.validate_on_submit():
        assignment = Assignment(
            title=form.title.data,
            description=form.description.data,
            course_id=course.id,
            max_points=form.max_points.data
        )
        db.session.add(assignment)
        db.session.commit()
        
        flash('Asignación creada exitosamente', 'success')
        return redirect(url_for('teacher.course_details', course_id=course.id))
    
    return render_template('teacher/assignment_form.html', form=form, course=course, title='Agregar Asignación')

@teacher_bp.route('/grades')
@login_required
def grades():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Get courses taught by this teacher
    courses = Course.query.filter_by(teacher_id=teacher.id).all()
    
    # Filter by course if specified
    course_id = request.args.get('course_id', type=int)
    course_filter = None
    if course_id:
        course_filter = Course.query.get_or_404(course_id)
        if course_filter.teacher_id != teacher.id:
            flash('No tienes permiso para ver este curso', 'danger')
            return redirect(url_for('teacher.grades'))
    
    # Get students and their grades
    students_with_grades = []
    query = db.session.query(Student, User).join(User, Student.user_id == User.id)
    
    # Filter students by course if necessary
    if course_filter:
        query = query.join(Enrollment, Student.id == Enrollment.student_id).filter(Enrollment.course_id == course_id)
    else:
        # Only include students in at least one of teacher's courses
        query = query.join(Enrollment, Student.id == Enrollment.student_id).join(
            Course, Enrollment.course_id == Course.id
        ).filter(Course.teacher_id == teacher.id).distinct()
    
    students = query.all()
    
    for student, user in students:
        # Get grades for this student
        student_grades = []
        courses_query = Course.query
        
        if course_filter:
            courses_query = courses_query.filter_by(id=course_id)
        else:
            courses_query = courses_query.filter_by(teacher_id=teacher.id)
        
        for course in courses_query.all():
            assignments = Assignment.query.filter_by(course_id=course.id).all()
            for assignment in assignments:
                grade = Grade.query.filter_by(
                    student_id=student.id,
                    assignment_id=assignment.id
                ).first()
                
                student_grades.append({
                    'course': course,
                    'assignment': assignment,
                    'grade': grade,
                    'max_points': assignment.max_points
                })
        
        students_with_grades.append({
            'student': student,
            'user': user,
            'grades': student_grades
        })
    
    return render_template(
        'teacher/grades.html',
        students_with_grades=students_with_grades,
        courses=courses,
        course_filter=course_filter
    )

@teacher_bp.route('/assignments/<int:assignment_id>/grade/<int:student_id>', methods=['GET', 'POST'])
@login_required
def grade_assignment(assignment_id, student_id):
    teacher = Teacher.query.filter_by(user_id=current_user.id).first_or_404()
    
    # Get the assignment and verify teacher has access
    assignment = Assignment.query.get_or_404(assignment_id)
    course = Course.query.get_or_404(assignment.course_id)
    if course.teacher_id != teacher.id:
        flash('No tienes permiso para calificar esta asignación', 'danger')
        return redirect(url_for('teacher.grades'))
    
    # Get the student and verify enrollment
    student = Student.query.get_or_404(student_id)
    enrollment = Enrollment.query.filter_by(
        student_id=student.id,
        course_id=course.id
    ).first()
    if not enrollment:
        flash('Este estudiante no está inscrito en este curso', 'danger')
        return redirect(url_for('teacher.grades'))
    
    # Get existing grade if any
    grade = Grade.query.filter_by(
        student_id=student.id,
        assignment_id=assignment.id
    ).first()
    
    form = GradeForm()
    if form.validate_on_submit():
        if grade:
            # Update existing grade
            grade.score = form.score.data
            grade.comments = form.comments.data
        else:
            # Create new grade
            grade = Grade(
                student_id=student.id,
                assignment_id=assignment.id,
                score=form.score.data,
                comments=form.comments.data
            )
            db.session.add(grade)
        
        db.session.commit()
        flash('Calificación guardada exitosamente', 'success')
        return redirect(url_for('teacher.grades'))
    
    # Pre-populate form
    if request.method == 'GET' and grade:
        form.score.data = grade.score
        form.comments.data = grade.comments
    
    student_user = User.query.get(student.user_id)
    return render_template(
        'teacher/grade_form.html',
        form=form,
        assignment=assignment,
        student=student,
        student_user=student_user,
        course=course,
        max_points=assignment.max_points
    )

@teacher_bp.route('/profile')
@login_required
def profile():
    teacher = Teacher.query.filter_by(user_id=current_user.id).first_or_404()
    courses_count = Course.query.filter_by(teacher_id=teacher.id).count()
    
    # Count unique students
    students_count = db.session.query(func.count(func.distinct(Enrollment.student_id))).join(
        Course, Course.id == Enrollment.course_id
    ).filter(Course.teacher_id == teacher.id).scalar() or 0
    
    # Get courses with student counts
    courses = Course.query.filter_by(teacher_id=teacher.id).all()
    for course in courses:
        course.student_count = Enrollment.query.filter_by(course_id=course.id).count()
    
    return render_template(
        'teacher/profile.html',
        teacher=teacher,
        courses_count=courses_count,
        students_count=students_count,
        courses=courses
    )
