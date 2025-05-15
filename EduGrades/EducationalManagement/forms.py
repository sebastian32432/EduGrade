from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField, FloatField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from models import User

class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember_me = BooleanField('Recordarme')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    first_name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    password_confirm = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Rol', choices=[('student', 'Estudiante'), ('teacher', 'Profesor'), ('admin', 'Administrador')])
    submit = SubmitField('Registrar')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('El nombre de usuario ya existe. Por favor, elija otro.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Este correo electrónico ya está registrado. Por favor, use otro.')

class CourseForm(FlaskForm):
    name = StringField('Nombre del Curso', validators=[DataRequired(), Length(max=100)])
    code = StringField('Código del Curso', validators=[DataRequired(), Length(max=20)])
    description = TextAreaField('Descripción', validators=[Optional()])
    submit = SubmitField('Guardar Curso')

class AssignmentForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Descripción', validators=[Optional()])
    max_points = FloatField('Puntos Máximos', validators=[DataRequired()])
    submit = SubmitField('Guardar Asignación')

class GradeForm(FlaskForm):
    score = FloatField('Calificación', validators=[DataRequired()])
    comments = TextAreaField('Comentarios', validators=[Optional()])
    submit = SubmitField('Guardar Calificación')

class UserForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    first_name = StringField('Nombre', validators=[DataRequired(), Length(max=64)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(max=64)])
    role = SelectField('Rol', choices=[('student', 'Estudiante'), ('teacher', 'Profesor'), ('admin', 'Administrador')])
    is_active = BooleanField('Activo')
    submit = SubmitField('Guardar Usuario')
    
    def __init__(self, original_username=None, original_email=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email
    
    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('El nombre de usuario ya existe. Por favor, elija otro.')
    
    def validate_email(self, email):
        if email.data != self.original_email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Este correo electrónico ya está registrado. Por favor, use otro.')
