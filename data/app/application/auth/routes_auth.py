"""Routes for user authentication."""
from flask import Blueprint, render_template, request,redirect, flash, session, url_for,g,jsonify
from flask_login import login_required,logout_user, current_user, login_user
from flask import current_app as app
from .forms import LoginForm, SignupForm
from .. import db,login_manager
#from ..models.user import User
from ..models.db_user import User
from .user_login import UserLogin
from .callback_google import callback_google,get_google_provider_cfg

# Blueprint Configuration
auth_bp = Blueprint('auth_bp', __name__,
                    url_prefix='/auth',
                    template_folder='templates',
                    static_folder='statics')
#compile_auth_assets(app)

@auth_bp.route('/login/fb', methods=['GET', 'POST'])
def login_fb():
    return render_template('auth/fb.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login page.

    GET: Serve Log-in page.
    POST: If form is valid and new user creation succeeds, redirect user to the logged-in homepage.
    """
    #raise Exception(current_user)
    with app.db_session.session_scope() as session: 
        if current_user.is_authenticated:
            
            return redirect(url_for('captain.home'))
            return "you're logged in:{}".format("OK")  # Bypass if user is logged in

        login_form = LoginForm()
        if request.method == 'POST':
            if login_form.validate_on_submit():
                email = login_form.email.data
                password = login_form.password.data
                user = session.query(User).filter_by(email=email,active=True).first()
                if user and user.check_password(password=password):
                    login = UserLogin(user)
                    login_user(login)
                    user.login() # update last_login time
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('captain.home'))
            else:
                flash(login_form.errors)          
            flash('Invalid username/password combination')
            return redirect(url_for('captain.home'))

        return render_template('auth/login.html',
                               form=login_form,
                               title='Log in.',
                               template='login-page', next=request.args.get('next') or '',
                               body="Log in with your User account.")
                               
@auth_bp.route('/login/g/<type>', methods=['GET', 'POST'])
def login_google(type):
    from .callback_google import client
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    #request.base_url + "/callback",
    #4 type: user_login,customer_login,register_user,register_customer
    _callback = url_for('auth_bp.callback',
        _external=True,
        _scheme='https',
        social='g',
        type = type)
    #return str(request.base_url + "/callback")    
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=_callback,
        scope=["openid", "email", "profile"],
    )
    #return request_uri
    #process:find db if user exist then redirect to homepage or nextURL
    return redirect(request_uri)
    
@auth_bp.route('/login/f', methods=['GET', 'POST'])
def login_facebook():
    pass
    
@auth_bp.route('/login/t', methods=['GET', 'POST'])
def login_twitter():
    pass

@auth_bp.route("/callback/<social>/<type>",endpoint= "callback")
def callback(social,type):
    if social == 'g':
        return jsonify({'{}-{}:'.format(social,type):callback_google(request,type)})
  

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

    with app.db_session.session_scope() as session: 
        signup_form = SignupForm()
        if request.method == 'POST':
            if signup_form.validate_on_submit():
                name = signup_form.name.data
                email = signup_form.email.data
                password = signup_form.password.data
                existing_user = session.query(User).filter_by(email=email).first()
                if existing_user is None:
                    user = User(name=name,
                                email=email)
                    user.set_password(password)
                    user.source = 'local'
                    user.active = True
                    session.add(user)
                    session.commit()  # Create new user
                    login = UserLogin(user)
                    login_user(login)
                    next_page = request.args.get('next')
                    return redirect(next_page or url_for('captain.home'))
                    
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
def load_user(id):
    """ 回應 current_user.is_authenticated"""
    return UserLogin.get_user(id)
    """
    with app.db_session.session_scope() as session:     
        try:
            #return User.query.get(user_id)
            return session.query(User).get(user_id)
        except:
            return None   
    """

def redirect_dest(home):
    """ 處理未登入前的目的網址,在登入成功時轉址 """
    return redirect(request.args.get('next') or url_for(home))
    
@login_manager.unauthorized_handler
def handle_needs_login():
    flash("You have to be logged in to access this page.")
    #instead of using request.path to prevent Open Redirect Vulnerability 
    next=url_for(request.endpoint,**request.view_args)
    return redirect(url_for('auth_bp.login', next=next))
      