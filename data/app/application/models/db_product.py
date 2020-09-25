from sqlalchemy.orm import validates,load_only,relationship,backref
from sqlalchemy import (Integer,ForeignKey,String,DateTime,
    Column,Boolean,Text,JSON,Table,BLOB)
import datetime
from sqlalchemy.sql import text
from .db_base import Base

product_subcategory = Table('product_subcategory', Base.metadata,
    Column('id',Integer, primary_key=True),
    Column('id_product', Integer, ForeignKey('product.id')),
    Column('id_subcategory', Integer, ForeignKey('sub_product_category.id'))
    )

product_variant = Table('product_variant', Base.metadata,
    Column('id',Integer, primary_key=True),
    Column('id_product', Integer, ForeignKey('product.id')),
    Column('id_variant', Integer, ForeignKey('variant.id'))
    )
    
productsku_value = Table('productsku_value', Base.metadata,
    Column('id',Integer, primary_key=True),
    Column('id_product_sku', Integer, ForeignKey('product_sku.id')),
    Column('id_variant_values', Integer, ForeignKey('variant_values.id'))
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
    id_parent = Column(Integer, ForeignKey('product_category.id'))
    child = relationship("ProductCategory",
                backref=backref('parent', remote_side=[id]))
                
    def __repr__(self):
        return (self.id,self.name)
    def __str__(self):
        return str(f'{self.id}:{self.name}')
        
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
    id_parent = Column(Integer, ForeignKey('sub_product_category.id'))
    child = relationship("SubProductCategory",
                backref=backref('parent', remote_side=[id]))
    products = relationship('Product', secondary=product_subcategory, backref='SubProductCategory')
    def __repr__(self):
        return (self.id,self.name)
    def __str__(self):
        return str(f'{self.id}:{self.name}')
    
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key = True)
    name = Column(String(100),
                         unique=True,
                         nullable=False)
    description = Column(String(300))
    #price = Column(Integer)
    #discount_percent = Column(Integer,default=0)
    #discount_amount = Column(Integer,default=0)
    #lot_maintain=1 #庫存管理default是,否:不計算庫存量, 一律只顯示"有庫存"
    #quantity_limit=0 #限購量d否,是:cart中, 同一商品數量, 無論訂購多少, 都顯示這個限量,並加註此商品有限購量
    image = Column(String(22),unique=True)
    sku = Column(String(20), #從sku辨別屬性值
        unique=True,
        nullable=False)
    isvariant = Column(Boolean,default=False)
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
    category = relationship("ProductCategory", backref="Product")
    sub_categorys = relationship('SubProductCategory', secondary=product_subcategory, backref='Product')
    images = relationship("ProductImage", backref="Product",cascade="all, delete")
    articles = relationship("ProductArticleMaster", backref="Product",cascade="all, delete")
    skus = relationship("ProductSku", backref = "Product",cascade="all, delete")
    variants = relationship('Variant', secondary=product_variant, backref='Product')
    def __repr__(self):
        return (self.id,self.name)
    def __str__(self):
        return str(f'{self.id}:{self.name}')
    
class ProductImage(Base):
    __tablename__ = 'product_image'
    id = Column(Integer, primary_key = True)
    id_product = Column(Integer, ForeignKey('product.id'))
    file_name = Column(String(40),unique=True,
        nullable=False) #sku_short_uuid.jpg

class Variant(Base):
    __tablename__ = 'variant'
    id = Column(Integer, primary_key = True)
    variant= Column(String(20))
    values = relationship("VariantValues",  backref="Variant", cascade="all, delete")
    products = relationship('Product', secondary=product_variant, backref='Variant')

    def __repr__(self):
        return (self.id,self.variant)
    def __str__(self):
        return str(f'{self.id}:{self.variant}')        
    
class ProductSku(Base):
    """ 商品sku主表:
        -關聯商品多對一,關聯明細表一對多
        -主要設定數量, 價位差異,sku 號碼(最好自動產生),
    """
    __tablename__ = 'product_sku'
    id = Column(Integer, primary_key = True)
    sku = Column(String(20), #從sku辨別屬性值
        nullable=False)  
    quantity = Column(Integer,nullable=False,default=0)
    price = Column(Integer,nullable=False,default=0)  
    active = Column(Boolean,default=False)
    lot_maintain = Column(Boolean,default=False)
    id_product = Column(Integer, ForeignKey('product.id'))
    values = relationship('VariantValues', secondary=productsku_value, backref='ProductSku', cascade="all, delete")

    def __repr__(self):
        return (self.id,self.sku)
    def __str__(self):
        return str(f'{self.id}:{self.sku}')      

class VariantValues(Base):
    __tablename__ = 'variant_values'
    id = Column(Integer, primary_key = True)
    value = Column(String(20))
    order = Column(Integer)
    id_variant = Column(Integer, ForeignKey('variant.id'))
    #variant = relationship("Variant",  back_populates="VariantValues")

    def __repr__(self):
        return (self.id,self.value)
    def __str__(self):
        return str(f'{self.id}:{self.value}')   
    
product_article_details = Table('product_article_details', Base.metadata,
    Column('id',Integer, primary_key=True),
    Column('id_product_article', Integer, ForeignKey('product_article.id')),
    Column('id_product_article_master', Integer, ForeignKey('product_article_master.id'))
    )
    
class ProductArticle(Base):
    __tablename__ = 'product_article'
    id = Column(Integer, primary_key = True)
    name = Column(String(60),unique=True)
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
    article_details = relationship('ProductArticleMaster', secondary=product_article_details, backref='ProductArticle')
    #article_details = relationship("ProductArticleDetails", backref="article")

    
class ProductArticleMaster(Base): # 為為product article 的details 表格
    __tablename__ = 'product_article_master'
    id = Column(Integer, primary_key = True)   
    id_product = Column(Integer, ForeignKey('product.id'))
    title = Column(String(60)) #商品內的文章標題, 像是商品說明, 退換貨說明, 規格...等等,會有重複
    order = Column(Integer)
    articles = relationship('ProductArticle', secondary=product_article_details,
        backref='ProductArticleMaster',cascade="all, delete")

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
    active = Column(Boolean,default=True) #後台可設定不顯示
    customer_id = Column(Integer, ForeignKey('customer.id'))
    customer = relationship("Customer", backref = "product_review")
    product_id = Column(Integer, ForeignKey('product.id'))
    product = relationship("Product", backref = "product_review")                    
            
if __name__ == "__main__":
    print('test')