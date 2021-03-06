#from __main__ import app
from flask import request, render_template, make_response,current_app,redirect, flash, session, url_for,g
from flask_login import current_user,login_required
from datetime import datetime as dt
from . import login_manager

@current_app.route('/', methods=['GET'])
def home():
    return redirect(url_for('captain.home'))
    return redirect(url_for('admin_bp.home'))
    return redirect(url_for('admin_bp.admin',model='User'))
    
@current_app.route('/newuser', methods=['GET'])
@login_required
def create_user():
    """Create a user."""

    return "newuser page"
    
@current_app.before_request
def before_request():
    if current_user.is_authenticated:
        g.user = current_user

    
@login_manager.unauthorized_handler
def unauthorized_callback(): 
    return redirect('/auth/login?next=' + request.path)    
    
