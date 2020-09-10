from flask import abort,current_app as app
from flask_login import current_user
from .baserepo import BaseRepo
from ...models.db_product import *
from ...models.db_customer import Customer
from ...models.db_user import User
from .productcategory import RepoProductCategory
from .form_product import *
from sqlalchemy import exc,func
import datetime

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
        self.update_sub_form = {'basic':("基本資訊",Update_basic_Form),'category':("目錄",Update_category_Form),
            'variant':("屬性",Update_variant_Form),'sku':("庫存",Update_sku_Form),'image':("圖片",Update_image_Form),
            'article':("文章",Update_article_Form),'active':("上架",Update_active_Form)}
        #異動tables
        #Base.metadata.create_all(app.db_session.engine)
        #異動data
        #self.init_db()
        
        
    def __repr__(self):
        return self.title
        
    def form_mapper(self,db_data):
        form_data = {}
        if self.repo_sub == 'basic':
            form_data = {"name":db_data.name,"sku":db_data.sku,"description":db_data.description,
                "order":db_data.order}
        if self.repo_sub == 'category':
            if db_data.category:
                form_data = {"name":db_data.name,"category":db_data.category.id}
            else:
                form_data = {"category":""}
      
        return self.Struct(**form_data)
        
    def update_form(self,id=None):
        #這裡區分 repo_sub 
        db_item = self.find(id)

        try:    
            form = self.update_sub_form[self.repo_sub][1](obj=db_item) #UpdateForm(obj=db_item)
            if self.repo_sub == 'category':
                prductCategory = RepoProductCategory()
                form.category.choices = form.category.choices + prductCategory.get_tree()
            #raise Exception(db_item.category)    
        except KeyError as e:
            abort(404)
                        
        #if form has any select choices to fill...
        #example:form.roles.choices = self.get_roles()
        
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
  
    def find(self, id=None):
        form_item = None
        if id:
            with app.db_session.session_scope() as session: 
                db_item = session.query(Product).get(id)
                form_item = self.form_mapper(db_item)
        else:
            db_item = Product()
            form_item = self.form_mapper(db_item)
        return form_item

    def update(self,item,id=None):
        #這裡區分 repo_sub 
        
        def update_basic(session,db_item,item):
            db_item.name = item.name
            db_item.sku = item.sku
            db_item.description = item.description
            db_item.order = item.order
            
        def update_category(session,db_item,item):
            category = session.query(ProductCategory).filter(ProductCategory.id==item.category).first()
            db_item.category = category
            
        _sub_update = {"basic":update_basic,"category":update_category}
        
        def strip_link_text(link): #不能有空白
            return "_".join(link.split())
        
        try:
            with app.db_session.session_scope() as session:
                if id and id is not None:
                    db_item = session.query(Product).get(id)
                else:
                    db_item = Product()
                #--- 區分sub處
                
                _sub_update[self.repo_sub](session,db_item,item)
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
    
    #custom function -----
    def _list_details(self,row):
        return {
                'title_field':row.variant, #編輯icon tooltips name
                'fields_value':[
                    row.variant
                    ]
                }
    def get_details(self,id):
        with app.db_session.session_scope() as session:
            product = session.query(Product).filter(Product.id==id).first()
            self.title = f'{self.title}-[{product.name}]'    #多餘 -{self.update_sub_form[self.repo_sub][0]}  
        if self.repo_sub == "variant":
            variants = []
            with app.db_session.session_scope() as session:
                product = session.query(Product).filter(Product.id==id).first()
                #variants = [v for v in product.variants]
                variants = self.get_details_list(id,product.variants)
                #raise Exception(self.get_details_list(product.variants)) 
            return {'fields':['屬性'],
                        'data':variants}  
        
    