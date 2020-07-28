from flask import current_app as app
from flask_login import current_user
from .baserepo import BaseRepo
from ...models.db_user import Base,User,Roles,user_roles
from .form_user import SearchForm,UpdateForm
from sqlalchemy import exc
#from ...models.db_product import Article,ArticleCategory,ProductAttribute
"""
- model 集中放置於 /application/models/
- 各個 form 在同目錄下 
- 需在此repo 中, 一起import models 和 forms

"""
   
class RepoUser(BaseRepo):
    #public function  ----    
    def __init__(self):
        super().__init__()
        self.title = "管理員"
        self.model = User
        self.description = """
        說明: 本頁面管理後台的使用者帳戶基本資料及權限, 但最初的管理員帳號無法刪除, 失效, 更改權限。
        """
        #異動tables
        #Base.metadata.create_all(app.db_session.engine)
        #異動data
        #self.init_db()
        
        
    def __repr__(self):
        return self.title
        
    def form_mapper(self,db_user):
        
        user = {"name":db_user.name,"email":db_user.email,"active":"1" if bool(db_user.active) else "0",
            "source":db_user.source,"roles":[str(i.id) for i in db_user.roles]}
        user = self.Struct(**user)
        return user
        
    def update_form(self,id=None):
        user = self.find(id)
        form = UpdateForm(obj=user)
        form.roles.choices = self.get_roles()
        return form,user
        
    def search_form(self):
        form = SearchForm()
        form.roles.choices = form.roles.choices + self.get_roles()

        return form

    def get_listrows(self,rows):
        out_rows = []
        for row in rows:
            out_rows.append(['<div style="width:100px;"><input type="checkbox" name="delete" value="{}">'.format(row.id)+
                '<a href="javascript:delete_items({});" class="ml-1"><i class="feather icon-x-circle"></a></i>'.format(row.id)+
                '<a href="/captain/update/user/{}" class="ml-1"><i class="feather icon-edit"></a></i></div>'.format(row.id),
                row.name,
                row.email,'有效' if row.active else '失效',row.source, str(row.roles) if row.roles else "無"])
        return {
            "fields":['名稱','郵箱','有效','來源','權限'],
            "rows":out_rows
            }
            
    def get_search_filters(self,search):
        filters = []
        if search:
            if 'name' in search and search.name.data:
                filters.append(User.name==search.name.data)
            if 'email' in search and search.email.data:
                filters.append(User.email.like('%{}%'.format(search.email.data)) )            
            if 'source' in search and search.source.data:
                filters.append(User.source==search.source.data)   
            if 'roles' in search and search.roles.data:
                #filters.append(User.roles.any(Roles.role==search.roles.data.role))
                filters.append(User.roles.any(Roles.id == search.roles.data))
            if 'active' in search and search.active.data:
                filters.append(User.active==search.active.data)    
        return filters
  
    def find(self, id=None):
        form_item = None
        if id:
            with app.db_session.session_scope() as session: 
                db_user = session.query(User).get(id)
                form_item = self.form_mapper(db_user)
        else:
            db_user = User()
            form_item = self.form_mapper(db_user)
        return form_item

    def update(self,user,id=None):
        with self.session as session:
            if id and id is not None:
                db_user = session.query(User).get(id)
            else:
                db_user = User()
                
            db_user.name = user.name
            db_user.email = user.email
            db_user.active = True if user.active=="1" else False
            db_user.source = user.source
            
            if user.roles:
                roles = session.query(Roles).filter(Roles.id.in_(user.roles)).all()
                db_user.roles =roles
            else:
                db_user.roles.clear()
            if not id:
                session.add(db_user)
            session.commit()

    def delete(self, item):
        try:
            """檢查:管理員不能刪除"""
            #return str(type(item))
            with self.session as session: 
                for user in item:
                    
                    _del = session.query(User).filter(User.id==user).first()
                    if _del:
                        #return str(_del.id )
                        if _del.email == app.config['ADMIN']:
                            return "此帳號-{},是管理員,不能刪除!".format(_del.name)
                        if _del.id ==current_user.id:
                            return "此帳號-{},己登入,不能刪除!".format(_del.name)
                            
                        #_del.roles.clear()
                        #session.commit()
                        #session.delete(_del)
                        return "有錯誤發生" 
                
        except exc.SQLAlchemyError as e:
            """ 捕獲錯誤, 否則無法回傳
            """
            if 'orig' in e.__dict__:
                return str(e.__dict__['orig'])
            #raise e
            return '刪除失敗!!'
        return None  
    
    #custom function -----
    def get_roles(self):
        #choice = [('','選擇')]
        with app.db_session.session_scope() as session: 
            choice= [(str(g.id), g.role) for g in session.query(Roles).all()]
        return choice    

    
    