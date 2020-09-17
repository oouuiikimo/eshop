from flask import (Blueprint, render_template,current_app,json,request,redirect,
    flash, session, url_for,g,jsonify,send_file,make_response)
from flask_login import login_required,current_user
from .. import login_manager
from flask_wtf import CSRFProtect, FlaskForm
from .menu import get_menu
from ..store_config import store_config,set_config
from wtforms import ValidationError
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
    return redirect(url_for('captain.list',repo_name='User'))

@captain.route('/test', methods=['GET','POST'])
@login_required
def test():   
    return render_template('/captain/test_btn_group.html')
    
@captain.route('/list/<repo_name>', methods=['GET','POST'])
@login_required
def list(repo_name):
    #return render_template('list.html')
    #定義預設頁數值
    default_per_page = 10
    page = request.args.get('page') or 1
    per_page = request.args.get('per_page') or default_per_page
    sort = request.args.get('sort')
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
        session['sort']=sort
        lastURL = session['lastURL'].pop()
        return redirect(lastURL) #jsonify(session['search'])
    #return jsonify(session['search'])    
    if 'search' in session and session['search'] and repo_name in session['search'] and session['search'][repo_name]:
        search=session['search'][repo_name]
    else:
        search=None
        
    #復原searchForm內容
    if  'search' in session and session['search'] and repo_name in session['search'] and session['search'][repo_name]:
        #session['search']= None
        #return jsonify(session['search'])
        for i in session['search'][repo_name]:
            searchForm[i].data = session['search'][repo_name][i]
    #記住上一頁的位址及頁碼,供post,update取消鍵返回之用
    session['lastURL'] = ['/captain/list/{}?page={}&per_page={}'.format(repo_name,int(page),int(per_page))]
    #準備資料集
    page,data,count,pagination = repo.get_list(page=page,per_page=per_page,search=search,sort=sort)
    data_to_template = {'page':page,'per_page':per_page,'data':data,'count':count,'pagination':pagination,
        'search_form':searchForm,'repo_name':repo_name,'repo_title':repo.title,'repo_desc':repo.description,
        "active_menu":repo.active_menu,'sort':sort,"store":current_app.store_config}
    return render_template('/captain/list.html',**data_to_template)
    
#new repo item. if has repo_sub then show default sub form    
@captain.route('/update/<repo_request>', defaults={'id': None}, methods=['GET','POST'])    
#if has repo_sub then show default sub form
@captain.route('/update/<repo_request>/<id>', methods=['GET','POST'])
@login_required
def update(repo_request,id):
    repo_name = repo_request
    repo = _repo(repo_name)()  
    #處理複雜的次操作,轉到update_sub
    
    if repo.repo_sub:
        if not id:
            id=0
        return redirect(url_for('captain.update_sub',repo_request=repo_request,id=id,repo_sub=repo.repo_sub))
    
    form,item = repo.update_form(id)  
    #return str(item) #form.validate())  
    if request.method == 'POST' and form.validate():
        #return "OK"
        form.populate_obj(obj=item)
        error = repo.update(item,id) #可以返回依 repo_sub 值有不同的update
        if error:
            flash(error)
            #raise ValidationError(error)
        else:    
            if 'lastURL' in session and session['lastURL'] is not None:
                return redirect(session['lastURL'].pop())
            return redirect(url_for('captain.list',repo_name=repo_name))

    data_to_template = {'form':form,'item':item,'update_type':'{}.{}'.format(repo.title,'新增' if not id else '編輯'),
        "active_menu":repo.active_menu,"store":current_app.store_config}

    return render_template('/captain/update.html',**data_to_template)
    
#show details list or form for update
@captain.route('/update/<repo_request>/<id>/<repo_sub>',defaults={'detail_id':None}, methods=['GET','POST'])
#edit details item form
@captain.route('/update/<repo_request>/<id>/<repo_sub>/<detail_id>', methods=['GET','POST'])
@login_required
def update_sub(repo_request,id,repo_sub,detail_id):
    repo_name = repo_request#repo_split[0]
    repo = _repo(repo_name)() 
    repo.set_subrepo(repo_sub,id,detail_id)
    repo.set_title(int(id))
    
    details = repo.get_details(id)
    form = []
    
    #show form only when no details or has detail_id
    #if detail_id form must have detail_id
    if not details or detail_id :
        form,item = repo.update_form(id,detail_id)
        details = [] #don't show list when edit form
        if detail_id:
            #push lastURL
            session['lastURL'].append(f'/captain/update/{repo_request}/{id}/{repo_sub}')
            #return jsonify(session['lastURL'])
    
        if request.method == 'POST' and form.validate():
            #return "OK"
            form.populate_obj(obj=item)
            result = repo.update(item,id) #可以返回依 repo_sub 值有不同的update
            try: 
                _id = int(result) #redirect 到新id頁
                if detail_id and 'lastURL' in session and session['lastURL'] is not None:
                    return redirect(session['lastURL'].pop())
                return redirect(url_for('captain.update_sub',repo_request=repo_request,id=_id,
                    repo_sub=repo_sub,detail_id=detail_id))
            except ValueError:
                flash(result)                
    
    data_to_template = {'form':form,'update_type':'{}.{}'.format(repo.title,'新增' if not id else '編輯'),
        "active_menu":repo.active_menu,"store":current_app.store_config,
        "sub_menu":repo.sub_menu(id),"details":details,
        "repo_name":repo_name,"repo_sub":repo.repo_sub,"id":id,"detail_id":detail_id,
        "js":repo.js if repo.js else ""}
    return render_template('/captain/sub_update.html',**data_to_template)
    
@captain.route('/delete/<repo_name>', methods=['POST'])
@login_required
def delete(repo_name):
    repo = _repo(repo_name)() 
    remove_items = json.loads(request.form.get('id'))
    if remove_items is None or len(remove_items)==0:
        return jsonify({"error":'有錯誤 :{}'.format("沒有可刪除的項目!")})
    lastURL = ""
    if "lastURL" in session and len(session['lastURL']):
        lastURL = session['lastURL'][-1]
        
    error = repo.delete(remove_items)
    
    if error:
        #raise Exception(error)
        return jsonify({"error":'有錯誤 :{}'.format(error)})
    return jsonify({"success":'己刪除記錄 :{}'.format(remove_items),"redirect":lastURL}) 

@captain.route('/delete/<repo_name>/<id>/<repo_sub>', methods=['POST'])
@login_required
def delete_sub(repo_name,id,repo_sub):
    repo = _repo(repo_name)() 
    repo.repo_sub = repo_sub
    repo.set_subrepo(repo_sub,id,0)
    remove_items = json.loads(request.form.get('id'))
    if remove_items is None or len(remove_items)==0:
        return jsonify({"error":'有錯誤 :{}'.format("沒有可刪除的項目!")})
    lastURL = ""
    if "lastURL" in session and len(session['lastURL']):
        lastURL = session['lastURL'][-1]
    #return jsonify({"success":"OK"})
    error = repo.delete_details(id,remove_items)
    
    if error:
        #raise Exception(error)
        return jsonify({"error":'有錯誤 :{}'.format(error)})
    return jsonify({"success":'己刪除記錄 :{}'.format(remove_items),"redirect":lastURL}) 
    
@captain.route('/account_setting', methods=['GET','POST'])
@login_required
def account_setting():  
    data_to_template = {"active_menu":"sub_account_setting","store":current_app.store_config}
    if request.method == 'POST':
        import base64
        repo = _repo('User')() 
        binary_photo = base64.b64decode(request.form.get('photo'))
        repo.update_photo(current_user.id,binary_photo)
        #with open('test_1.jpg','wb') as _file:
        #    _file.write(base64.b64decode(request.form.get('photo')))
        return jsonify({"success":"OK"})    
        
    return render_template('/captain/account_setting.html',**data_to_template)

@captain.route('/get_photo/<id>', methods=['GET'])
@login_required
def get_photo(id): 
    
    repo = _repo('User')() 
    _photo = repo.get_photo(id)
    #with open('test_2.jpg', 'wb') as file:
    #    file.write(_photo)
    response = make_response(_photo)
    response.headers.set('Content-Type', 'image/png')

    return response

    
@captain.route('/store_setting', methods=['GET'])
@login_required
def store_setting():  
    store = current_app.store_config #store_config(False)
    
    data_to_template = {"active_menu":"sub_store_setting","store":current_app.store_config}
    return render_template('/captain/store_setting.html',**data_to_template)

@captain.route('/product_setting', methods=['GET'])
@login_required
def product_setting():  
    store = current_app.store_config #store_config(False)
    
    data_to_template = {"active_menu":"sub_product_setting","store":current_app.store_config}
    return render_template('/captain/product_setting.html',**data_to_template)
    
@captain.route('/image', methods=['GET'])
@login_required
def image():  
    store = current_app.store_config #store_config(False)
    
    data_to_template = {"active_menu":"image_manager","store":current_app.store_config}
    return render_template('/captain/image.html',**data_to_template)

@captain.route('/zm', methods=['GET'])
@login_required
def zm(): 
    return render_template('/captain/zm.html')   
def _repo(name):
    import importlib
    
    def _class(_package,_module):

        module = importlib.import_module('{}.{}'.format(repo_path,_package.lower()))
        return getattr(module, _module)
        
    def _get_repo(model):
        _package = model #實體檔案 {}.py
        _module = 'Repo{}'.format(model) #檔案內class 名稱 ,第一個字大寫
        return _class(_package,_module)
                
    return _get_repo(name)