import os

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SESSION_SECRET', 'dev-secret-key')
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:0503180817@localhost/edugrade')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    
    # Flask-Login configuration
    SESSION_TYPE = 'filesystem'
    
    # Application specific configuration
    APP_NAME = 'EduGrade'
    ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@edugrade.com')
