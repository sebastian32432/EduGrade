import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from sqlalchemy.orm import DeclarativeBase

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize extensions
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app():
    # Create and configure the app
    app = Flask(__name__)
    
    # Set configuration
    app.config.from_object('config.Config')
    
    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    
    # Set up login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Por favor inicie sesión para acceder a esta página.'
    login_manager.login_message_category = 'warning'
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.teacher import teacher_bp
    from routes.student import student_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(student_bp)
    
    # Create database tables
    with app.app_context():
        # Import models to ensure they're registered with SQLAlchemy
        from models import User, Course, Student, Teacher, Admin, Grade, Assignment
        
        logger.info("Creating database tables...")
        db.create_all()
        logger.info("Database tables created successfully.")
    
    return app
