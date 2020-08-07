from flask import current_app as app
from flask_login import current_user
from .baserepo import BaseRepo
from ...models.db_article import BlogCategory
from ...models.db_user import User
from .form_blogcategory import SearchForm,UpdateForm
from sqlalchemy import exc
import datetime
from sqlalchemy.sql import text
 
class RepoBlogCategory(BaseRepo):
    def __init__(self):
        super().__init__()
        self.title = "部落格文章目錄"
        self.model = BlogCategory
        self.active_menu = "sub_list_blogcategory"
        self.description = """
        說明: 網站內文章列表, 請注意, 若有文章刪除, 前台連結將無法顯示文章內容, 更新亦同。
        """
        #異動tables
        #Base.metadata.create_all(app.db_session.engine)
        #異動data
        #self.init_db()
        
               
    def form_mapper(self,db_data):
        
        form_data = {"name":db_data.name,"is_leaf":'1' if db_data.is_leaf else '0',"parent":db_data.parent,'id':db_data.id}

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

    def get_listrows(self,rows):
        out_rows = []
        with app.db_session.session_scope() as session:
            for row in rows:
                created_by = session.query(User).filter_by(email=row.created_by).first()
                updated_by = session.query(User).filter_by(email=row.updated_by).first()
                if created_by: #更換為姓名
                    row.created_by = created_by.name
                if updated_by: #更換為姓名
                    row.updated_by = updated_by.name
                    
                out_rows.append(['<div style="width:100px;"><input type="checkbox" name="delete" value="{}">'.format(row.id)+
                    '<a href="javascript:delete_items({});" class="ml-1">'.format(row.id)+
                    '<i class="feather icon-x-circle" data-toggle="tooltip" title="刪除-{}-{}"></a></i>'.format(self.title,row.name)+
                    '<a href="/captain/update/BlogCategory/{}" class="ml-1">'.format(row.id)+
                    '<i class="feather icon-edit" data-toggle="tooltip" title="編輯-{}-{}"></a></i></div>'.format(self.title,row.name),
                    row.name,'是' if row.is_leaf else '否',row.parent if row.parent else '無',
                    row.created_by,row.created.strftime("%Y/%m/%d %H:%M"),row.updated_by,row.updated.strftime("%Y/%m/%d %H:%M")
                    ])
        return {
            "fields":['目錄名稱','最底層目錄','上層目錄','建立者','建立日期','更新者','更新日期'],
            "rows":out_rows
            }
            
    def get_search_filters(self,search):
        filters = []
        if search:
            if 'name' in search and search['name']: 
                filters.append(BlogCategory.name.like('%{}%'.format(search['name'])) )   
            if 'is_leaf' in search and search['is_leaf']: 
                filters.append(BlogCategory.is_leaf==search['is_leaf'])    
            if 'parent' in search and search['parent']: 
                filters.append(BlogCategory.parent==search['parent'])                  

        return filters
  
    def find(self, id=None):
        form_item = None
        if id:
            with app.db_session.session_scope() as session:
                db_item = session.query(BlogCategory).get(id)
                form_item = self.form_mapper(db_item)
        else:
            db_item = BlogCategory()
            form_item = self.form_mapper(db_item)
        return form_item

    def update(self,item,id=None):
        
        try:
            with app.db_session.session_scope() as session:
                #return str(item)
                if id and id is not None:
                    db_item = session.query(BlogCategory).get(id)
                else:
                    db_item = BlogCategory()
                    
                db_item.name = item.name
                db_item.is_leaf = True if item.is_leaf=='1' else False
                if item.parent:
                    parent = session.query(BlogCategory).filter_by(id==item.parent).first()
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
        try:
            """檢查:是否有網站引用,不能刪除"""
            #return str(type(items))
            with app.db_session.session_scope() as session: 
                for item in items:
                    _del = session.query(BlogCategory).filter(BlogCategory.id==item).first()
                    if _del:
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

    def is_has_child(self,id):
        with app.db_session.session_scope() as session:
            has_child = session.query(BlogCategory).filter(BlogCategory.parent_id==id).count()
        #result = BlogCategory.query.filter(BlogCategory.id.in_([i.parent_id for i in has_child])).count()
        return has_child #.with_entities(func.count(BlogCategory.id)).scalar()
    
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
                child = [i.id for i in session.execute(statement,{"id":id})]
                child.append(id) #自己以及下層, 都不能出現
                return [(i.id,i.name) for i in session.query(BlogCategory).filter(BlogCategory.id.notin_(child),BlogCategory.is_leaf==False).all()]
            else:
                #is_leaf 不能出現
                return [(i.id,i.name) for i in session.query(BlogCategory).filter(BlogCategory.is_leaf == False ).all()]
        
        #return func

    def get_tree_for_search(self):
        """搜尋表單, 欄位下接選擇項:不需列出最下層 is_leaf is False
        """
        #has_child = db.session.query(BlogCategory.parent_id).distinct()
        #return BlogCategory.query.filter(BlogCategory.id.in_([i.parent_id for i in has_child])).all()
        with app.db_session.session_scope() as session:
            return [(i.id,i.name) for i in session.query(BlogCategory).filter(BlogCategory.is_leaf == False).all()]

    def get_tree_for_article(self):
        """文章表單用:不列出含有下層目錄的母層, 只列子層-> is_leaf is True
        """

        #注意以下, notin 裡面必須排除掉 null 否則, 結果會不正確
        #has_child = db.session.query(BlogCategory.parent_id).filter(BlogCategory.parent_id.isnot(None)).distinct()
        #return BlogCategory.query.filter(BlogCategory.id.notin_(has_child)).all()
        with app.db_session.session_scope() as session:
            return [(i.id,i.name) for i in session.query(BlogCategory).filter(BlogCategory.is_leaf == True).all()]
        
    def __repr__(self):
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
            if self.parent:
                tree = session.execute(statement,{"id":self.id}).first()
                return tree.path

        return self.name