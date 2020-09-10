import sys
sys.path.append("..")
from models.db_product import (SubProductCategory,ProductCategory,
    Product,ProductSku,ProductArticle,ProductReview,
    ProductArticleMaster,ProductImage,
    Variant,VariantValues
    )
    
from models.db_customer import Customer
from db_test import run_my_program,create,drop
    
author = 'tom@your-tom.com'
    
def product_add(session):
    p1 = Product(name="p1",active=True,order=1,sku='p1',
        created_by=author,updated_by=author)    
    session.add(p1)
        
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

def add_article(session):
    a1 = ProductArticle(name='文1',content='content for 文1',
        created_by=author,updated_by=author)
    a2 = ProductArticle(name='文2',content='content for 文2',
        created_by=author,updated_by=author) 
    a3 = ProductArticle(name='文3',content='content for 文3',
        created_by=author,updated_by=author)   
    session.add(a1)
    session.add(a2)
    session.add(a3)
    
def add_article_master(session):
    am1 = ProductArticleMaster(title='商品介紹',order=1)
    a1=session.query(ProductArticle).get(1)
    a2=session.query(ProductArticle).get(2)
    a3=session.query(ProductArticle).get(3)
    am1.articles.append(a3)
    am1.articles.append(a2)
    am1.articles.append(a1)
    session.add(am1)
    p1 = session.query(Product).get(1)
    p1.articles.append(am1)

def query_product_articles(session):
    p1 = session.query(Product).get(1)
    #ars = p1.articles[0].articles #.articles
    print(f'商品:{p1.name}')
    for master in p1.articles:
        print(f'{master.title} | order:{master.order}')
        
        for ar in master.articles:
            print(f'{ar.id}-{ar.name}-{ar.content}')

def set_product_variants(session):
    p1 = session.query(Product).get(1)
    v = session.query(Variant).all()
    p1.variants.extend([v[0],v[1]])
    session.add(p1)
    
def query_product_variants(session):
    p1 = session.query(Product).get(1)
    
    for variant in p1.variants:
        print(str(variant))
        print(str(variant.values))
        
        
    
def add_variant(session):
    v1 = Variant(variant="尺寸")
    v2 = Variant(variant="顏色")
    v3 = Variant(variant="材質")
    v1v1 = VariantValues(value="XXL",order=1)
    v1v2 = VariantValues(value="XL",order=2)
    v1v3 = VariantValues(value="L",order=3)
    v1v4 = VariantValues(value="M",order=4)
    v1v5 = VariantValues(value="S",order=5)
    v1v6 = VariantValues(value="XS",order=6)
    v1v7 = VariantValues(value="XXS",order=7)
    v2v1 = VariantValues(value="黑",order=1)
    v2v2 = VariantValues(value="白",order=2)
    v2v3 = VariantValues(value="紅",order=3)
    v2v4 = VariantValues(value="藍",order=4)
    v2v5 = VariantValues(value="綠",order=5)
    v2v6 = VariantValues(value="黃",order=6)
    v2v7 = VariantValues(value="紫",order=7)
    v2v8 = VariantValues(value="粉",order=8)
    v3v1 = VariantValues(value="棉",order=1)
    v3v2 = VariantValues(value="尼龍",order=2)
    v3v3 = VariantValues(value="纖維",order=3)
    v1.values.extend([v1v1,v1v2,v1v3,v1v4,v1v5,v1v6,v1v7])
    v2.values.extend([v2v1,v2v2,v2v3,v2v4,v2v5,v2v6,v2v7,v2v8])
    v3.values.extend([v3v1,v3v2,v3v3])
    session.add_all([v1,v2,v3])

def set_sku(session):
    p1 = session.query(Product).get(1)
    sku1 = ProductSku(name='L-黃',sku='L-黃',quantity=5,price=100)
    L = session.query(VariantValues).get(3)
    yellow = session.query(VariantValues).get(13)
    sku1.values.extend([L,yellow])
    sku1.product = p1
    session.add(sku1)
    
def query_product_sku(session):    
    p1 = session.query(Product).get(1)
    print(p1)
    for sku in p1.skus:
        print(sku)
        for value in sku.values:
            print(f'{value.variant}:{value}')

def query_category_product(session):
    p1 = session.query(Product).get(1)
    c1 = session.query(ProductCategory).get(1)
    p1.category = c1
    session.add(p1)
    
def reset():
    drop(SubProductCategory,ProductCategory,
        Product,ProductSku,ProductArticle,ProductReview,
        ProductArticleMaster,ProductImage,
        Variant,VariantValues,ProductSkuValues)
    create(SubProductCategory,ProductCategory,
        Product,ProductSku,ProductArticle,ProductReview,
        ProductArticleMaster,ProductImage,
        Variant,VariantValues,ProductSkuValues)
    
    
if __name__ == "__main__":
    
    #drop(ProductSku)
    #create(ProductSku)
    
    #"""
    funcs = [query_category_product] #[query_product_variants,set_sku] #[add_variant,product_add,set_product_variants] 
    for func in funcs:
        run_my_program(func)
    #"""
    