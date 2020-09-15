from flask import abort,current_app as app
from flask_login import current_user
from .baserepo import BaseRepo
from ...models.db_product import *
from ...models.db_customer import Customer
from ...models.db_user import User
from .productcategory import RepoProductCategory
from .form_product import *
from .sub_product import sub_repo
from sqlalchemy import exc,func
import datetime
import os
_path = os.path.dirname(os.path.abspath(__file__))

class RepoProduct(BaseRepo):
    #public function  ----    
    def __init__(self):
        super().__init__()
        self.title = "商品設定"
        self.model = Product
        self.active_menu = "sub_list_product"
        self.description = """
        說明: 商品頁面內文章列表, 請注意, 若有文章刪除, 前台連結將無法顯示文章內容, 更新亦同。
        """
        if self.repo_sub is None:
            self.repo_sub = 'basic'
        self.subRepo = None       
        
    def __repr__(self):
        return self.title
    
    def sub_menu(self,id):
        return sub_repo
        
    def set_subrepo(self,repo_sub,id,detail_id):
        self.repo_sub = repo_sub
        self.subRepo = sub_repo[self.repo_sub]["class"](app,id,detail_id)    
        
    def update_form(self,id=0,detail_id=0):
        #取表單需要的單筆資料,並轉成struct,供表單呈現
        form_data = self.subRepo.form_data()    
        db_item = self.Struct(**form_data)
        #取表單class ,並動態產生choices ,如果有需要
        form = self.subRepo.set_form_choice(db_item)  
        #取需要的js.檔案, 備template使用
        
        try:
            if self.subRepo.update_form_js:
                js = os.path.join(_path,self.subRepo.update_form_js)
                #raise Exception(js)
                with open(js,'r') as jsfile:
                    self.js = jsfile.read()
        except KeyError as e:
            pass
        
        return form,db_item
        
    def search_form(self):
        form = SearchForm()
        #if form has any select choices to fill...
        #form.roles.choices = form.roles.choices + self.get_roles()

        return form

    def _list_rows(self,row):
        return {
                'title_field':row.name, #編輯icon tooltips name
                'fields_value':[
                    row.name,row.sku
                    ]
                }
                
    def _list_fields(self):
        return ['商品名稱','型號']
                   
    def get_search_filters(self,search):
        filters = []
        if search:
            if 'title' in search and search['title']: 
                filters.append(Product.title.like(f'%{search["title"]}%') )   

        return filters

    def update(self,item,id=None):
        
        try:
            with app.db_session.session_scope() as session:
                if id and id is not None:
                    db_item = session.query(Product).get(id)
                else:
                    db_item = Product()
                #--- 區分sub處
                
                self.subRepo.update(session,db_item,item)
                #raise Exception(db_item.category.id)
                #---
                db_item.updated = datetime.datetime.now()
                db_item.updated_by = current_user.email
            
                if not id:
                    db_item.created_by = current_user.email
                    session.add(db_item)
                    
        except exc.SQLAlchemyError as e:
            """ 捕獲錯誤, 否則無法回傳
            """
            if 'orig' in e.__dict__:
                return str(e.__dict__['orig'])
                #raise Exception(str(e.__dict__['orig']))
            return "更新失敗!"    
            #raise Exception('刪除失敗!!')

    def delete(self, items):
    
        def validate_del(session,item):
            #todo:檢查sku,session.query(func.count(User.id)).scalar() 
            sku_count = session.query(func.count(ProductSku.id)).filter(ProductSku.id_product==item.id).scalar() 
            #raise Exception('skus:'+str(skus))
            if sku_count>=1:
                return False
            return True
            
        def after_del(session,item):
            #刪除images,variants
            pass
            
        try:
            """檢查:是否有商品頁引用,不能刪除"""
            #return str(type(items))
            with app.db_session.session_scope() as session:
                for item in items:
                    _del = session.query(Product).filter(Product.id==item).first()
                    if _del:
                        if validate_del(session,_del):
                            #session.delete(_del)
                            after_del(session,_del)
                        else:
                            return "刪除失敗,尚有庫存商品"                        
                
        except exc.SQLAlchemyError as e:
            """ 捕獲錯誤, 否則無法回傳
            """
            if 'orig' in e.__dict__:
                return str(e.__dict__['orig'])
            #raise e
            return '刪除失敗!!'
        return None  
    
    def set_title(self,id=None):
        if id and id >0:
            with app.db_session.session_scope() as session:
                product = session.query(Product).filter(Product.id==id).first()
                self.title = f'{self.title}-[{product.name}]'
                
    #custom function -----        
        
    def get_details(self,id): 
        # 製作details 

        if int(id)==0:
            return
        dic_replace = self.detail_dict() #{"class_name":self.__class__.__name__.replace("Repo",""),
        return self.subRepo.details(dic_replace,self.detail_template)

        
    