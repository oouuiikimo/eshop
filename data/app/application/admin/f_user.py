from wtforms import Form, StringField, TextField, validators,BooleanField
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL)
from wtforms.fields import SelectField,SelectMultipleField
import sqlalchemy

class PostForm(Form):
    title = StringField('Title', [validators.Length(min=4, max=5)])
    body = SelectField('body', coerce=int)

class UserForm(Form):
    
    """Contact form."""
    name = StringField('名稱', [
        DataRequired()],render_kw={'class':'form-control'})
    email = StringField('Email', [
        Email(message=('郵件格式有問題, 請確認')),
        DataRequired()],render_kw={'class':'form-control'}) 
    source = SelectField('帳號來源', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))], 
        render_kw={'class':'form-control'},
        choices = [('google', 'google'),
               ('facebook', 'facebook'),
               ('local', '本地')])
    roles = SelectMultipleField('權限', 
        #coerce=int, 
        render_kw={'class':'form-control'})
    active = BooleanField('有效', default='checked',
        render_kw={'class':'form-check-input'})        
  
        