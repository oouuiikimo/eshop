from flask import current_app as app
from flask_login import current_user
from .baserepo import BaseRepo
from ...models.db_product import ProductArticle
from ...models.db_customer import Customer
from ...models.db_user import User
from .form_productarticle import SearchForm,UpdateForm
from sqlalchemy import exc
import datetime

class RepoProductArticle(BaseRepo):
    #public function  ----    
    def __init__(self):
        super().__init__()
        self.title = "商品頁面內文章"
        self.model = ProductArticle
        self.active_menu = "sub_list_productarticle"
        self.description = """
        說明: 商品頁面內文章列表, 請注意, 若有文章刪除, 前台連結將無法顯示文章內容, 更新亦同。
        """
        #異動tables
        #Base.metadata.create_all(app.db_session.engine)
        #異動data
        #self.init_db()
        
        
    def __repr__(self):
        return self.title
        
    def form_mapper(self,db_data):
        
        form_data = {"title":db_data.title,"content":db_data.content,"tag":",".join(db_data.tag) if db_data.tag else ""}

        return self.Struct(**form_data)
        
    def update_form(self,id=None):
        db_item = self.find(id)
        form = UpdateForm(obj=db_item)
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
                'title_field':row.title,
                'fields_value':[
                    row.title,
                    "\n".join(f'<div class="badge badge-primary">{i}</div>' for i in row.tag)
                    ]
                }
                
    def _list_fields(self):
        return ['文章標題','標簽']
                   
    def get_search_filters(self,search):
        filters = []
        if search:
            if 'title' in search and search['title']: 
                filters.append(ProductArticle.title.like(f'%{search["title"]}%') )   
            if 'tag' in search and search['tag']: #search json list
                filters.append(ProductArticle.tag.contains(search['tag']) )            

        return filters
  
    def find(self, id=None):
        form_item = None
        if id:
            with app.db_session.session_scope() as session: 
                db_item = session.query(ProductArticle).get(id)
                form_item = self.form_mapper(db_item)
        else:
            db_item = ProductArticle()
            form_item = self.form_mapper(db_item)
        return form_item

    def update(self,item,id=None):
    
        def strip_link_text(link): #不能有空白
            return "_".join(link.split())
        
        try:
            with app.db_session.session_scope() as session:
                if id and id is not None:
                    db_item = session.query(ProductArticle).get(id)
                else:
                    db_item = ProductArticle()
                    
                db_item.title = item.title
                db_item.content = item.content
                db_item.tag = item.tag.split(',')
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
                    _del = session.query(ProductArticle).filter(ProductArticle.id==item).first()
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


    
    