from wtforms import (Form, StringField, TextField, validators,widgets,
    BooleanField,SelectMultipleField,SelectField,RadioField)
from wtforms.validators import (DataRequired,ValidationError,
                                Email,
                                EqualTo,
                                Length,
                                URL)
from flask_wtf import CSRFProtect, FlaskForm

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SelectCheckboxField(SelectField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
    
    
    
class UpdateForm(FlaskForm):

    name = StringField('名稱', [
        DataRequired()],
        render_kw={'class':'form-control','placeholder':'請輸入帳號代表名稱'})
    email = StringField('Email', [
        Email(message=('郵件格式有問題, 請確認')),
        DataRequired()],
        render_kw={'class':'form-control','placeholder':'請輸入電子郵件位址'}) 
    source = SelectCheckboxField('帳號來源',  [DataRequired("沒有選擇來源")],
        render_kw={'class':'form-control'},
        choices = [('google', 'google'),
               ('facebook', 'facebook'),
               ('local', '本地')],
        default='local')
    roles = MultiCheckboxField('權限', 
        choices = [],#('1', 'admin'),('2', 'customer')],
        render_kw={'class':'form-control'})
    active = RadioField('有效', 
        choices = [('1', '有效'),('0', '失效')],
        render_kw={'class':'custom-control-input'})    
    
        
class SearchForm(FlaskForm):
    
    """Contact form."""
    name = StringField('名稱', 
        render_kw={'class':'form-control','style':'width:100px;'})
    email = StringField('Email', 
        render_kw={'class':'form-control','style':'width:200px;'}) 
    source = SelectField('帳號來源', 
        render_kw={'class':'form-control'},
        choices = [('','- 請選擇 -'),('google', 'google'),
               ('facebook', 'facebook'),
               ('local', '本地')])
    roles = SelectField('權限', 
        choices = [('','- 請選擇 -')],
        render_kw={'class':'form-control'})
    active = SelectField('有效', 
        render_kw={'class':'form-control'},
        choices = [('',' 請選擇 '),('1', '有效'),('0', '無效')])     
        
    
    