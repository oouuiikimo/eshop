from sqlalchemy.orm import validates,load_only,relationship,backref
from sqlalchemy import (Integer,ForeignKey,String,DateTime,
    Column,Boolean,Text,JSON,Table,BLOB)
import datetime
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

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
    image = Column(BLOB)
    small_image = Column(BLOB) #異動時由後台自動生成
    medium_image = Column(BLOB) #異動時由後台自動生成
    html_content_1 = Column(Text)
    html_content_2 = Column(Text)
    html_content_3 = Column(Text)
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
    title (副標)
    other_information 
    description (商品內容)(有專門另一個功能存文章, 在此只存其連結)
    id_images -> db.LargeBinary (有專門另一個功能存圖檔, 在此只存其連結)
        -設定大小限制
        -(一對多, 關聯另一表格 product_images,需先存檔product , 才能到另一關聯表格上傳檔案)
        - 
        -images blob 
        儲存: https://pynative.com/python-sqlite-blob-insert-and-retrieve-digital-data/
        讀取: https://stackoverflow.com/questions/11017466/flask-to-return-image-stored-in-database
    active
    id_type (一對一, 且product type刪除需檢查是否使用中,建立variant時, 會參考到這個id 並取 productType中記錄的 attributes 設定)
    categories (db.array(db.string))(關聯另一表格)

    package_product 組合商品(建其它專用表格)
    related 相關商品(建其它專用表格)
    
    """  
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
    __tablename__ = 'product_sku_master'
    id = Column(Integer, primary_key = True)
    sku = Column(String(50), #從sku辨別屬性值
        unique=True,
        nullable=False)
    name = Column(String(50),
        nullable=False) 
    quantity_lot = Column(Integer,nullable=False)
    quantity_sold = Column(Integer,nullable=False)
    lot_number = Column(String(50),
        nullable=True)
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
    product = relationship("Product", backref = "product_sku_master")

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
    
"""
ProductCategory
"""
    
"""    
#class ProductVariant(db.Model):
    #sku 應用在此, 包裝或組合,規格..等等的唯一型號
    #todo:如何處理不同的組合, 規格呈現及資料儲存方式
    id
    sku
    product_id
    detail_id
    quanty
    price_add_type rate|amount
    price_add_value +-(?)

class ProductVariantDetail
"""
        
if __name__ == "__main__":
    print('test')