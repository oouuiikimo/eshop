from .. import login_manager
from flask import current_app as app
from flask_login import UserMixin
from ..models.db_user import User

class UserLogin(UserMixin):
    
    def __init__(self,_user):
    
        self.id = int(_user.id)
        self.name = str(_user.name)
        self.email = str(_user.email)
        self.created = str(_user.created)
        self.source = str(_user.source)
        self.active = str(_user.active)
        self.photo = str(_user.photo)
        self.last_login = str(_user.last_login)
        self.roles = [str(i.role) for i in _user.roles]
        
    def get_id(self):
        return self.id
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
                
    @staticmethod
    def get_user(id):
        
        with app.db_session.session_scope() as session:     
              
            user = UserLogin(session.query(User).get(id))
            #raise Exception(user)
            return user

            
if __name__ == "__main__":
    
    result = User.get('MS001') 
    print(result)   