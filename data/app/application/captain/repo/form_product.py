from wtforms import (Form, StringField, TextField, validators,widgets,IntegerField,
    BooleanField,SelectMultipleField,SelectField,RadioField,TextAreaField,
    HiddenField,FileField)
from wtforms.validators import (DataRequired,ValidationError,
                                Email,
                                EqualTo,
                                Length,
                                URL)
from flask_wtf import CSRFProtect, FlaskForm
from .form_base import MultiCheckboxField,SelectCheckboxField,HiddenSelect

#依repo_sub 會有許多 UpdateForm    

class Update_basic_Form(FlaskForm):
    name = StringField('名稱', [
        DataRequired(),Length(max=100)],
        render_kw={'class':'form-control','placeholder':'商品名稱100字內,須唯一'})    
    sku = StringField('型號', [
        DataRequired(),Length(max=20)],
        render_kw={'class':'form-control','placeholder':'商品型號20字內,須唯一'})    
    description =  TextAreaField('商品搜尋頁簡介', [],
        render_kw={'class':'form-control','placeholder':'300字內', 'rows': 20})  
    order = SelectField('排序', choices=[(3, '-請選擇顯示排序-'),(1, '熱銷優先'), (2, '推廣'), (3, '一般'), (4, '過季品'), (5, '不推廣')],
        render_kw={'class':'form-control'}, coerce=int)  
    category = SelectField('主目錄', 
        choices = [('', '-請選擇目錄-')],
        render_kw={'class':'form-control'})
    isvariant = SelectField('屬性商品', 
        choices = [('1', '多屬性商品'),('0', '單一屬性商品')],
        default='0',
        render_kw={'class':'form-control','disabled':True})   
    active = RadioField('上架', 
        choices = [('1', '上架'),('0', '下架')],
        default='0',
        render_kw={'class':'custom-control-input'})          
        
class Insert_basic_Form(FlaskForm):
    name = StringField('名稱', [
        DataRequired(),Length(max=100)],
        render_kw={'class':'form-control','placeholder':'商品名稱100字內,須唯一'})    
    sku = StringField('型號', [
        DataRequired(),Length(max=20)],
        render_kw={'class':'form-control','placeholder':'商品型號20字內,須唯一'})    
    description =  TextAreaField('商品搜尋頁簡介', [],
        render_kw={'class':'form-control','placeholder':'300字內', 'rows': 20})  
    order = SelectField('排序', choices=[(3, '-請選擇顯示排序-'),(1, '熱銷優先'), (2, '推廣'), (3, '一般'), (4, '過季品'), (5, '不推廣')],
        render_kw={'class':'form-control'}, coerce=int)  
    category = SelectField('主目錄', 
        choices = [('', '-請選擇目錄-')],
        render_kw={'class':'form-control'})
    isvariant = RadioField('屬性商品', 
        choices = [('1', '多屬性商品'),('0', '單一屬性商品')],
        default='0',
        render_kw={'class':'custom-control-input'})   
    active = RadioField('上架', 
        choices = [('1', '上架'),('0', '下架')],
        default='0',
        render_kw={'class':'custom-control-input'})  
        
class Update_variant_Form(FlaskForm):
    variant = SelectField('商品適用屬性', [DataRequired()],
        choices = [('', '-請選擇目錄-')],
        render_kw={'class':'form-control'})  
    original = HiddenField('original',default=0)    

class Update_subcategory_Form(FlaskForm):
    subcategory = SelectField('其它分類', 
        DataRequired(),choices = [('', '-請選擇目錄-')],
        render_kw={'class':'form-control'})
    original = HiddenField('original',default=0)    
        
class Update_sku_Form(FlaskForm):
    sku = StringField('副型號',
        render_kw={'class':'form-control','readonly':True})
    price = IntegerField('價格', [DataRequired(message="請輸入價格(數字)")],
        render_kw={'class':'form-control'})
    quantity = IntegerField('存量', [DataRequired(message="請輸入存量(數字)")],
        render_kw={'class':'form-control'},default=0)
    lot_maintain = RadioField('庫存管理', 
        choices = [('1', '是'),('0', '否')],
        default='0',
        render_kw={'class':'custom-control-input'})
    active = RadioField('上架', 
        choices = [('1', '上架'),('0', '下架')],
        default='0',
        render_kw={'class':'custom-control-input'})

class Update_skus_Form(FlaskForm):
    sku = StringField('副型號',
        render_kw={'class':'form-control'})
    price = IntegerField('價格', [DataRequired(message="請輸入價格(數字)")],
        render_kw={'class':'form-control'})
    quantity = IntegerField('存量', [DataRequired(message="請輸入存量(數字)")],
        render_kw={'class':'form-control'},default=0)
    lot_maintain = RadioField('庫存管理', 
        choices = [('1', '是'),('0', '否')],
        default='0',
        render_kw={'class':'custom-control-input'})
    active = RadioField('上架', 
        choices = [('1', '上架'),('0', '下架')],
        default='0', 
        render_kw={'class':'custom-control-input'})
    #todo:要有一個input 是可以存所選的屬性值, 不管有幾個屬性, 或沒有
    #
    values = HiddenField('屬性值')
    variantvalues_source = HiddenSelect('variantvalues_source',
        choices=[(0,'-請選擇-')], coerce= int,
        render_kw={'class':'d-none'})
        
class Update_image_Form(FlaskForm):
    file_name = HiddenField('商品圖片', [
        DataRequired(),Length(max=40)],
        render_kw={'class':'form-control'})
    file = FileField('圖片',
        render_kw={'class':'d-none'})    
    watermark = BooleanField('加浮水印')
    fill_or_crop = RadioField('縮放方式', 
        choices = [('1', '填滿'),('0', '裁切')],
        default='0',
        render_kw={'class':'custom-control-input'})
    active = RadioField('上架', 
        choices = [('1', '上架'),('0', '下架')],
        render_kw={'class':'custom-control-input'})
        
class Update_article_Form(FlaskForm):
    title = StringField('文章標題', [
        DataRequired(),Length(max=60)],
        render_kw={'class':'form-control','placeholder':'文章標題60字內,用以辨識文章,須唯一'})     
    content =  TextAreaField('文章內容', [],
        render_kw={'class':'form-control editor','placeholder':'請輸入文章內容....', 'rows': 20})    

class Update_active_Form(FlaskForm):
    active = RadioField('上架', 
        choices = [('1', '上架'),('0', '下架')],
        render_kw={'class':'custom-control-input'})  
    
class SearchForm(FlaskForm):
    
    """Contact form."""
    name = StringField('商品名稱', 
        render_kw={'class':'form-control'})
