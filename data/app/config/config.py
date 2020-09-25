"""Flask config class."""
import os


class Config:
    """Set Flask configuration vars."""

    # General Config
    TESTING = True
    DEBUG = True
    SECRET_KEY = b''
    SESSION_COOKIE_NAME = 'my_cookie'

    # Database
    SQLALCHEMY_DATABASE_URI = 'sqlite:////home/user/data/app/application/site1.db' #'postgresql+psycopg2://postgres:ouigugi@postgres:5432/wwwdev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN = ''
    #BABEL_DEFAULT_LOCALE = 'zh_TW'
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME = '',
    MAIL_PASSWORD = ''
    CACHE = {'CACHE_TYPE': 'filesystem','CACHE_DIR':'cache','CACHE_DEFAULT_TIMEOUT':300}
    #google
    GOOGLE_CLIENT_ID = ''
    GOOGLE_CLIENT_SECRET = ''
    GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
    EXPLAIN_TEMPLATE_LOADING = False



