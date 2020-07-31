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

class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key = True)
    title = Column(String(50),
                         unique=True,
                         nullable=False) 
    content = Column(Text)
    active = Column(Boolean)
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
    author = Column(String(80),
                           nullable=False)
    category_id = Column(Integer, ForeignKey('articlecategory.id'))
    category = relationship("ArticleCategory", backref="article")                       


                           
class ArticleCategory(Base):

    __tablename__ = "articlecategory"
    id = Column(Integer, primary_key = True)
    name = Column(String(50),
                         unique=True,
                         nullable=False)
    is_leaf = Column(Boolean,nullable=False,default=False)
    """
    雙向ref做法
    child = relationship("ArticleCategory",
                backref=backref('parent', remote_side=[id]))
    """
    parent_id = Column(Integer, ForeignKey('articlecategory.id'))
    child = relationship("ArticleCategory",
                backref=backref('parent', remote_side=[id]))
                
    @validates('is_leaf')
    def validate_is_leaf(self, key, is_leaf):
        has_articles = 0
        if is_leaf is False:
            has_articles = Article.query.filter(Article.category_id==self.id).count()
            if has_articles>0:
                raise Exception('這個類別尚有文章, 請先清空再取消文章類別')
        return is_leaf
    
    @classmethod
    def is_has_child(cls,id):
        has_child = ArticleCategory.query.filter(ArticleCategory.parent_id==id).count()
        #result = ArticleCategory.query.filter(ArticleCategory.id.in_([i.parent_id for i in has_child])).count()
        return has_child #.with_entities(func.count(ArticleCategory.id)).scalar()
    
    @classmethod
    def get_tree(cls,id=None):
        """更新或新增表單用,顯示上層目錄供歸屬:
            .不能列出參考列的下層,只能列上層, is_leaf=True, 不然會形成迴圏, 
        """
        def func():
            statement = text(
            """
            WITH RECURSIVE category_path (id, path) AS
            (
              SELECT id, name as path
                FROM articlecategory
                WHERE parent_id ==:id /*IS NULL or ==2*/
                
              UNION ALL
              SELECT c.id,  cp.path|| ' > '|| c.name as path
                FROM category_path AS cp JOIN articlecategory AS c
                  ON cp.id = c.parent_id
            )
            SELECT * FROM category_path
            ORDER BY path;
            """)
            if id:
                child = [i.id for i in db.session.execute(statement,{"id":id})]
                child.append(id) #自己以及下層, 都不能出現
                return ArticleCategory.query.filter(ArticleCategory.id.notin_(child),ArticleCategory.is_leaf==False).all()
            else:
                #is_leaf 不能出現
                return ArticleCategory.query.filter(ArticleCategory.is_leaf == False ).all()
        
        return func

    @classmethod
    def get_tree_for_search(cls):
        """搜尋表單, 欄位下接選擇項:不需列出最下層 is_leaf is False
        """
        #has_child = db.session.query(ArticleCategory.parent_id).distinct()
        #return ArticleCategory.query.filter(ArticleCategory.id.in_([i.parent_id for i in has_child])).all()
        return ArticleCategory.query.filter(ArticleCategory.is_leaf == False).all()

    @classmethod
    def get_tree_for_article(cls):
        """文章表單用:不列出含有下層目錄的母層, 只列子層-> is_leaf is True
        """

        #注意以下, notin 裡面必須排除掉 null 否則, 結果會不正確
        #has_child = db.session.query(ArticleCategory.parent_id).filter(ArticleCategory.parent_id.isnot(None)).distinct()
        #return ArticleCategory.query.filter(ArticleCategory.id.notin_(has_child)).all()
        return ArticleCategory.query.filter(ArticleCategory.is_leaf == True).all()
        
    def __repr__(self):
        statement = text(
        """
        WITH RECURSIVE category_path (id, path) AS
        (
          SELECT id, name as path
            FROM articlecategory
            WHERE parent_id IS NULL
          UNION ALL
          SELECT c.id,  cp.path|| ' > '|| c.name as path
            FROM category_path AS cp JOIN articlecategory AS c
              ON cp.id = c.parent_id
        )
        SELECT * FROM category_path
        where id == :id;
        """)
        if self.parent:
            tree = db.session.execute(statement,{"id":self.id}).first()
            return tree.path

        return self.name
        
if __name__ == "__main__":
    print('test')