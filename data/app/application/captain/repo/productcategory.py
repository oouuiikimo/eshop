from flask import current_app as app
from flask_login import current_user
from .baserepo import BaseRepo
from ...models.db_product import ProductCategory
from ...models.db_user import User
from ...models.db_customer import Customer
from .form_productcategory import SearchForm,UpdateForm
from sqlalchemy import exc
import datetime
from sqlalchemy.sql import text
 
class RepoProductCategory(BaseRepo):
    def __init__(self):
        super().__init__()
        self.title = "商品主目錄維護"
        self.model = ProductCategory
        self.active_menu = "sub_list_productcategory"
        self.description = """
        說明: 網站內文章列表, 請注意, 若有文章刪除, 前台連結將無法顯示文章內容, 更新亦同。
        """
        #異動tables
        #Base.metadata.create_all(app.db_session.engine)
        #異動data
        #self.init_db()
        
               
    def form_mapper(self,db_data):
        
        form_data = {"name":db_data.name,"is_leaf":'1' if db_data.is_leaf else '0',"parent":str(db_data.parent_id),'id':db_data.id}

        return self.Struct(**form_data)
        
    def update_form(self,id=None):
        db_item = self.find(id)
        form = UpdateForm(obj=db_item)
        #if form has any select choices to fill... => parent
        #example:form.roles.choices = self.get_roles()
        form.parent.choices = form.parent.choices + self.get_tree(id)
        return form,db_item
        
    def search_form(self):
        form = SearchForm()
        #if form has any select choices to fill...
        #form.roles.choices = form.roles.choices + self.get_roles()
        form.parent.choices = form.parent.choices + self.get_tree_for_search()

        return form

    def _list_rows(self,row):
        #if row.id == 2:
        #    raise Exception(str(row.parent.name))
        return {
                'title_field':row.name,
                'fields_value':[
                    row.name,'是' if row.is_leaf else '否',
                    self.get_cat_path(row) if row.parent else '無',
                    ]
                }
                
    def _list_fields(self):
        return ['目錄名稱','最底層目錄','上層目錄']

    def _get_all_child_id(self,id):
        with app.db_session.session_scope() as session:
            child = [i.id for i in session.execute(self._child_tree_sql(),{"id":id})]
            #所有下層
            return child
                
    def get_search_filters(self,search):
        filters = []

        
        if search:
            if 'name' in search and search['name']: 
                filters.append(ProductCategory.name.like(f'%{search["name"]}%') )   
            if 'is_leaf' in search and search['is_leaf']: 
                filters.append(ProductCategory.is_leaf==search['is_leaf'])    
            if 'parent' in search and search['parent']: 
                #raise Exception(str(_get_all_child_id(int(search['parent']))))
                filters.append(ProductCategory.id.in_(self._get_all_child_id(int(search['parent']))))   
                #todo: 要把該類以下所有的類別id,全列出來才對              

        return filters
  
    def find(self, id=None):
        form_item = None
        if id:
            with app.db_session.session_scope() as session:
                db_item = session.query(ProductCategory).get(id)
                form_item = self.form_mapper(db_item)
        else:
            db_item = ProductCategory()
            form_item = self.form_mapper(db_item)
        return form_item

    def update(self,item,id=None):
        
        try:
            with app.db_session.session_scope() as session:
                #return str(item)
                if id and id is not None:
                    db_item = session.query(ProductCategory).get(id)
                else:
                    db_item = ProductCategory()
                    
                db_item.name = item.name
                db_item.is_leaf = True if item.is_leaf=='1' else False
                if item.parent:
                    parent = session.query(ProductCategory).filter(ProductCategory.id==int(item.parent)).first()
                    db_item.parent = parent
                else:
                    db_item.parent = None
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
    
        def validate_has_child(session,item):
            if not self._get_all_child_id(item.id):
                return False
            return True
            
        def validate_has_blog(session,item):
            if not item.is_leaf:
                return False
            #todo:建立blog repo 後要添加以下程式,檢查是否有文章在此目錄底下
            blog = session.query(BlogArticle).filter(BlogArticle.id_category==item.id).first()
            if not blog:
                return False
            return True
        try:
            """檢查:是否有網站引用,不能刪除,有下層目錄亦不能刪除"""
            #return str(type(items))
            with app.db_session.session_scope() as session: 
                for item in items:
                    
                    _del = session.query(ProductCategory).filter(ProductCategory.id==item).first()
                    if _del:
                        if not validate_has_child(session,_del) and not validate_has_blog(session,_del):
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

    def is_has_child(self,id):
        with app.db_session.session_scope() as session:
            has_child = session.query(ProductCategory).filter(ProductCategory.parent_id==id).count()
        #result = ProductCategory.query.filter(ProductCategory.id.in_([i.parent_id for i in has_child])).count()
        return has_child #.with_entities(func.count(ProductCategory.id)).scalar()
    
    def _child_tree_sql(self):
        return text(
        """
        WITH RECURSIVE category_path (id, path) AS
        (
          SELECT id, name as path
            FROM blog_category
            WHERE parent_id ==:id /*IS NULL or ==2*/
            
          UNION ALL
          SELECT c.id,  cp.path|| ' > '|| c.name as path
            FROM category_path AS cp JOIN blog_category AS c
              ON cp.id = c.parent_id
        )
        SELECT * FROM category_path
        ORDER BY path;
        """)
        
    def get_tree(self,id=None):
        """更新或新增表單用,顯示上層目錄供歸屬:
            .不能列出參考列的下層,只能列上層, is_leaf=True, 不然會形成迴圏, 
        """
        #def func():
        statement = text(
        """
        WITH RECURSIVE category_path (id, path) AS
        (
          SELECT id, name as path
            FROM blog_category
            WHERE parent_id ==:id /*IS NULL or ==2*/
            
          UNION ALL
          SELECT c.id,  cp.path|| ' > '|| c.name as path
            FROM category_path AS cp JOIN blog_category AS c
              ON cp.id = c.parent_id
        )
        SELECT * FROM category_path
        ORDER BY path;
        """)
        with app.db_session.session_scope() as session:
            if id:
                child = [i.id for i in session.execute(self._child_tree_sql(),{"id":id})]
                child.append(id) #自己以及下層, 都不能出現
                return [(str(i.id),self.get_cat_path(i)) for i in session.query(ProductCategory).filter(ProductCategory.id.notin_(child),ProductCategory.is_leaf==False).all()]
            else:
                #is_leaf 不能出現
                return [(str(i.id),self.get_cat_path(i)) for i in session.query(ProductCategory).filter(ProductCategory.is_leaf == False ).all()]
        
        #return func

    def get_tree_for_search(self):
        """搜尋表單, 欄位下接選擇項:不需列出最下層 is_leaf is False
        """
        #has_child = db.session.query(ProductCategory.parent_id).distinct()
        #return ProductCategory.query.filter(ProductCategory.id.in_([i.parent_id for i in has_child])).all()
        with app.db_session.session_scope() as session:
            return [(str(i.id),self.get_cat_path(i)) for i in session.query(ProductCategory).filter(ProductCategory.is_leaf == False).all()]

    def get_tree_for_article(self):
        """文章表單用:不列出含有下層目錄的母層, 只列子層-> is_leaf is True
        """

        #注意以下, notin 裡面必須排除掉 null 否則, 結果會不正確
        #has_child = db.session.query(ProductCategory.parent_id).filter(ProductCategory.parent_id.isnot(None)).distinct()
        #return ProductCategory.query.filter(ProductCategory.id.notin_(has_child)).all()
        with app.db_session.session_scope() as session:
            return [(str(i.id),i.name) for i in session.query(ProductCategory).filter(ProductCategory.is_leaf == True).all()]
        
    def __repr__(self):
        return self.title
    
    def get_cat_path(self,item_cat):
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
            if item_cat.parent:
                tree = session.execute(statement,{"id":item_cat.id}).first()
                return tree.path

        return item_cat.name