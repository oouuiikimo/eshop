from flask_admin.contrib.sqla import ModelView
from ...models import db,User
from flask import current_app as app
from wtforms.validators import ValidationError
from flask_admin.form import SecureForm

class UserView(ModelView):
    form_base_class = SecureForm #add csrf
    column_labels = {'username':'帳號', 'email':'郵箱','bio':'簡介','admin':'管理權限'
        ,'last_login':'最近登入','domain':'帳號來源','created':'建立日期'}
    column_exclude_list = ['password']    
    form_columns = ['username', 'email','domain','bio','admin'] #可新增的欄位
    page_size = 20
    column_searchable_list = ['email','username'] #搜尋
    column_filters = ['email','domain'] #過濾器
    form_choices = {'domain':[('google', 'google'),('facebook', 'facebook'),('local', '本地')]} #改select
    """
    def on_model_change(self, form, model, is_created):
        if str(form.email.data) != 'oouuii_kimo@yahoo.com.tw':
            raise ValidationError('email is wrong!{}:{}'.format(str(form.email.data),str(form.email.data) != 'oouuii_kimo@yahoo.com.tw'))
        else:
            return model
    """

db.init_app(app)    
UserModelView = UserView(User, db.session,name="管理员")    