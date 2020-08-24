import sys
sys.path.append("..")
from models.db_product import (SubProductCategory,ProductCategory,
    Product,ProductSku,ProductArticle,ProductReview
    )
    
from models.db_customer import Customer
from db_test import run_my_program,create,drop
    
author = 'tom@your-tom.com'
    
def product_add(session):
    p2 = Product(name="p2",active=True,order=1)
    p2.created_by = 'tom@your-tom.com'
    p2.updated_by = 'tom@your-tom.com'
    
    session.add(p2)
    
def update_product(session,id):
    p = session.query(Product).get(1)
    p.attribute = [
                {'name':'Size',
                 'variants':[
                            {'text':'XL','image':''},
                            {'text':'L','image':''},
                            {'text':'M','image':''},
                            {'text':'S','image':''},
                            {'text':'XS','image':''}
                            ]},
                {'name':'Color',
                 'variants':[
                            {'text':'白','image':''},
                            {'text':'藍','image':''},
                            {'text':'黃','image':''},
                            {'text':'綠','image':''},
                            {'text':'紅','image':''},
                            {'text':'黑','image':''}
                            ]},   
                 {'name':'Gender',
                 'variants':[
                            {'text':'男','image':''},
                            {'text':'女','image':''}
                             ]}
        ]    
        
    session.add(p)    
    
def sku_add(session,id):
    p = session.query(Product).get(id)
    #sku = ProductSku(sku="XL-白-男",sku_details={"Size":"XL","Color":"白","Gender":"男"},
    #created_by = 'tom@your-tom.com',updated_by = 'tom@your-tom.com')
    sku = session.query(ProductSku).get(id)
    sku.product = p
    session.add(sku)
    
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

def sub_product_review_add(session):
    c = session.query(Customer).get(1)
    p = session.query(Product).get(1)
    r1 = ProductReview(review="促銷商品")
    r1.product = p
    r1.customer = c

    session.add(r1)
    
def reset():
    #drop(ProductBase)
    #create(ProductBase)
    pass
    
if __name__ == "__main__":

    #drop(ProductSku)
    #create(ProductSku)
    
    #"""
    func = sku_add
    print(run_my_program(func,1))
    #"""
    