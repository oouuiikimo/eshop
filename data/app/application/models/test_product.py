from db_product import (SubProductCategory,ProductCategory,
    Product,product_subcategory,
    #ProductAttribute,ProductType,
    Product,Base as ProductBase)
from db_test import run_my_program,create,drop
    
author = 'tom@your-tom.com'
    
def product_add(session):
    p2 = Product(name="p2",active=True,order=1)
    p2.created_by = 'tom@your-tom.com'
    p2.updated_by = 'tom@your-tom.com'
    
    session.add(p2)
    
def set_product_category(session,id,cat_id):   
    p = session.query(Product).get(id)
    c = session.query(ProductCategory).get(cat_id)
    p.category=c
    session.add(p)
    
def product_category_add(session):    
    pc1= ProductCategory(name="服裝",is_leaf=False,active=1,order=1,
        created_by = 'tom@your-tom.com',updated_by = 'tom@your-tom.com')
    pc2= ProductCategory(name="男裝",is_leaf=False,active=1,order=1,
        created_by = 'tom@your-tom.com',updated_by = 'tom@your-tom.com')
    pc2.parent = pc1
    session.add(pc1)
    session.add(pc2)
    
def sub_product_category_add(session):
    p = session.query(Product).get(1)
    spc1 = SubProductCategory(name="促銷商品",is_leaf=True,active=1,order=1,
        created_by=author,updated_by=author)
    p.sub_categorys.append(spc1)
    session.add(p)

def reset():
    drop(ProductBase)
    create(ProductBase)
    
if __name__ == "__main__":
    reset()
    """
    func = sub_product_category_add #set_product_category #product_category_add #product_add
    print(run_my_program(func))
    """
    