from flask_login import UserMixin
from ..share.models import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import validates
import datetime,re
from wtforms.validators import ValidationError

class User(UserMixin,db.Model):
    """Model for user accounts."""

    __tablename__ = 'users'
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
                        default=datetime.datetime.utcnow)
    password = db.Column(db.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=True)
    bio = db.Column(db.Text,
                    index=False,
                    unique=False,
                    nullable=True)
    last_login = db.Column(db.DateTime,
                           index=False,
                           unique=False,
                           nullable=True)

    @validates('email')
    def validate_email(self, key, email):
      if not email:
        raise ValidationError('郵件不能空白')
      if not re.match("[^@]+@[^@]+\.[^@]+", email):
        raise ValidationError('郵件格式錯誤!{}'.format(email))

      return email

    
                           
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)
