from wtforms import (Form, StringField, TextField, validators,widgets,
    BooleanField,SelectMultipleField,SelectField,RadioField,TextAreaField)
from wtforms.validators import (DataRequired,ValidationError,
                                Email,
                                EqualTo,
                                Length,
                                URL)
from flask_wtf import CSRFProtect, FlaskForm
from .form_base import MultiCheckboxField,SelectCheckboxField

    
class UpdateForm(FlaskForm):

    title = StringField('文章標題', [
        DataRequired(),Length(max=60)],
        render_kw={'class':'form-control','placeholder':'文章標題60字內,用以辨識文章,須唯一'})     
    content =  TextAreaField('文章內容', [],
        render_kw={'class':'form-control editor','placeholder':'請輸入文章內容....', 'rows': 20})
    tag = StringField('標簽', [],
        render_kw={'class':'form-control','data-role':"tagsinput"})
        
class SearchForm(FlaskForm):
    
    """Contact form."""
    title = StringField('文章標題', 
        render_kw={'class':'form-control'})
    tag = StringField('標簽', [],
        render_kw={'class':'form-control'})