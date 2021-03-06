from flask import Flask,render_template
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_caching import Cache 
from flask_mail import Mail,  Message
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal, Permission, RoleNeed, UserNeed, Identity, AnonymousIdentity, identity_changed, \
    identity_loaded, Denial
from .models.database import DB_SESSION  
from .store_config import store_config  
import os
# Globally accessible libraries

#db = SQLAlchemy()
login_manager = LoginManager()     
script_dir = os.path.dirname(os.path.realpath('__file__'))   

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.config.Config')
    app.store_config = store_config()
    # Initialize Plugins
    #store_config.from_object(store_config.py)
    login_manager.init_app(app) #need secretkey
    #db = SQLAlchemy()
    #db.init_app(app)
    csrf = CSRFProtect()
    csrf.init_app(app)
    mail = Mail(app)
    cache = Cache(config=app.config['CACHE'])
    cache.init_app(app)
    app.db_session = DB_SESSION(app.config["SQLALCHEMY_DATABASE_URI"])
    
    with app.app_context():
        """ Include our Routes 
        must after Initialize plugins otherwise you can not import them inside bp
        """

        from . import routes
        from .admin import routes_admin
        from .auth import routes_auth
        from .captain import routes as routes_captain
        from .RichFilemanager.File import bluePrint as fileBluePrint
        from .shop import routes_shop
        # Register Blueprints
        app.register_blueprint(routes_admin.admin_bp)
        app.register_blueprint(routes_auth.auth_bp)
        app.register_blueprint(routes_captain.captain)
        app.register_blueprint(fileBluePrint)
        app.register_blueprint(routes_shop.shop)
        app.register_error_handler(404, page_not_found)
        return app 
        

def page_not_found(error):
   return render_template('404.html', title = '404'), 404