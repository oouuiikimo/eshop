"""Routes for user authentication."""
from flask import Blueprint, render_template, request,redirect, flash, session, url_for,g
from flask_login import login_required,logout_user, current_user, login_user
from flask import current_app as app
from .forms import LoginForm, SignupForm
from .. import db,login_manager
from ..models.user import User

# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    url_prefix='/auth',
                    template_folder='templates',
                    static_folder='statics')
#compile_auth_assets(app)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page.

    GET: Serve Log-in page.
    POST: If form is valid and new user creation succeeds, redirect user to the logged-in homepage.
    """
    #return str(current_user.is_authenticated)
    if current_user.is_authenticated:
        return "you're logged in:{}".format(g.user.name)  # Bypass if user is logged in

    login_form = LoginForm()
    if request.method == 'POST':
        if login_form.validate_on_submit():
            email = login_form.email.data
            password = login_form.password.data
            #return str(email)
            user = User.query.filter_by(email=email,active=True).first()  # Validate Login Attempt
            if user and user.check_password(password=password):
                login_user(user)
                user.login() # update last_login time
                db.session.commit()
                next_page = request.args.get('next')
                #return 'hello {}.{}'.format(user.name,str(current_user.is_authenticated))
                return redirect(next_page or url_for('admin_bp.admin'))
        else:
            flash(login_form.errors)          
        flash('Invalid username/password combination')
        return redirect(url_for('admin_bp.admin'))

    return render_template('auth/login.html',
                           form=login_form,
                           title='Log in.',
                           template='login-page', next=request.args.get('next') or '',
                           body="Log in with your User account.")

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()

    #for key in ('identity.name', 'identity.auth_type'):
    #    session.pop(key, None)

    #identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for("auth_bp.login"))
    
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    User sign-up page.

    GET: Serve sign-up page.
    POST: If submitted credentials are valid, redirect user to the logged-in homepage.
    """
    #existing_user = User.query.filter(User.name == 'tom').first()
    #return str(existing_user.name)
    signup_form = SignupForm()
    if request.method == 'POST':
        #return str(signup_form.validate_on_submit())
        if signup_form.validate_on_submit():
            name = signup_form.name.data
            email = signup_form.email.data
            password = signup_form.password.data
            #return 'email:{}'.format(email)
            existing_user = User.query.filter_by(email=email).first()  # Check if user exists
            if existing_user is None:
                user = User(name=name,
                            email=email)
                user.set_password(password)
                db.session.add(user)
                db.session.commit()  # Create new user
                login_user(user)  # Log in as newly created user
                return "OK" #redirect(url_for('main_bp.dashboard'), code=400)
            flash('A user already exists with that email address.')
            return redirect(url_for('auth_bp.signup'))
        else:
            flash(signup_form.errors)    

    return render_template('auth/signup.html',
                           title='Create an Account.',
                           form=signup_form,
                           template='signup-page',
                           body="Sign up for a user account.")
                           
@login_manager.user_loader
def load_user(user_id):
    """ 回應 current_user.is_authenticated"""
    try:
        return User.query.get(user_id)
    except:
        return None   

def redirect_dest(home):
    """ 處理未登入前的目的網址,在登入成功時轉址 """
    return redirect(request.args.get('next') or url_for(home))
    
@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    #instead of using request.path to prevent Open Redirect Vulnerability 
    next=url_for(request.endpoint,**request.view_args)
    return redirect(url_for('auth_bp.login', next=next))
      