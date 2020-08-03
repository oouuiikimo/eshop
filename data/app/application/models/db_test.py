from database import DB_SESSION
from db_user import User,Roles,user_roles,Base as UserBase
from db_product import ProductAttribute,ProductType,Product,Article,ArticleCategory,Base as ProductBase

SQLALCHEMY_DATABASE_URI = 'sqlite:////home/user/data/app/application/models/site.db'

def run_my_program(func):
    result = None
    
    db = DB_SESSION(SQLALCHEMY_DATABASE_URI)
    with db.session_scope() as session:
        result = func(session)
    return result    
    
def create():

    db = DB_SESSION(SQLALCHEMY_DATABASE_URI)
    ProductBase.metadata.drop_all(db.engine) 
    ProductBase.metadata.create_all(db.engine) 
    #meta.drop_all(db.engine)
    #User.drop(db.engine)
    #User.create(db.engine)
    
def set_user(session):        
    tom = session.query(User).filter_by(email="tom@your-tom.com").first()
    tom.set_password('')
    
def user_add(session):
    Account = Roles(role='Account')
    admin =Roles(role='Admin')

    tom = User(name='tom',email='tom@your-tom.com',active=True,source='google')
    tom.set_password('')
    session.add(admin)
    session.add(Account)
    tom.roles.append(admin)
    session.add(tom)
    
def user_add2(session):
    oouuii_kimo = User(name='oouuii_kimo',email='oouuii_kimo@hotmail.com',active=True,source='facebook')
    account = session.query(Roles).filter_by(role='Account').first()
    oouuii_kimo.roles.append(account)
    session.add(oouuii_kimo)    

def update_user_roles(session):

    cust = session.query(Roles).filter_by(role='customer').first()
    admin =session.query(Roles).filter_by(role='admin').first()
    #role1 = Roles(role='role1')
    #session.add(role1)
    tom = session.query(User).get(1)
    tom.roles.clear()
    tom.roles.append(cust)
    #session.add(cust)
    #session.add(tom)
    _dict = [i.email for i in session.query(User).all()] 
    return _dict
    
def query_productAttribute(session):
    result = session.query(ProductAttribute).all()
    
    return  [to_dict(i) for i in result]
    
def add_productAttribute(session):
    
    atr1 = ProductAttribute(name='大小')
    atr2 = ProductAttribute(name='款式')
    atr3 = ProductAttribute(name='顏色')
    atr4 = ProductAttribute(name='重量')
    #atr4 = ProductAttribute(name='大小')
    session.add_all([atr1,atr2,atr3,atr4])

    
if __name__ == "__main__":
    
    #create()
    #user_add()
    #user = db_session.query(User).filter(User.name=='tom').first()
    #func = add_productAttribute
    #func = query_productAttribute
    #func = update_user_roles
    #result = run_my_program(func)
    print(run_my_program(set_user))