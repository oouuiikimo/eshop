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
        from .admin import routes as admin_routes
        from .auth import routes as auth_routes
        # Register Blueprints
        app.register_blueprint(admin_routes.admin_bp)
        app.register_blueprint(auth_routes.auth_bp)

        return app