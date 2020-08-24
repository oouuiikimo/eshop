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
    #google
    GOOGLE_CLIENT_ID = '459227710478-741udk5m52ed4jdtrl3h4upbsar4fpe4.apps.googleusercontent.com'
    GOOGLE_CLIENT_SECRET = 'NPyEdkGa7cmPyMyY-gZwg_cS'
    GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
    EXPLAIN_TEMPLATE_LOADING = False


