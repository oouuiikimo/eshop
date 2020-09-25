# sqlalchemy.orm import mapper, sessionmaker
from .test import Test
#from flask import current_app as app
from .baserepo import BaseRepo
"""
- model 集中放置於 /application/models/
- 各個 form 在同目錄下 
- 需在此repo 中, 一起import models 和 forms

"""
        
class User(BaseRepo):
          
    def __init__(self):
        super().__init__()
        self.title = "使用者管理"
        #self.init_db()

    def init_db(self):
        user = User(name='tom',email='tom@your-tom.com',active=True,source='local')
        role = Roles(role='admin')
        user.roles.append(role)
        self.session.add(user)
        self.session.commit()
        
    def all(self):
        return self.session.query(Post).all()

    def create(self, title, body):
        post = Post(title=title, body=body)
        self.session.add(post)
        self.session.commit()
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
        return self.session.query(User).filter(User.id == id).first()

    def update(self, User):
        
        self.session.add(User)
        self.session.commit()

    def delete(self, post):
        self.session.delete(post)
        self.session.commit()
        
    def restore_roles(self,roles):
        #return User.roles
        if roles:
            roles = self.session.query(Roles).filter(Roles.id.in_(roles)).all()
            #User.roles =roles
            return roles
        return None
    def get_roles(self):
        return [(str(g.id), g.role) for g in self.session.query(Roles).all()]        
        
    def __repr__(self):
        return self.title
    
    