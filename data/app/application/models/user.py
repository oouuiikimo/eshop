from flask_login import UserMixin
from ..share.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates,load_only,relationship
import datetime,re
from wtforms.validators import ValidationError

user_roles = db.Table('user_roles',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('roles_id', db.Integer, db.ForeignKey('roles.id')))

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    role = db.Column(db.String(20),unique=True,
                         nullable=False)
    users = relationship('User', secondary=user_roles, backref='Roles')
    def __repr__(self):
        return str(self.role)

# used for query_factory 
def getRoles():
    fields = ['roles']
    a = Roles.query.all()
    return a


class User(UserMixin,db.Model):
    """Model for user accounts."""

    __tablename__ = 'user'
    id = db.Column(db.Integer,
                   primary_key=True)
    name = db.Column(db.String(64),
                         index=False,
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(80),
                      index=True,
                      unique=True,
                      nullable=False)
    created = db.Column(db.DateTime,
                        index=False,
                        unique=False,
                        default=datetime.datetime.now())
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=True)
    source = db.Column(db.String(20),
                        nullable=False)
    active = db.Column(db.Boolean)                     
    bio = db.Column(db.Text,
                    index=False,
                    unique=False,
                    nullable=True)
    last_login = db.Column(db.DateTime,
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
        
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False
         
    def get_id(self):
        return self.id  # python 3        
