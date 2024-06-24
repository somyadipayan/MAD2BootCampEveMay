import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gocerystore.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'veryverysecretkey'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    CELERY_BROKER_URL = 'redis://localhost:6379/1'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/2'
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 1025