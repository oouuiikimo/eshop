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

    name = StringField('商品名', [
        DataRequired()],
        render_kw={'class':'form-control','placeholder':'請輸入商品名,限100字內'})
    description = StringField('簡介', [
        DataRequired()],
        render_kw={'class':'form-control','placeholder':'請輸入簡介,限300字內..'}) 
    id_category = SelectField('主目錄',
        choices = [('','-- 請選擇 --')],
        render_kw={'class':'form-control'})
    image = TextAreaField('代表圖', [],
        render_kw={'class':'form-control editor'})
    active = RadioField('上架', 
        choices = [('1', '是'),('0', '否')],
        render_kw={'class':'custom-control-input'})
    
    
        
class SearchForm(FlaskForm):
    
    """Contact form."""
    name = StringField('名稱', 
        render_kw={'class':'form-control','style':'width:100px;'})
    description = StringField('簡介', 
        render_kw={'class':'form-control','style':'width:200px;'}) 
    active = SelectField('上架',  
        choices = [('','-- 請選擇 --'),('1','是'),('0','否')],
        render_kw={'class':'form-control'})        
    id_category = SelectField('主目錄',
        choices = [('','-- 請選擇 --')],
        render_kw={'class':'form-control'})      
        
    
    