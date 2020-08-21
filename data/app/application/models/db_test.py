from database import DB_SESSION
from db_user import User,Roles,user_roles,Base as UserBase
from db_product import (SubProductCategory,ProductCategory,
    Product,product_subcategory,
    #ProductAttribute,ProductType,
    Product,Base as ProductBase)
from db_article import BlogCategory,SiteArticle,BlogArticle,Base as ArticleBase

#SQLALCHEMY_DATABASE_URI = 'sqlite:////home/user/data/app/application/models/site.db'
SQLALCHEMY_DATABASE_URI = 'sqlite:////home/user/data/app/application/site1.db'

def run_my_program(func,*arg):
    #用統一的session 去跑測試的 func,回傳func結果
    db = DB_SESSION(SQLALCHEMY_DATABASE_URI)
    with db.session_scope() as session:
        return func(session,*arg)
    return None    
    
def create(model):
    #可單獨建立群組表格, 依import mudule 的 Base
    db = DB_SESSION(SQLALCHEMY_DATABASE_URI)
    model.metadata.create_all(db.engine) 
    
def drop(model):
    #可單獨刪除群組表格, 依import mudule 的 Base
    db = DB_SESSION(SQLALCHEMY_DATABASE_URI)
    model.metadata.drop_all(db.engine) 
    
def set_user(session):        
    tom = session.query(User).filter_by(email="tom@your-tom.com").first()
    tom.set_password('')
    
def user_add(session):
    Account = Roles(role='Account')
    admin =Roles(role='Admin')

    tom = User(name='tom',email='tom@your-tom.com',active=True,source='google')
    tom.created_by = 'tom@your-tom.com'
    tom.updated_by = 'tom@your-tom.com'
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
    from test_product import product_add
    #drop(ProductBase)
    #create(ProductBase)
    #func = user_add
    #user = db_session.query(User).filter(User.name=='tom').first()
    func = product_add
    #func = query_productAttribute
    #func = update_user_roles
    print(run_my_program(func))
    #print(run_my_program(func))
    #drop()
    