from sqlalchemy.orm import validates,load_only,relationship,backref
from sqlalchemy import Integer,ForeignKey,String,DateTime,Column,Boolean,Text,JSON
import datetime
from sqlalchemy.sql import text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class BlogArticle(Base):
    __tablename__ = 'blog_article'
    id = Column(Integer, primary_key = True)
    tag = Column(JSON)
    description = Column(String(200))
    title = Column(String(60),unique=True)
    active = Column(Boolean,default=False)
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
    id_category = Column(Integer, ForeignKey('blog_category.id'))
    category = relationship("BlogCategory", backref="blog_article")
    
class SiteArticle(Base):
    __tablename__ = 'site_article'
    id = Column(Integer, primary_key = True)
    description = Column(String(200))
    link_text = Column(String(60),unique=True) #連結網址
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
                    
class ProductArticle(Base):
    __tablename__ = 'product_article'
    id = Column(Integer, primary_key = True)
    tag = Column(JSON) #搜尋用
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


class BlogCategory(Base):
    #todo: 有些function 要cache
    
    __tablename__ = "blog_category"
    id = Column(Integer, primary_key = True)
    name = Column(String(50),
                         unique=True,
                         nullable=False)
    is_leaf = Column(Boolean,nullable=False,default=False)
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
    parent_id = Column(Integer, ForeignKey('blog_category.id'))
    child = relationship("BlogCategory",
                backref=backref('parent', remote_side=[id]))
                

