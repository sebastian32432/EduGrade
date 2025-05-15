from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func

from app import db
from models import User, Admin, Teacher, Student, Course, Enrollment, Grade, Assignment
from forms import UserForm, CourseForm

# Create blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Middleware to check if user is an admin
@admin_bp.before_request
def check_admin():
    if not current_user.is_authenticated or current_user.role != 'admin':
        flash('No tienes permiso para acceder a esta página', 'danger')
        return redirect(url_for('auth.login'))

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # Get statistics for dashboard
    stats = {
        'total_users': User.query.count(),
        'total_teachers': Teacher.query.count(),
        'total_students': Student.query.count(),
        'total_courses': Course.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
    }
    
    # Get recent user registrations
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', stats=stats, recent_users=recent_users)

@admin_bp.route('/users')
@login_required
def users():
    query = User.query
    
    # Handle filtering
    role_filter = request.args.get('role')
    if role_filter and role_filter != 'all':
        query = query.filter(User.role == role_filter)
    
    # Handle search
    search = request.args.get('search')
    if search:
        query = query.filter(
            (User.username.ilike(f'%{search}%')) | 
            (User.email.ilike(f'%{search}%')) |
            (User.first_name.ilike(f'%{search}%')) |
            (User.last_name.ilike(f'%{search}%'))
        )
    
    # Get all users
    users = query.order_by(User.username).all()
    
    return render_template('admin/roles.html', users=users)

@admin_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            role=form.role.data,
            is_active=form.is_active.data
        )
        # Set a default password (should be changed by user)
        user.set_password('password123')
        
        # Create role-specific record
        if form.role.data == 'teacher':
            teacher = Teacher(user=user)
            db.session.add(teacher)
        elif form.role.data == 'student':
            student = Student(user=user)
            db.session.add(student)
        elif form.role.data == 'admin':
            admin = Admin(user=user)
            db.session.add(admin)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Usuario creado exitosamente', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/user_form.html', form=form, title='Agregar Usuario')

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = UserForm(original_username=user.username, original_email=user.email)
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.is_active = form.is_active.data
        
        # Handle role change if needed
        if user.role != form.role.data:
            # Remove old role
            if user.role == 'teacher' and user.teacher:
                db.session.delete(user.teacher)
            elif user.role == 'student' and user.student:
                db.session.delete(user.student)
            elif user.role == 'admin' and user.admin:
                db.session.delete(user.admin)
            
            # Add new role
            user.role = form.role.data
            if form.role.data == 'teacher':
                teacher = Teacher(user=user)
                db.session.add(teacher)
            elif form.role.data == 'student':
                student = Student(user=user)
                db.session.add(student)
            elif form.role.data == 'admin':
                admin = Admin(user=user)
                db.session.add(admin)
        
        db.session.commit()
        flash('Usuario actualizado exitosamente', 'success')
        return redirect(url_for('admin.users'))
    
    # Pre-populate form
    if request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.role.data = user.role
        form.is_active.data = user.is_active
    
    return render_template('admin/user_form.html', form=form, title='Editar Usuario')

@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    # Don't allow deleting the current user
    if user.id == current_user.id:
        flash('No puedes eliminar tu propio usuario', 'danger')
        return redirect(url_for('admin.users'))
    
    db.session.delete(user)
    db.session.commit()
    
    flash('Usuario eliminado exitosamente', 'success')
    return redirect(url_for('admin.users'))

@admin_bp.route('/reports')
@login_required
def reports():
    # Summary statistics
    stats = {
        'total_activities': Assignment.query.count(),
        'active_users': User.query.filter_by(is_active=True).count(),
        'resources_used': Course.query.count() + Assignment.query.count(),
    }
    
    # Activities per month data (for charts)
    current_year = func.extract('year', Assignment.created_at)
    current_month = func.extract('month', Assignment.created_at)
    
    activities_per_month = db.session.query(
        current_month.label('month'),
        func.count(Assignment.id).label('count')
    ).filter(
        current_year == func.extract('year', func.current_date())
    ).group_by(current_month).order_by(current_month).all()
    
    months_data = [0] * 12  # Initialize with zeros
    for month, count in activities_per_month:
        # Adjust for 0-based indexing
        months_data[int(month) - 1] = count
    
    # Distribution data for pie chart
    distribution_data = {
        'Tareas': Assignment.query.count(),
        'Cursos': Course.query.count(),
        'Estudiantes': Student.query.count(),
        'Profesores': Teacher.query.count()
    }
    
    return render_template(
        'admin/reports.html', 
        stats=stats,
        months_data=months_data,
        distribution_data=distribution_data
    )

@admin_bp.route('/api/users')
@login_required
def api_users():
    """API endpoint to get users data for AJAX requests."""
    users = User.query.all()
    users_data = []
    
    for user in users:
        users_data.append({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify(users_data)
