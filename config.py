import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-sayam-todiy')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///todiy.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
