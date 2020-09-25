import sys
sys.path.append("..")
from models.db_customer import (Customer)

from db_test import run_my_program,create,drop

author = 'tom@your-tom.com'
    
def add(session):
    c1 = Customer(name="tom",email='tom@your-tom.com',source='google',active=True)
    c1.created_by = 'tom@your-tom.com'
    c1.updated_by = 'tom@your-tom.com'
    
    session.add(c1)
    
def reset():
    drop(CustomerBase)
    create(CustomerBase)
    
if __name__ == "__main__":
    func = add #set_product_category #product_category_add #product_add
    print(run_my_program(func))
    