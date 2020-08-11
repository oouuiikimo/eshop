from flask import current_app as app
from flask_login import current_user
from .baserepo import BaseRepo
from ...models.db_article import BlogCategory,BlogArticle
from ...models.db_user import User
from .form_blogarticle import SearchForm,UpdateForm
from sqlalchemy import exc
import datetime
from sqlalchemy.sql import text
 
class RepoBlogArticle(BaseRepo):
    def __init__(self):
        super().__init__()
        self.title = "部落格文章"
        self.model = BlogArticle
        self.active_menu = "sub_list_blogarticle"
        self.description = """
        說明: 網站內文章列表, 請注意, 若有文章刪除, 前台連結將無法顯示文章內容, 更新亦同。
        """
        #異動tables
        #Base.metadata.create_all(app.db_session.engine)
        #異動data
        #self.init_db()
        
    def __repr__(self):
        return self.title
        
    def form_mapper(self,db_data):
        #raise Exception(str("\n".join(f'<div class="badge badge-danger">{i}</div>' for i in db_data.tag)))
        form_data = {
            "title":db_data.title,
            "active":'1' if db_data.active else '0',
            "content":db_data.content,
            "id_category":str(db_data.id_category),
            'id':db_data.id,
            'description':db_data.description,
            'tag': ",".join(db_data.tag) if db_data.tag else ""
            #'tag':'<div class="badge badge-danger">{i}</div>' for i in db_data.tag
            }

        return self.Struct(**form_data)
        
    def update_form(self,id=None):
        db_item = self.find(id)
        form = UpdateForm(obj=db_item)
        #if form has any select choices to fill... => parent
        #example:form.roles.choices = self.get_roles()
        form.id_category.choices = form.id_category.choices + self.get_tree_for_article()
        return form,db_item
        
    def search_form(self):
        form = SearchForm()
        #if form has any select choices to fill...
        #form.roles.choices = form.roles.choices + self.get_roles()
        form.id_category.choices = form.id_category.choices + self.get_tree_for_article()

        return form

    def _list_rows(self,row):
        #if row.id == 2:
        #    raise Exception(str(row.parent.name))
        return {
                'title_field':row.id,
                'fields_value':[
                    row.title,'是' if row.active else '否',
                    self.get_cat_path(row.id_category) if row.id_category else '無',
                    "\n".join(f'<div class="badge badge-primary">{i}</div>' for i in row.tag)
                    ]
                }
                
    def _list_fields(self):
        return ['標題','上架','上層目錄','標簽']
               
    def get_search_filters(self,search):
        filters = []

        
        if search:
            if 'title' in search and search['title']: 
                filters.append(BlogArticle.title.like(f'%{search["title"]}%') )   
            if 'active' in search and search['active']: 
                filters.append(BlogArticle.active==search['active'])    
            if 'id_category' in search and search['id_category']: 
                filters.append(BlogArticle.id_category==int(search['id_category']))       
            
        return filters
  
    def find(self, id=None):
        form_item = None
        if id:
            with app.db_session.session_scope() as session:
                db_item = session.query(BlogArticle).get(id)
                form_item = self.form_mapper(db_item)
        else:
            db_item = BlogArticle()
            form_item = self.form_mapper(db_item)
        return form_item

    def update(self,item,id=None):
        
        try:
            with app.db_session.session_scope() as session:
                #return str(item)
                if id and id is not None:
                    db_item = session.query(BlogArticle).get(id)
                else:
                    db_item = BlogArticle()
                    
                db_item.title = item.title
                db_item.content = item.content
                db_item.description = item.description
                db_item.active = True if item.active=='1' else False
                db_item.tag = item.tag.split(',')
                #raise Exception(str(item.tag))
                if item.id_category:
                    category = session.query(BlogCategory).filter(BlogCategory.id==int(item.id_category)).first()
                    db_item.category = category
                else:
                    db_item.category = None
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
    
        try:
            """檢查:是否有網站引用,不能刪除,有下層目錄亦不能刪除"""
            #return str(type(items))
            with app.db_session.session_scope() as session: 
                for item in items:
                    _del = session.query(BlogArticle).filter(BlogArticle.id==item).first()
                    session.delete(_del)
                
        except exc.SQLAlchemyError as e:
            """ 捕獲錯誤, 否則無法回傳
            """
            if 'orig' in e.__dict__:
                return str(e.__dict__['orig'])
            #raise e
            return '刪除失敗!!'
        return None  
    
    #custom function -----   

    def get_tree_for_article(self):
        """文章表單用:不列出含有下層目錄的母層, 只列子層-> is_leaf is True
        """

        #注意以下, notin 裡面必須排除掉 null 否則, 結果會不正確
        #has_child = db.session.query(BlogCategory.parent_id).filter(BlogCategory.parent_id.isnot(None)).distinct()
        #return BlogCategory.query.filter(BlogCategory.id.notin_(has_child)).all()
        with app.db_session.session_scope() as session:
            return [(str(i.id),i.name) for i in session.query(BlogCategory).filter(BlogCategory.is_leaf == True).all()]
    
    def get_cat_path(self,id):
        #return only one cat tree
        statement = text(
        """
        WITH RECURSIVE category_path (id, path) AS
        (
          SELECT id, name as path
            FROM blog_category
            WHERE parent_id IS NULL
          UNION ALL
          SELECT c.id,  cp.path|| ' > '|| c.name as path
            FROM category_path AS cp JOIN blog_category AS c
              ON cp.id = c.parent_id
        )
        SELECT * FROM category_path
        where id == :id;
        """)
        with app.db_session.session_scope() as session:
            tree = session.execute(statement,{"id":id}).first()
            return tree.path
