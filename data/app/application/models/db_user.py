from sqlalchemy.orm import validates,load_only,relationship,backref
from sqlalchemy import Integer,ForeignKey,String,DateTime,Table,Column,Boolean,Text
import datetime,re

from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


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
        return str(self.role)

# used for query_factory 
def getRoles(session):
    fields = ['roles']
    a = session.query(Roles).all()
    return a


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
                        unique=False,
                         nullable=True)
    social_id = Column(String(50),
                        unique=True)
    active = Column(Boolean)                     
    photo = Column(String(200),
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

    def update_last_login(self):
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
          
