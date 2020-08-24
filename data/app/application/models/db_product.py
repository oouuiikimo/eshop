from sqlalchemy.orm import validates,load_only,relationship,backref
from sqlalchemy import (Integer,ForeignKey,String,DateTime,
    Column,Boolean,Text,JSON,Table,BLOB)
import datetime
from sqlalchemy.sql import text
from .db_base import Base

product_subcategory = Table('product_subcategory', Base.metadata,
    Column('id',Integer, primary_key=True),
    Column('product_id', Integer, ForeignKey('product.id')),
    Column('subcategory_id', Integer, ForeignKey('sub_product_category.id'))
    )
    
class ProductCategory(Base):
    #todo: 有些function 要cache
    
    __tablename__ = "product_category"
    id = Column(Integer, primary_key = True)
    name = Column(String(50),
                         unique=True,
                         nullable=False)
    is_leaf = Column(Boolean,nullable=False,default=False)
    order = Column(Integer)
    active = Column(Boolean,default=False)
    created = Column(DateTime,
                    index=False,
                    unique=False,
                    default=datetime.datetime.now(),
                    nullable=False)
    updated = Column(DateTime,
                    index=False,
                    unique=False,
                    nullable=False,
                    default=datetime.datetime.now())
    created_by = Column(String(80),
                    nullable=False)
    updated_by = Column(String(80),
                    nullable=False)
    """
    雙向ref做法
    child = relationship("BlogCategory",
                backref=backref('parent', remote_side=[id]))
    """
    parent_id = Column(Integer, ForeignKey('product_category.id'))
    child = relationship("ProductCategory",
                backref=backref('parent', remote_side=[id]))
                
class SubProductCategory(Base):
    #todo: 有些function 要cache
    
    __tablename__ = "sub_product_category"
    id = Column(Integer, primary_key = True)
    name = Column(String(50),
             unique=True,
             nullable=False)
    is_leaf = Column(Boolean,nullable=False,default=False)
    order = Column(Integer)
    active = Column(Boolean,default=False)
    created = Column(DateTime,
                    index=False,
                    unique=False,
                    default=datetime.datetime.now(),
                    nullable=False)
    updated = Column(DateTime,
                    index=False,
                    unique=False,
                    nullable=False,
                    default=datetime.datetime.now())
    created_by = Column(String(80),
                    nullable=False)
    updated_by = Column(String(80),
                    nullable=False)    
    """
    雙向ref做法
    child = relationship("BlogCategory",
                backref=backref('parent', remote_side=[id]))
    """
    parent_id = Column(Integer, ForeignKey('sub_product_category.id'))
    child = relationship("SubProductCategory",
                backref=backref('parent', remote_side=[id]))
    products = relationship('Product', secondary=product_subcategory, backref='SubProductCategory')
    def __repr__(self):
        return str(self.name)
    
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key = True)
    name = Column(String(100),
                         unique=True,
                         nullable=False)
    description = Column(String(300))
    price = Column(Integer)
    discount_percent = Column(Integer,default=0)
    discount_amount = Column(Integer,default=0)
    attribute = Column(JSON)
    #attribute : 
    """
        [
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
                            {'text':'女','image':''},            
        ]       
    """        
    lot_maintain=1 #庫存管理default是,否:不計算庫存量, 一律只顯示"有庫存"
    quantity_limit=0 #限購量d否,是:cart中, 同一商品數量, 無論訂購多少, 都顯示這個限量,並加註此商品有限購量
    image = Column(BLOB)
    small_image = Column(BLOB) #異動時由後台自動生成
    medium_image = Column(BLOB) #異動時由後台自動生成
    html_content_1 = Column(Text)
    html_content_2 = Column(Text)
    html_content_3 = Column(Text)
    link_content_1 = Column(JSON)
    link_content_2 = Column(JSON)
    link_content_3 = Column(JSON)    
    images_1 = Column(BLOB) #除代表圖外, 另可再秀5張圖, 應該夠...
    images_2 = Column(BLOB)
    images_3 = Column(BLOB)
    images_4 = Column(BLOB)
    images_5 = Column(BLOB)
    order = Column(Integer)
    active = Column(Boolean,default=False)
    created = Column(DateTime,
                    index=False,
                    unique=False,
                    default=datetime.datetime.now(),
                    nullable=False)
    updated = Column(DateTime,
                    index=False,
                    unique=False,
                    nullable=False,
                    default=datetime.datetime.now())
    created_by = Column(String(80),
                    nullable=False)
    updated_by = Column(String(80),
                    nullable=False)
    id_category = Column(Integer, ForeignKey('product_category.id'))
    category = relationship("ProductCategory", backref="product")
    sub_categorys = relationship('SubProductCategory', secondary=product_subcategory, backref='Product')
    
"""    
class ProductAttribute_M(Base):
    #""#"
    商品屬性主表:
        -關聯商品多對一,關聯明細表一對多
        -關聯sku明細表一對多, 
    ""#"
    __tablename__ = 'product_attribute_master'
    id = Column(Integer, primary_key = True)
    name = Column(String(50),
         nullable=False) 
    show_image = Column(Boolean,default=False)
    order = Column(Integer)
    created = Column(DateTime,
                    index=False,
                    unique=False,
                    default=datetime.datetime.now(),
                    nullable=False)
    updated = Column(DateTime,
                    index=False,
                    unique=False,
                    nullable=False,
                    default=datetime.datetime.now())
    created_by = Column(String(80),
                    nullable=False)
    updated_by = Column(String(80),
                    nullable=False)    
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", backref = "product_attribute_master")

class ProductAttribute_D(Base):
    #""#"
    商品屬性明細表:
        -關聯明細表一對多
        -關聯sku明細表一對多, 
    #""#"
    __tablename__ = 'product_attribute_details'
    id = Column(Integer, primary_key = True)
    name = Column(String(50),
         nullable=False)   
    image = Column(String(50),
         nullable=True)       
    attribute_id = Column(Integer, ForeignKey('product_attribute_master.id'))
    attribute = relationship("ProductAttribute_M", backref = "product_attribute_details") 
"""    

class ProductSku(Base):
    """ 商品sku主表:
        -關聯商品多對一,關聯明細表一對多
        -主要設定數量, 價位差異,sku 號碼(最好自動產生),
    """
    __tablename__ = 'product_sku'
    id = Column(Integer, primary_key = True)
    sku = Column(String(50), #從sku辨別屬性值
        unique=True,
        nullable=False)
    sku_details = Column(JSON)    
    quantity_lot = Column(Integer,nullable=False,default=0)
    quantity_sold = Column(Integer,nullable=False,default=0)
    price_add = Column(Integer,nullable=False,default=0)
    created = Column(DateTime,
                    index=False,
                    unique=False,
                    default=datetime.datetime.now(),
                    nullable=False)
    updated = Column(DateTime,
                    index=False,
                    unique=False,
                    nullable=False,
                    default=datetime.datetime.now())
    created_by = Column(String(80),
                    nullable=False)
    updated_by = Column(String(80),
                    nullable=False)    
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", backref = "product_sku")

"""
class ProductSku_D(Base):
    ""#" 商品sku明細表:
        -關聯ProductAttribute_M多對一,關聯ProductAttribute_D多對一
        
    ""#"
    __tablename__ = 'product_sku_details'
    id = Column(Integer, primary_key = True)
    name = Column(String(50),
         unique=True,
         nullable=False)  
    sku_id = Column(Integer, ForeignKey('product_sku_master.id'))
    sku = relationship("ProductSku_M", backref = "product_sku_details") 
    attribute_detail_id = Column(Integer, ForeignKey('product_attribute_details.id'))
    attribute_detail = relationship("ProductAttribute_D", backref = "product_sku_details") 
    attribute_master_id = Column(Integer, ForeignKey('product_attribute_master.id'))
    attribute_master = relationship("ProductAttribute_M", backref = "product_sku_details") 
    #backref means two way reference only set on one side. here is child side
                         
class ProductType(Base):
    __tablename__ = 'produc_type'
    id = Column(Integer, primary_key = True)
    name = Column(String(50),
                         unique=True,
                         nullable=False)
"""
                        
class ProductArticle(Base):
    __tablename__ = 'product_article'
    id = Column(Integer, primary_key = True)
    title = Column(String(60),unique=True)
    content = Column(Text)
    created = Column(DateTime,
                    index=False,
                    unique=False,
                    default=datetime.datetime.now(),
                    nullable=False)
    updated = Column(DateTime,
                    index=False,
                    unique=False,
                    nullable=False,
                    default=datetime.datetime.now())
    created_by = Column(String(80),
                    nullable=False)
    updated_by = Column(String(80),
                    nullable=False)    
                    
class ProductReview(Base):
    __tablename__ = 'product_review'
    id = Column(Integer, primary_key = True)
    review = Column(String(300)) #限300字內
    stars = Column(Integer) #0~10,每一點為半顆星
    created = Column(DateTime,
                    index=False,
                    unique=False,
                    default=datetime.datetime.now(),
                    nullable=False)
    """ 不提供修改
    updated = Column(DateTime,
                    index=False,
                    unique=False,
                    nullable=False,
                    default=datetime.datetime.now())

    updated_by = Column(String(80),
                    nullable=False)    
    """
    active = Column(Boolean,default=True) #後台可設定不顯示
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", backref = "product_review")     
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", backref = "product_review")                    
            
if __name__ == "__main__":
    print('test')