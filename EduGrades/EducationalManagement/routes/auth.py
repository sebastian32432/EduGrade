from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from urllib.parse import urlparse

from app import db
from models import User
from forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to appropriate dashboard
    if current_user.is_authenticated:
        return redirect_based_on_role(current_user.role)
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Usuario o contraseña incorrectos', 'danger')
            return render_template('login.html', form=form)
        
        # Log in the user
        login_user(user, remember=form.remember_me.data)
        
        # Redirect to the appropriate dashboard based on role
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = redirect_based_on_role(user.role)
            
        return redirect(next_page)
    
    # Renderizamos la nueva plantilla de login
    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'info')
    return redirect(url_for('auth.login'))

# Eliminamos la ruta de registro ya que solo queremos el login

def redirect_based_on_role(role):
    if role == 'admin':
        return url_for('admin.dashboard')
    elif role == 'teacher':
        return url_for('teacher.dashboard')
    elif role == 'student':
        return url_for('student.dashboard')
    else:
        # Default fallback
        return url_for('auth.login')
