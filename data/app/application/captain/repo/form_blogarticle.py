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
    description = StringField('文章簡介', [
        DataRequired(),Length(max=200)],
        render_kw={'class':'form-control','placeholder':'文章簡介200字內,用於網頁搜尋的文章說明'})        
    content =  TextAreaField('文章內容', [],
        render_kw={'class':'form-control editor','placeholder':'請輸入文章內容....', 'rows': 20})
    id_category = SelectField('上層目錄',
        choices = [('','-- 請選擇 --')],
        render_kw={'class':'form-control'})    
    active = RadioField('上架', 
        choices = [('1', '是'),('0', '否')],
        render_kw={'class':'custom-control-input'})        
    tag = StringField('標簽', [],
        render_kw={'class':'form-control','data-role':"tagsinput"})
    
        
class SearchForm(FlaskForm):
    
    """Contact form."""
    title = StringField('文章標題', 
        render_kw={'class':'form-control'})
    active = SelectField('上架',  
        choices = [('','-- 請選擇 --'),('1','是'),('0','否')],
        render_kw={'class':'form-control'})        
    id_category = SelectField('上層目錄',
        choices = [('','-- 請選擇 --')],
        render_kw={'class':'form-control'})            
    tag = StringField('標簽', 
        render_kw={'class':'form-control'}) 