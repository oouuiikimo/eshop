#from sqlalchemy import Table, MetaData, Column, String, Integer, Text, create_engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import validates,load_only,relationship,backref
from sqlalchemy import Integer,ForeignKey,String,DateTime,Table,Column,Boolean,Text, create_engine
import datetime,re

from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()
engine = create_engine('sqlite:///dev.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(Text)

    def __repr__(self):
        return self.title

user_roles = Table('user_roles', Base.metadata,
    Column('id',Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('user.id')),
    Column('roles_id', Integer, ForeignKey('roles.id'))
    )

class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key = True)
    role = Column(String(20),unique=True,
                         nullable=False)
    users = relationship('User', secondary=user_roles, backref='Roles')
    def __repr__(self):
        return str(self.id)

class Dynamic(dict):
  """Dynamic objects are just bags of properties, some of which may happen to be functions"""
  def __init__(self, **kwargs):
    self.__dict__ = self
    self.update(kwargs)

  def __setattr__(self, name, value):
    import types    
    if isinstance(value, types.FunctionType):
      self[name] = types.MethodType(value, self)
    else:
      super(Dynamic, self).__setattr__(name, value)

class User(Base):
    """Model for user accounts."""

    __tablename__ = 'user'
    id = Column(Integer,
                   primary_key=True)
    name = Column(String(64),
                         index=False,
                         unique=True,
                         nullable=False)
    email = Column(String(80),
                      index=True,
                      unique=True,
                      nullable=False)
    created = Column(DateTime,
                        index=False,
                        unique=False,
                        default=datetime.datetime.now())
    password = Column(String(200),
                         primary_key=False,
                         unique=False,
                         nullable=True)
    source = Column(String(20),
                        nullable=False)
    active = Column(Boolean)                     
    bio = Column(Text,
                    index=False,
                    unique=False,
                    nullable=True)
    last_login = Column(DateTime,
                           index=False,
                           unique=False,
                           nullable=True)
    roles = relationship('Roles', secondary=user_roles, backref='User')
    
    @validates('email')
    def validate_email(self, key, email):
      if not email:
        raise ValidationError('郵件不能空白')
      if not re.match("[^@]+@[^@]+\.[^@]+", email):
        raise ValidationError('郵件格式錯誤!{}'.format(email))

      return email

    def login(self):
        self.last_login = datetime.datetime.now()
                           
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        if self.password and password:
            return check_password_hash(self.password, password)
        return False

    def __repr__(self):
        return '<User {}>'.format(self.name)
          
class PostRepo(object):
          
    def __init__(self):
        self.session = Session()
        #self.init_db()

    def init_db(self):
        user = User(name='tom',email='tom@your-tom.com',active=True,source='local')
        role = Roles(role='admin')
        user.roles.append(role)
        self.session.add(user)
        self.session.commit()
        
    def all(self):
        return self.session.query(Post).all()

    def create(self, title, body):
        post = Post(title=title, body=body)
        self.session.add(post)
        self.session.commit()
        return post

    def find(self, id):
        #todo:必須結合select 到roles model
        u={"id":1,"name":"tom","email":"oo@yppyy.cc","source":"facebook","active":1,"roles":[1]}
        d = Dynamic(**u)
        class U():
            def __init__(self):
                self.id = 1
                self.name = "tom"
        user = d #{"id":1,"name":"tom","email":"oo@yyy.cc","source":"google","active":1,"roles":[(1,"admin")]}
        return self.session.query(User).filter(User.id == id).first()

    def update(self, User):
        
        self.session.add(User)
        self.session.commit()

    def delete(self, post):
        self.session.delete(post)
        self.session.commit()
        
    def restore_roles(self,roles):
        #return User.roles
        if roles:
            roles = self.session.query(Roles).filter(Roles.id.in_(roles)).all()
            #User.roles =roles
            return roles
        return None
    def get_roles(self):
        return [(str(g.id), g.role) for g in self.session.query(Roles).all()]


Base.metadata.create_all(engine)