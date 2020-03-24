#from __main__ import app
from flask import request, render_template, make_response,current_app,g,redirect
from flask_login import current_user,login_required
from datetime import datetime as dt
from .share.models import db
from .models.user import User
from . import login_manager

@current_app.route('/', methods=['GET'])
def test():
    if g.user.is_authenticated:
        return 'it works!TEST_USER:{}'.format(current_user.name)
    else:
        return "not logged in"
    
@current_app.route('/newuser', methods=['GET'])
@login_required
def create_user():
    """Create a user."""

    return "newuser page"
    
@current_app.before_request
def before_request():
    g.user = current_user  
    
@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/auth/login?next=' + request.path)    