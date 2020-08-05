from flask import (Blueprint, render_template,current_app,json,request,redirect,
    flash, session, url_for,g,jsonify)
from flask_login import login_required
from flask_wtf import CSRFProtect, FlaskForm
from flask_caching import Cache
"""
from flask_principal import Principal, Permission, RoleNeed, UserNeed, Identity, AnonymousIdentity, identity_changed, \
    identity_loaded, Denial
"""

# Set up a Blueprint
shop = Blueprint('shop', __name__,
                    url_prefix='/shop',
                     template_folder='templates',
                     static_folder='assets')
                     
repo_path = 'application.shop.repo'
                     
@shop.route('/', methods=['GET','POST'])
@login_required
def home():   
    return redirect(url_for('shop.cart'),repo='cart')
    
@shop.route('/cart/<repo_name>', methods=['GET','POST'])
@login_required
def cart(repo_name): 
    """
    try:
        repo = _repo('cart',repo_name)()    
    except:
        return render_template('404.html'), 404
    """    
    
    repo = _repo('cart',repo_name)()   
    #repo 傳送post,ajax
    if request.method== 'POST':    
        _is_ajax = bool(request.args.get('ajax'))
        _post_action = request.args.get('action')
        #呼叫repo 內的 action 動作, 並回傳
        if not _post_action:
            return None
        result = repo.post(_post_action) #{"success":"OK"}
        if _is_ajax:
            return jsonify(result)
        if 'error' in result: 
            return None
        return redirect(url_for('shop.cart',repo_name='list'))
        
    #共通頁面資訊
    data_public = {'wishcount':5}
    #repo 頁面資訊
    data_repo = repo.data
    #結合資訊
    data_to_template = {**data_public, **data_repo}
    #return jsonify(data_to_template)
    return render_template(repo.template,**data_to_template)

@shop.route('/article/<article_name>', methods=['GET','POST'])
@login_required
def article(article_name): 

    def _get_article(article_name):
        pass
        
    try:
        repo = _get_article(article_name)()
    except:
        return render_template('404.html'), 404
     
    data_to_template = {'wishcount':5}
    return render_template('/shop/article.html', **data_to_template)

@shop.route('/member/<repo_name>', methods=['GET','POST'])
@login_required
def member(repo_name): 
    try:
        repo = _repo('member_{}'.format(repo_name))()
    except:
        return render_template('404.html'), 404
     
    data_to_template = {'wishcount':5}
    return render_template('/shop/member.html', **data_to_template)
    
def _repo(pre,name):
    import importlib
    
    def _class(_package,_module):

        module = importlib.import_module('{}.{}'.format(repo_path,_package))
        return getattr(module, _module)
        
    def _get_repo(_pre,module):
        _package = '{}_{}'.format(_pre,module) #實體檔案 {}.py
        _capitalize_module_name = '{}{}'.format(_pre.capitalize(),module.capitalize())
        #檔案內class 名稱 ,第一個字大寫
        return _class(_package,_capitalize_module_name)
                
    return _get_repo(pre,name)