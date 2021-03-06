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
        self.submenu = []
        
    def __repr__(self):
        return self.title
    
    def sub_menu(self,id):
        if int(id)>0:
            with app.db_session.session_scope() as session: 
                #若isvariant = false ,不顯示屬性頁簽,並禁止進入該頁簽
                #raise Exception(sub_repo)
                if not self.subRepo.parent(session).isvariant:
                    self.submenu = {key:value for (key,value) in sub_repo.items() if key is not 'variant'}
                else:
                    self.submenu = sub_repo
            
        #id若為0表示新增, 只能出現basic先供存檔, 再補其它    
        else:
            self.submenu = {"basic":sub_repo["basic"]}    
        
    def set_subrepo(self,repo_sub,id,detail_id):
        #檢查menu是否有該repo_sub, 若無或被禁止, 則回應錯誤或導向
        self.repo_sub = repo_sub
        self.subRepo = sub_repo[self.repo_sub]["class"](app,id,detail_id) 
        self.sub_menu(id)
        if repo_sub not in self.submenu:
            self.repo_sub = "basic"
            
           
        self.set_title(int(id))
        
    def update_form(self,id=0,detail_id=0):
        #取表單需要的單筆資料,並轉成struct,供表單呈現
        form_data = self.subRepo.form_data()    
        db_item = self.Struct(**form_data)
        #取表單class ,並動態產生choices ,如果有需要
        form = self.subRepo.prepare_form(db_item)  
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
            if 'name' in search and search['name']: 
                filters.append(Product.name.like(f'%{search["name"]}%') )   

        return filters

    def update(self,item,id=None):
        
        try:
            with app.db_session.session_scope() as session:
                if id and int(id)>0:
                    db_item = session.query(Product).get(id)
                else:
                    db_item = Product()
                #--- 區分sub處
                
                self.subRepo.update(session,db_item,item)
                #raise Exception("repo_sub update")
                #---
                db_item.updated = datetime.datetime.now()
                db_item.updated_by = current_user.email
            
                if int(id)==0:
                    db_item.created_by = current_user.email
                session.add(db_item)
                session.commit()
                return db_item.id #回傳更新的id
                    
        except exc.SQLAlchemyError as e:
            """ 捕獲錯誤, 否則無法回傳
            """
            if 'orig' in e.__dict__:
                return str(e.__dict__['orig'])
                #raise Exception(str(e.__dict__['orig']))
            return "更新失敗!"    
        except Exception as e: 
            return str(e)
            raise Exception(str(e))

    def delete(self,items):
        """
        刪除 product, 不是details
        """
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
    
    def delete_details(self,product_id,dels):
        """
        id = product.id
        items = details.id
        """
        #raise Exception(self.repo_sub)
        try:
            with app.db_session.session_scope() as session:
                if product_id and int(product_id)>0:
                    db_item = session.query(Product).get(product_id)
                else:
                    return "查無商品"
                #--- 區分sub處
                self.subRepo.delete(session,db_item,dels)
                #---
                db_item.updated = datetime.datetime.now()
                db_item.updated_by = current_user.email

                session.add(db_item)
                    
        except exc.SQLAlchemyError as e:
            """ 捕獲錯誤, 否則無法回傳
            """
            if 'orig' in e.__dict__:
                return str(e.__dict__['orig'])
                #raise Exception(str(e.__dict__['orig']))
            return f"更新失敗!{e}" 
            raise e
        except Exception as e: 
            return str(e)
            #raise Exception(str(e))
        
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
        dict_replace = self.detail_dict() #{"class_name":self.__class__.__name__.replace("Repo",""),
        #處理details 每行的編輯欄位, 上面在baserepo, 下面丟給sub_repo處理
        return self.subRepo.details(dict_replace,self.detail_template)

        
    