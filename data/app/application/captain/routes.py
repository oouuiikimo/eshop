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
                     template_folder='templates',
                     static_folder='statics')
                     
repo_path = 'application.captain.repo'
                     
@captain.route('/', methods=['GET','POST'])
@login_required
def home():   
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
    repo = _repo(repo_name)()
    
    #準備 repo_modelname_search_form       
    searchForm = repo.search_form()

    #if post filter 處理查詢條件,else 回傳空值
    if request.method == 'POST':
        
        session['search'] = {repo_name:{
            i.id: i.data for i in searchForm if i.id is not 'csrf_token' and
            (i.data is not "" and i.data is not None)
            }} 
        return redirect(session['lastURL']) #jsonify(session['search'])
        
    if session['search'][repo_name]:
        search=session['search'][repo_name]
    else:
        search=None
        
    #復原searchForm內容
    if repo_name in session['search'] and session['search'][repo_name]:
        for i in session['search'][repo_name]:
            searchForm[i].data = session['search'][repo_name][i]
    #記住上一頁的位址及頁碼,供post,update取消鍵返回之用
    session['lastURL'] = '/captain/list/{}?page={}&per_page={}'.format(repo_name,int(page),int(per_page))
    #準備資料集
    page,data,count,pagination = repo.get_list(page=page,per_page=per_page,search=search)
    data_to_template = {'page':page,'per_page':per_page,'data':data,'count':count,'pagination':pagination,
        'search_form':searchForm,'repo_name':repo_name,'repo_title':repo.title,'repo_desc':repo.description}
    return render_template('/captain/list.html',**data_to_template)
    
@captain.route('/update/<repo_name>/', defaults={'id': None}, methods=['GET','POST'])    
@captain.route('/update/<repo_name>/<id>', methods=['GET','POST'])
@login_required
def update(repo_name,id):
    repo = _repo(repo_name)()  
    form,item = repo.update_form(id)   
    if request.method == 'POST' and form.validate():
        form.populate_obj(obj=item)
        repo.update(item,id)
        if 'lastURL' in session and session['lastURL'] is not None:
            return redirect(session['lastURL'])
        return redirect(url_for('captain.list',repo_name=repo_name))

    data_to_template = {'form':form,'item':item,'update_type':'{}.{}'.format(repo.title,'新增' if not id else '編輯')}
    return render_template('/captain/update.html',**data_to_template)
    
@captain.route('/delete/<repo_name>', methods=['POST'])
@login_required
def delete(repo_name):
    repo = _repo(repo_name)() 
    remove_items = json.loads(request.form.get('id'))
    lastURL = ""
    if "lastURL" in session:
        lastURL = session['lastURL']
        
    error = repo.delete(remove_items)
    
    if error:
        #raise Exception(error)
        return jsonify({"error":'有錯誤 :{}'.format(error)})
    return jsonify({"success":'己刪除記錄 :{}'.format(remove_items),"redirect":lastURL}) 
    
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