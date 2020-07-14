from flask import Blueprint, render_template,current_app,json,request,redirect, flash, session, url_for,g
from flask_login import login_required
from sqlalchemy.orm import load_only,joinedload,lazyload,outerjoin
from .. import db,login_manager
from ..models.user import User,Roles
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect, FlaskForm
from ..share.formhelp import flash_errors
from ..admin.forms_admin import mapUpdateForm,mapSearchForm
from ..admin.menu_admin import get_menu
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
                     
@admin_bp.route('/', methods=['GET','POST'])
def home():
    return redirect(url_for('admin_bp.admin',model='User',menu='Accounts'))

@admin_bp.route('/<menu>/<model>', methods=['GET','POST'])
@login_required
def admin(menu,model):
    """Admin page route."""
    page = request.args.get('page') or 1
    per_page = request.args.get('per_page') or 10
    #return page
    #kwargs = {}
    formName,formClass = mapUpdateForm(model)
    searchForm = mapSearchForm(model)
    fields = formClass.get_fields() 
    if request.method == 'POST':
        search=searchForm()
    else:
        search=None
    rows,pagination = formClass.get_list(page=page,per_page=per_page,search=search)
    data = {'model':model,'fields':fields,'rows':rows,'menulist':get_menu(menu,model),
        'pagination':pagination,'menu':menu,'formName':formName,
        'searchform':searchForm(),'debug':searchForm(),'page':int(page),'per_page':int(per_page)}
    #return str(type(searchForm().roles.data))
    return render_template('admin.html',**data)

@admin_bp.route('/search/<model>', methods=['POST'])
@login_required
def search(model):
    form = mapSearchForm(model)()
    
    _print = ''
    if not form.validate():    
        _print = 'form is {} validate</br>'.format(form.validate())
        for item in form:
            _print = _print + '{}:{}</br>'.format(item.name,item.data)
        
        for item in form:
            if item.errors:
                for error in item.errors:
                    _print = _print + '{}:{}</br>'.format(item.id,error)
        return str(_print) #redirect(url_for('admin_bp.admin',model=model,activelink='admin.{}'.format(model)))
    else:
        #flash_errors(form)
        for item in form:
            if item.errors:
                for error in item.errors:
                    _print = _print + '{}:{}</br>'.format(item.id,error)
    return str(_print)
    
@admin_bp.route('/insert/<menu>/<model>', methods=['GET','POST'])
@login_required
def insert(menu,model):
    
    formName,formClass = mapUpdateForm(model)
    form,item,layout = formClass.get_form() 
    
    if request.method == 'POST':
        if form.validate():           
            #form.populate_obj(item)
            formClass.insert_data(form,item)
            
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('admin_bp.admin',model=model,menu=menu))
        else:
            flash_errors(form)

    return render_template(formClass.get_template(), form=form, formName=formName,formaction='/admin/insert/{}/{}'.format(menu,model),
        model=model,menulist=get_menu(menu,model), menu=menu, layout=layout)     
    
@admin_bp.route('/update/<menu>/<model>/<id>', methods=['GET','POST'])
@login_required
def update(menu,model,id):
    #return str(g.user.email)
    formName,formClass = mapUpdateForm(model,id)
    form,item,layout = formClass.get_form(id) 
    
    if request.method == 'POST':
        if form.validate():           
            #form.populate_obj(item)
            try:
                formClass.update_data(form,item)
                return redirect(url_for('admin_bp.admin',model=model,menu=menu))
            except Exception as e:
                flash(str(e), 'error')
        else:
            flash_errors(form)

    return render_template(formClass.get_template(), form=form, formName=formName,formaction='/admin/update/{}/{}/{}'.format(menu,model,id),
        model=model, id=id,menu=menu,menulist=get_menu(menu,model), layout=layout) 

@admin_bp.route('/delete/<menu>/<model>/<id>', methods=['GET','POST'])
@login_required
def delete(menu,model,id):
    #todo:顯示此筆資料,讓使用者確認刪除
    return id
    
@admin_bp.route('/Trumbowyg', methods=['GET'])
@login_required
def Trumbowyg():
    return render_template('editor.html',activelink='{}.{}'.format('Tests','Trumbowyg'),menu=get_menu())
    
@admin_bp.route('/ckeditor', methods=['GET'])
@login_required
def ckeditor():
    return render_template('ckeditor.html',activelink='{}.{}'.format('Tests','ckeditor'),menu=get_menu())

@admin_bp.route('/test', methods=['GET'])
@login_required  
def test():
    from ..models.product import ArticleCategory
    return str(ArticleCategory.get_tree())#render_template('ckeditor.html')
