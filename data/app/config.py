"""Flask config class."""
import os


class Config:
    """Set Flask configuration vars."""

    # General Config
    TESTING = True
    DEBUG = True
    SECRET_KEY = b'_5#y2L"F4Q8z\n\oec]/'
    SESSION_COOKIE_NAME = 'my_cookie'

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site1.db' #'postgresql+psycopg2://postgres:ouigugi@postgres:5432/wwwdev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN = 'tom@your-tom.com'
    #BABEL_DEFAULT_LOCALE = 'zh_TW'



