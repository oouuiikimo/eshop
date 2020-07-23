from .test import Test
from flask import current_app as app
from .baserepo import BaseRepo
from ...models.db_user import Base,User,Roles,user_roles
from .form_user import SearchForm
#from ...models.db_product import Article,ArticleCategory,ProductAttribute
"""
- model 集中放置於 /application/models/
- 各個 form 在同目錄下 
- 需在此repo 中, 一起import models 和 forms

"""
        
class RepoUser(BaseRepo):
          
    def __init__(self):
        super().__init__()
        self.title = "使用者管理"
        self.model = User
        #異動tables
        #Base.metadata.create_all(app.db_session.engine)
        #異動data
        #self.init_db()

    def init_db(self):
        user = User(name='tom',email='tom@your-tom.com',active=True,source='local')
        role = Roles(role='admin')
        user.roles.append(role)
        self.session_scope.add(user)
        #self.session.commit()
        
    def search_form(self):
        return SearchForm
        
    def all(self,page,per_page,search):
        dict = None

        with self.session as session: 
            user = session.query(User).all()
            dict = app.db_session.rows_to_dict(user, True)
        
        return dict

    def get_listrows(self,rows):
        out_rows = []
        for row in rows:
            out_rows.append(['<input type="checkbox" name="delete" value="{}">'.format(row.id),
                '<a href="/captain/update/Accounts/User/{}">{}</a>'.format(row.id,row.name),
                row.email,'有效' if row.active else '失效',row.source,str(row.roles)])
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
                filters.append(User.roles.any(Roles.role==search.roles.data.role))
            if 'active' in search and search.active.data:
                filters.append(User.active==search.active.data)    
        return filters
            
    def create(self, title, body):
        post = Post(title=title, body=body)
        self.session_scope.add(post)
        #self.session.commit()
        return post

    def find(self, id):
        #todo:必須結合select 到roles model
        u={"id":1,"name":"tom","email":"oo@yppyy.cc","source":"facebook","active":1,"roles":[1]}
        d = Dynamic(**u)
        class U():
            def __init__(self):
                self.id = 1
                self.name = "tom"
        user = d #{"id":1,"name":"tom","email":"oo@yyy.cc","source":"google","active":1,"roles":[(1,"admin")]}
        return self.session_scope.query(User).filter(User.id == id).first()

    def update(self, User):
        
        self.session_scope.add(User)
        #self.session.commit()

    def delete(self, item):
        try:
            """檢查:管理員不能刪除"""
            with app.db_session.session_scope() as session: 
                for user in item:
                    _del = session.query(User).filter(User.id==user).first()
                    if _del.email == current_app.config['ADMIN']:
                        return "此帳號-{},是管理員,不能刪除!".format(_del.name)
                    if _del.id ==current_user.id:
                        return "此帳號-{},己登入,不能刪除!".format(_del.name)

                str_roles = "delete from user_roles where user_id in (:item);"
                session.execute(str_roles,{'item':item})
                stm = User.__table__.delete().where(User.id.in_(item))
                session.execute(stm)
                
        except exc.SQLAlchemyError as e:
            """ 捕獲錯誤, 否則無法回傳
            """
            if 'orig' in e.__dict__:
                return str(e.__dict__['orig'])
            #raise e
            return '刪除失敗!!'
        return None  
        
    def restore_roles(self,roles):
        #return User.roles
        if roles:
            roles = self.session_scope.query(Roles).filter(Roles.id.in_(roles)).all()
            #User.roles =roles
            return roles
        return None
    def get_roles(self):
        return [(str(g.id), g.role) for g in self.session_scope.query(Roles).all()]        
        
    def __repr__(self):
        return self.title
    
    