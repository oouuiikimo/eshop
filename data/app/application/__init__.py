from flask import Flask
from flask_login import LoginManager

from .share.models import db
# Globally accessible libraries
login_manager = LoginManager()



        
def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    login_manager.init_app(app) #need secretkey
    db.init_app(app)
    with app.app_context():
        """ Include our Routes 
        must after Initialize plugins otherwise you can not import them inside bp
        """

        from . import routes
        from .admin import routes_admin
        from .auth import routes_auth
        from .RichFilemanager.File import bluePrint as fileBluePrint
        # Register Blueprints
        app.register_blueprint(routes_admin.admin_bp)
        app.register_blueprint(routes_auth.auth_bp)
        
        app.register_blueprint(fileBluePrint)
        from .dbcreate import init_db,update_db,test_page,add_articleCategories
        #init_db(db) #,routes_auth.User) 
        #update_db(db) #,routes_auth.User) 
        #test_page(db)
        #add_articleCategories(db)
        return app 