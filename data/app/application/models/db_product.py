from sqlalchemy.orm import validates,load_only,relationship,backref
from sqlalchemy import Integer,ForeignKey,String,DateTime,Column,Boolean,Text,JSON
import datetime
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class ProductAttribute(Base):
    __tablename__ = 'product_attribute'
    id = Column(Integer, primary_key = True)
    name = Column(String(50),
                         unique=True,
                         nullable=False) 
                         
class ProductType(Base):
    __tablename__ = 'produc_type'
    id = Column(Integer, primary_key = True)
    name = Column(String(50),
                         unique=True,
                         nullable=False)
    attributes = Column(JSON) 
    
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key = True)
    name = Column(String(100),
                         unique=True,
                         nullable=False)
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
ProductCategory
"""
    
"""    
#class ProductVariantMaster(db.Model):
    id
    product_id
    detail_id
    quanty
    price_add_type rate|amount
    price_add_value +-(?)

class ProductVariantDetail
"""
        
if __name__ == "__main__":
    print('test')