from sqlalchemy.orm import validates,load_only,relationship,backref
from sqlalchemy import (Integer,ForeignKey,String,DateTime,
    Column,Boolean,Text,JSON,Table,BLOB)
import datetime
from sqlalchemy.sql import text
from .db_base import Base


class Customer(Base):

    __tablename__ = "customer"
    id = Column(Integer, primary_key = True)
    name = Column(String(50),
                         unique=True,
                         nullable=False)
    email = Column(String(80),
                      index=True,
                      unique=True,
                      nullable=False)
    active = Column(Boolean,default=False)
    password = Column(String(200),
                         primary_key=False,
                         unique=False,
                         nullable=True)
    source = Column(String(20),
                        unique=False,
                         nullable=True)
    social_id = Column(String(50),
                        unique=True)
    photo = Column(BLOB(200),
                    index=False,
                    unique=False,
                    nullable=True)
    last_login = Column(DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    point_ordered = Column(Integer) # 訂購積分 (每多少元一個積分)
    point_logon = Column(Integer) # 到訪積分
    point_returned = Column(Integer) # 退貨積分 (每多少元一個積分)
    point_abandon = Column(Integer) # 退訂積分 (棄購物車:一定時間內無結帳,則認訂放棄,以次數計)
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
                    