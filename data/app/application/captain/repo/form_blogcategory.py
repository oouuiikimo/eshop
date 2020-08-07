from wtforms import (Form, StringField, TextField, validators,widgets,
    BooleanField,SelectMultipleField,SelectField,RadioField,TextAreaField, HiddenField)
from wtforms.validators import (DataRequired,ValidationError,
                                Email,
                                EqualTo,
                                Length,
                                URL)
from flask_wtf import CSRFProtect, FlaskForm
from .form_base import MultiCheckboxField,SelectCheckboxField

    
class UpdateForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('目錄名稱', [
        DataRequired(),Length(max=50)],
        render_kw={'class':'form-control','placeholder':'目錄名稱50字內,用以辨識,須唯一'})
    parent = SelectField('上層目錄',
        choices = [('','-- 請選擇 --')],
        render_kw={'class':'form-control'})    
    #is_leaf = BooleanField('最底層目錄', 
    #    render_kw={'class':'form-check-input'})
    is_leaf = RadioField('最底層目錄', 
        choices = [('1', '是'),('0', '否')],
        render_kw={'class':'custom-control-input'})     
        
    #"""
    def validate_is_leaf( form, field):
        from flask import current_app as app
        from ...models.db_article import BlogCategory
        has_articles = 0
        if form.id.data and field.data is False:
            with app.db_session.session_scope() as session: 
                has_articles = session.query(BlogCategory).filter(BlogCategory.parent_id==form.id.data).count()
                if has_articles>0:
                    raise Exception('這個類別尚有文章, 請先清空再取消文章類別')
        return field.data
    #"""    
        
class SearchForm(FlaskForm):  
      
    parent = SelectField('上層目錄', 
        choices = [('','-- 請選擇 --')],
        render_kw={'class':'form-control'})
    name = StringField('名稱', render_kw={'class':'form-control'})
    is_leaf = SelectField('最底層目錄',  
        choices = [('','-- 請選擇 --'),('1','是'),('0','否')],
        render_kw={'class':'form-control'})