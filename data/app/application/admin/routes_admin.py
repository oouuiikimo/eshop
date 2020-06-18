from flask import Blueprint, render_template,current_app,json,request,redirect, flash, session, url_for,g
from flask_login import login_required
from sqlalchemy.orm import load_only,joinedload,lazyload,outerjoin
from .. import db,login_manager
from ..models.user import User,Roles
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect, FlaskForm
"""
from flask_principal import Principal, Permission, RoleNeed, UserNeed, Identity, AnonymousIdentity, identity_changed, \
    identity_loaded, Denial
from flask_caching import Cache    
from flask_mail import Mail,  Message
"""
# Set up a Blueprint
admin_bp = Blueprint('admin_bp', __name__,
                    url_prefix='/admin',
                     template_folder='templates',
                     static_folder='statics')
                     
@admin_bp.route('/', methods=['GET'])
@login_required
def admin():
    """Admin page route."""
    #user = User.query.filter_by(name='tom').first()
    """
    table_title,fields,rows,pages
    """
    #kwargs = {}
    fields = [('name','名稱'),('email','郵箱'),('active','有效'),('source','來源'),('roles','權限')]
    #rows = User.query.filter_by(**kwargs).options(load_only(*[x[0] for x in fields])).all() .options(load_only(*[x[0] for x in fields]))
    rows = User.query.all()
    out_rows = []
    for row in rows:
        out_rows.append(['<a href="/admin/update/User/{}">{}</a>'.format(row.id,row.name),
            row.email,row.active,row.source,'<a href="/admin/updatemany/{}">{}</a>'.format(row.id,row.roles)])
    #return json.dumps(out_rows)
    data = {'table_title':"User",'fields':fields,'rows':out_rows}
    return render_template('admin.html',**data)
    #return 'admin it works!TEST_USER:{}'.format(current_app.config['TEST_USER'])
    
@admin_bp.route('/update/<model>/<id>', methods=['GET','POST'])
@login_required
def update(model,id):
    from ..admin.forms_admin import UpdateUser
    item = User.query.get(id) #get data
    #return item.name
    #form = get_updateform(data)(obj= item)#data_class.get_form()(obj= item)
    form = UpdateUser(obj= item) 
    #set_choice = data_class.set_choice()
    #if set_choice:
    #    set_form_choices(form,set_choice,item)

    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        #return str(url_for('admin'))
        return redirect(url_for('admin_bp.admin'))
    
    return render_template('update.html', form=form, model=model, id=id) 
    
@admin_bp.route('/updatemany/<id>', methods=["GET"])
def get_user_form(id):
    from ..admin.forms_admin import UserRolesForm
    # ... Get the Person
    user = User()
    if id:
        # ... if userid supplied, use existing Person object
        user = User.query.get(id)

    # ... Populate the form
    person_form = UserRolesForm(obj=user)

    # ... return form
    return render_template('update.html', form=person_form)    