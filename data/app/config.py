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
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/user/data/app/application/site1.db' #'postgresql+psycopg2://postgres:ouigugi@postgres:5432/wwwdev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN = 'tom@your-tom.com'
    #BABEL_DEFAULT_LOCALE = 'zh_TW'
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = 'tom@your-tom.com',
    MAIL_PASSWORD = '6ouigugI'
    CACHE = {'CACHE_TYPE': 'filesystem','CACHE_DIR':'cache','CACHE_DEFAULT_TIMEOUT':300}



