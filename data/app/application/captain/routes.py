from flask import (Blueprint, render_template,current_app,json,request,redirect,
    flash, session, url_for,g,jsonify)
from flask_login import login_required,current_user
from .. import login_manager
from flask_wtf import CSRFProtect, FlaskForm
from .menu import get_menu
"""
from flask_principal import Principal, Permission, RoleNeed, UserNeed, Identity, AnonymousIdentity, identity_changed, \
    identity_loaded, Denial
from flask_caching import Cache    
from flask_mail import Mail,  Message
"""

# Set up a Blueprint
captain = Blueprint('captain', __name__,
                    url_prefix='/captain',
                     template_folder='templates/captain',
                     static_folder='statics')
                     
repo_path = 'application.captain.repo'
                     
@captain.route('/', methods=['GET','POST'])
@login_required
def home():
    """
    顯示model 資料列表
    """
   
    return redirect(url_for('captain.list',repo_name='user'))

@captain.route('/list/<repo_name>', methods=['GET','POST'])
@login_required
def list(repo_name):
    #return render_template('list.html')
    #定義預設頁數值
    default_per_page = 10
    page = request.args.get('page') or 1
    per_page = request.args.get('per_page') or default_per_page
    #準備 repo_modelname_list
    repo = _repo("user")()
    
    #準備 repo_modelname_search_form       
    search_form = repo.search_form()
    #if post filter 處理查詢條件,else 回傳空值
    if request.method == 'POST':
        search = search_form
    else:
        search=None
    #準備資料集
    
    page,data,pagination = repo.get_list(page=page,per_page=per_page,search=search)
    """
    data = {'model':model,'fields':fields,'rows':rows,'menulist':get_menu(menu,model),
        'pagination':pagination,'menu':menu,'formName':formName,
        'searchform':searchForm(),'debug':searchForm(),'page':int(page),'per_page':int(per_page)}

    session['lastURL'] = '/captain/{}/{}?page={}&per_page={}'.format(menu,model,int(page),int(per_page)) 
    """
    data_to_template = {'page':page,'data':data,'pagination':pagination}
    return render_template('list.html',**data_to_template)#str(rows)
    
@captain.route('/update/<repo_name>', methods=['GET','POST'])
@login_required
def update(repo_name):
    return str(_repo("user")())
    
@captain.route('/insert/<repo_name>', methods=['GET','POST'])
@login_required
def insert(repo_name):
    return str(_repo("user")())
    
@captain.route('/delete/<repo_name>', methods=['GET','POST'])
@login_required
def delete(repo_name):
    return str(_repo("user")())
    
def filter(repo_name):
    return str(_repo("user")())    
    
def menu(path):    
    """ 
    功能:
    - 回傳整個menu tree (可多層)
    - 回傳某個menu的 完整 tree path ,用 list 表示 ['path1','path2',....]
    說明:
    - 每個menu 名稱必須唯一 , 格式可為: route_name+'_'+repo_name
    
    """
    menu = get_menu()
    
def _repo(name):
    import importlib
    
    def _class(_package,_module):

        module = importlib.import_module('{}.{}'.format(repo_path,_package))
        return getattr(module, _module)
        
    def _get_repo(model):
        _package = model #實體檔案 {}.py
        _module = 'Repo{}'.format(model.capitalize()) #檔案內class 名稱 ,第一個字大寫
        return _class(_package,_module)
                
    return _get_repo(name)