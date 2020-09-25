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
    link_text = StringField('網址連結文字', [
        DataRequired(),Length(max=60)],
        render_kw={'class':'form-control','placeholder':'英文連結,空格以_取代,須唯一'})
    description = StringField('文章簡介', [
        DataRequired(),Length(max=60)],
        render_kw={'class':'form-control','placeholder':'文章簡介200字內,用於網頁搜尋的文章說明'})        
    content =  TextAreaField('文章內容', [],
        render_kw={'class':'form-control editor','placeholder':'請輸入文章內容....', 'rows': 20})
    
        
class SearchForm(FlaskForm):
    
    """Contact form."""
    title = StringField('文章標題', 
        render_kw={'class':'form-control'})
    link_text = StringField('網址連結文字', 
        render_kw={'class':'form-control'}) 
 
        
    
    