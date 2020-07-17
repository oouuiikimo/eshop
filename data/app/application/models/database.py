from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from contextlib import contextmanager

# For this example we will use an in-memory sqlite DB.
# Let's also configure it to echo everything it does to the screen.
engine = create_engine('sqlite:///site.db', echo=False)

# The base class which our objects will be defined on.
Base = declarative_base()
# work with sess
from db_user import *
from db_product import *
# Create all tables by issuing CREATE TABLE commands to the DB.
#Base.metadata.create_all(engine) 


# create a configured "Session" class
Session = sessionmaker(bind=engine)

# create a Session
#db_session = Session()

@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def to_dict(row):
        dict = {}
        dict.update(row.__dict__)
        if "_sa_instance_state" in dict:
            del dict['_sa_instance_state']
        return dict
        
def run_my_program(func):
    result = None
    with session_scope() as session:
        result = func(session)
    return result    
        
def user_add(session):
    cust = Roles(role='customer')
    admin =Roles(role='admin')
    role1 = Roles(role='role1')
    tom = User(name='tom',email='tom@your-tom.com',active=True,source='local')
    tom.set_password('')
    session.add(admin)
    tom.roles.append(admin)
    session.add(cust)
    session.add(tom)

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
    #user_add()
    #user = db_session.query(User).filter(User.name=='tom').first()
    #func = add_productAttribute
    func = query_productAttribute
    result = run_my_program(func)
    print(result)