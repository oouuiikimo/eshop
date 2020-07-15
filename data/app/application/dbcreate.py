from .models.product import ProductAttribute,ProductType,Article,ArticleCategory
from .models.user import User,Roles,user_roles
   
def init_db(db):
        
    db.drop_all()
    db.create_all()
    cust = Roles(role='customer')
    admin =Roles(role='admin')
    role1 = Roles(role='role1')
    tom = User(name='tom',email='tom@your-tom.com',active=True,source='local')
    tom.set_password('6ouigugI')
    db.session.add(admin)
    tom.roles.append(admin)
    db.session.add(cust)
    db.session.add(tom)
    db.session.commit()   
    add_productAttribute(db)    
    add_article(db)
    add_articleCategories(db)

def update_db(db):
    from .models.user import User,Roles,user_roles

    cust = Roles.query.filter_by(role='customer').first()
    admin =Roles.query.filter_by(role='admin').first()
    role1 = Roles(role='role1')
    db.session.add(role1)
    tom = User.query.get(1)
    tom.roles.clear()
    tom.roles.append(cust)
    #db.session.add(cust)
    #db.session.add(tom)
    db.session.commit()   

def test_page(db):
    count = 120
    for i in range(1, count):
        db.session.add(ProductAttribute(name='testATR-{}'.format(i)))
    db.session.commit() 
    
def add_productAttribute(db):
    
    atr1 = ProductAttribute(name='大小')
    atr2 = ProductAttribute(name='款式')
    atr3 = ProductAttribute(name='顏色')
    atr4 = ProductAttribute(name='重量')
    #atr4 = ProductAttribute(name='大小')
    db.session.add_all([atr1,atr2,atr3,atr4])
    db.session.commit() 
    
def add_articleCategories(db):
    art_c_1 = ArticleCategory(name='文章類別一.1.1')
    art_c_2 = ArticleCategory.query.filter_by(name='文章類別一.1').first()
    art_c_1.parent = art_c_2
    db.session.add(art_c_1)
    db.session.commit() 
    
def add_article(db):
    art_c_1 = ArticleCategory(name='文章類別一')
    art_c_2 = ArticleCategory(name='文章類別一.1')
    art_c_3 = ArticleCategory(name='文章類別一.2')
    art_c_1.child.append(art_c_2)
    art_c_3.parent = art_c_1
    db.session.add(art_c_1)
    db.session.add(art_c_2)
    db.session.add(art_c_3)
    db.session.commit() 
    