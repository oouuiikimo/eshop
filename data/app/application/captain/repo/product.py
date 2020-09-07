from flask import abort,current_app as app
from flask_login import current_user
from .baserepo import BaseRepo
from ...models.db_product import Product
from ...models.db_customer import Customer
from ...models.db_user import User
from .form_product import (Update_basic_Form,Update_attribute_Form,Update_category_Form,
    Update_price_Form,Update_image_Form,Update_article_Form,Update_active_Form,SearchForm)
from sqlalchemy import exc
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
        self.update_sub_form = {'basic':("基本資訊",Update_basic_Form),'attribute':("屬性資訊",Update_attribute_Form),
            'category':("目錄歸屬",Update_category_Form),'price':("價格資訊",Update_price_Form),'image':("圖片",Update_image_Form),
            'article':("文章",Update_article_Form),'active':("上架",Update_active_Form)}
        #異動tables
        #Base.metadata.create_all(app.db_session.engine)
        #異動data
        #self.init_db()
        
        
    def __repr__(self):
        return self.title
        
    def form_mapper(self,db_data):
        
        form_data = {"name":db_data.name}
        return self.Struct(**form_data)
        
    def update_form(self,id=None):
        #這裡區分 repo_sub 
        db_item = self.find(id)

        try:    
            form = self.update_sub_form[self.repo_sub][1]() #UpdateForm(obj=db_item)
        except KeyError as e:
            abort(404)
        self.title = f'{self.title}-{self.update_sub_form[self.repo_sub][0]}'    
        #if form has any select choices to fill...
        #example:form.roles.choices = self.get_roles()
        if self.repo_sub == 'attribute':
            self.details = self.details_attribute(id)
        return form,db_item
        
    def search_form(self):
        form = SearchForm()
        #if form has any select choices to fill...
        #form.roles.choices = form.roles.choices + self.get_roles()

        return form

    def _list_rows(self,row):
        return {
                'title_field':row.title,
                'fields_value':[
                    row.title
                    ]
                }
                
    def _list_fields(self):
        return ['文章標題']
                   
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
        def strip_link_text(link): #不能有空白
            return "_".join(link.split())
        
        try:
            with app.db_session.session_scope() as session:
                if id and id is not None:
                    db_item = session.query(Product).get(id)
                else:
                    db_item = Product()
                    
                db_item.title = item.title
                db_item.content = item.content
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
    
        def validate_product_used(session,item):
            if not item.is_leaf:
                return False
            #todo:建立blog repo 後要添加以下程式,檢查是否有文章在此目錄底下
            blog = session.query(Product).filter(Product.id_category==item.id).first()
            if not blog:
                return False
            return True
        try:
            """檢查:是否有商品頁引用,不能刪除"""
            #return str(type(items))
            with self.session as session: 
                for item in items:
                    _del = session.query(Product).filter(Product.id==item).first()
                    if _del:
                        if not validate_product_used(session,_del):
                            #session.delete(_del)
                            pass
                        else:
                            return "刪除失敗,無法刪除, 尚有文章或下層目錄"                        
                
        except exc.SQLAlchemyError as e:
            """ 捕獲錯誤, 否則無法回傳
            """
            if 'orig' in e.__dict__:
                return str(e.__dict__['orig'])
            #raise e
            return '刪除失敗!!'
        return None  
    
    #custom function -----

    def details_attribute(self,id=None):
        
        return {"fields":["屬性","屬性值","屬性圖片"],
                "data":[
                    ["尺寸","XL",""],
                    ["尺寸","L",""],
                    ["尺寸","M",""],
                    ["尺寸","S",""],
                    ["尺寸","XS",""],
                    ["顏色","黃",""],
                    ["顏色","白",""],
                    ["顏色","黑",""],
                    ["顏色","藍",""],
                    ["顏色","綠",""],
                    ["顏色","紅",""],
                    ["男女","男",""],
                    ["男女","女",""]
                ]}

    
    