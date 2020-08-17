from flask import Blueprint, render_template,current_app,json,request,redirect, flash, session, url_for,g,jsonify
from flask_login import login_required,current_user
from sqlalchemy.orm import load_only,joinedload,lazyload,outerjoin
from .. import login_manager
from ..models.user import User,Roles
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect, FlaskForm
from ..share.formhelp import flash_errors
from ..admin.forms_admin import mapUpdateForm,mapSearchForm,mapDeleteForm
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
@login_required
def home():
    #return str(current_user)
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
    page,rows,pagination = formClass.get_list(page=page,per_page=per_page,search=search)
    data = {'model':model,'fields':fields,'rows':rows,'menulist':get_menu(menu,model),
        'pagination':pagination,'menu':menu,'formName':formName,
        'searchform':searchForm(),'debug':searchForm(),'page':int(page),'per_page':int(per_page)}
    #return str(type(searchForm().roles.data))
    #todo:store last page url to session['lastURL'] = '/admin/{}/{}?page={}&per_page={}'.format(menu,model,int(page),int(per_page))
    session['lastURL'] = '/admin/{}/{}?page={}&per_page={}'.format(menu,model,int(page),int(per_page))
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
            try:
                formClass.insert_data(form,item)
            
            #db.session.add(item)
            #db.session.commit()
                if 'lastURL' in session and session['lastURL'] is not None:
                    return redirect(session['lastURL'])
                return redirect(url_for('admin_bp.admin',model=model,menu=menu))
            except Exception as e:
                flash(str(e), 'error')
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
                if 'lastURL' in session and session['lastURL'] is not None:
                    return redirect(session['lastURL'])
                return redirect(url_for('admin_bp.admin',model=model,menu=menu))
            except Exception as e:
                flash(str(e), 'error')
        else:
            flash_errors(form)

    return render_template(formClass.get_template(), form=form, formName=formName,formaction='/admin/update/{}/{}/{}'.format(menu,model,id),
        model=model, id=id,menu=menu,menulist=get_menu(menu,model), layout=layout) 

@admin_bp.route('/delete/<menu>/<model>', methods=['POST'])
@login_required
def delete(menu,model):
    #todo:顯示此筆資料,讓使用者確認刪除
    remove_items = request.form.get('id')
    lastURL = ""
    if "lastURL" in session:
        lastURL = session['lastURL']

    deleteClass = mapDeleteForm(model)
    error = deleteClass.delete_data(remove_items)
    if error:
        return jsonify({"error":'有錯誤 :{}'.format(error)})
    return jsonify({"success":'己刪除記錄 :{}'.format(remove_items),"redirect":lastURL}) 
    #'deleted : {},redirect:{}'.format(remove_items,session['lastURL'])

    
@admin_bp.route('/Trumbowyg', methods=['GET'])
@login_required
def Trumbowyg():
    return render_template('editor.html',activelink='{}.{}'.format('Tests','Trumbowyg'),menulist=get_menu())

@admin_bp.route('/editUser/<int:post_id>', methods=['GET','POST'])    
def editUser(post_id):
    from ..admin.f_user import UserForm
    from ..admin.m_user import PostRepo,Roles,User,user_roles
    import importlib
    
    def _class(_package,_module):

        #module = importlib.import_module(_package)
        module = importlib.import_module('application.admin.repo.{}'.format(_package))
        return getattr(module, _module)
        
    def _get_repo(model):
        _package = model #實體檔案
        _module = model.capitalize() #檔案內class 名稱
        return _class(_package,_module)

        
            
    repo = _get_repo("user")
    return str(repo())
    """
    1.引用class,依model type 
    2.查詢或回傳model及form
    3.POST 處理update,insert,delete
    4.回傳或轉頁
    """
    
    
    post_repo = PostRepo()
    post = post_repo.find(post_id)
    
    form = UserForm(obj=post)
    form.roles.choices = post_repo.get_roles()
    
    if request.method == 'POST' and form.validate():
        #return str([str(i.id) for i in post_repo.restore_roles(post)])
        #return str(request.form['roles'])
        roles = post_repo.restore_roles(request.form['roles'])
        #return str(form.roles)
        post.roles = roles #post_repo.restore_roles(form.roles.data)
        post.name = request.form['name']
        #return str(post.roles)
        #form.populate_obj(post) #說明: 這是將form data 放到post , 讓post 取得form 填入的資料
        #做法1:將form.roles.data 轉成 roles 再populate 到 post 
        #return "OK" #jsonify([i.role for i in post_repo.restore_roles(form.roles.data)])
        post_repo.update(post)
        return "fucking OK"
        return redirect(url_for('show_post', post_id=post.id))
    return render_template('posts_edit.html', form=form, post=post)
    
@admin_bp.route('/ckeditor', methods=['GET'])
@login_required
def ckeditor():
    return render_template('ckeditor.html',menulist=get_menu("Tests","ckeditor"),menu="Tests",model="ckeditor")

@admin_bp.route('/test', methods=['GET'])
@login_required  
def test():
    from ..models.product import ArticleCategory
    return str(ArticleCategory.get_tree())#render_template('ckeditor.html')
