from flask import Blueprint, render_template,current_app


# Set up a Blueprint
admin_bp = Blueprint('admin_bp', __name__,
                    url_prefix='/admin',
                     template_folder='templates',
                     static_folder='statics')
                     
@admin_bp.route('/', methods=['GET'])
def admin():
    """Admin page route."""
    return render_template('admin.html')
    #return 'admin it works!TEST_USER:{}'.format(current_app.config['TEST_USER'])