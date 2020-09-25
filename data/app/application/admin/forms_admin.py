from flask import g,current_app as app
from flask_login import current_user
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, TextField, SubmitField,validators,SelectMultipleField,PasswordField,BooleanField \
,IntegerField,HiddenField,SelectField,ValidationError,TextAreaField
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL)
from wtforms_sqlalchemy.fields import QuerySelectField,QuerySelectMultipleField
from ..models.user import User,Roles,getRoles,user_roles
from ..models.product import ProductAttribute,ArticleCategory,Article
from ..share.helpers import Pagination
from sqlalchemy import func,exc
import datetime,re
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
"""
 fix Flask WTForms and WTForms-SQLAlchemy QuerySelectField produce too many values to unpack 
"""
from ..models.fix_wtf_sql import fix_wtfsql
fix_wtfsql()

def mapUpdateForm(model,id=None):
        
    class BaseForm(FlaskForm):

        @classmethod
        def update_data(cls,form,item):
            try:
                form.populate_obj(item)
                db.session.add(item)  
                db.session.commit()
            except exc.SQLAlchemyError as e:
                """ 捕獲錯誤, 否則無法回傳
                """
                db.session().rollback()   
                error = str(e.__dict__['orig'])
                raise Exception(error)
                #raise Exception('資料庫更新失敗!!')
            

        @classmethod
        def insert_data(cls,form,item):
            try:
                form.populate_obj(item)
                db.session.add(item)  
                db.session.commit()
            except exc.SQLAlchemyError as e:
                """ 捕獲錯誤, 否則無法回傳
                """
                db.session().rollback()   
                error = str(e.__dict__['orig'])
                raise Exception(error)
                #raise Exception('資料庫新增失敗!!')
            
        @classmethod
        def get_count(cls,q):
            count_q = q.statement.with_only_columns([func.count()]).order_by(None)
            count = q.session.execute(count_q).scalar()
            return count
        
        @classmethod
        def get_query(cls,filters,page,per_page):
            import math
            page=int(page)
            per_page=int(per_page)
            #get all rows before doing pagination !!
            q = cls.get_model().query.filter(*filters)
            q_count = cls.get_count(q)
            #修正不正確的頁數顯示
            if (page-1)*per_page > q_count:
                page = math.ceil(q_count / per_page)
            return page,q_count,q.limit(per_page).offset((page-1)*per_page).all()
            
        @classmethod
        def get_form(cls,id=None):
            update_layout = cls.get_layout()
            if id: #"""for update"""
                item = cls.get_model().query.get(id)
                form = cls(obj=item)
            else: #"""for insert"""
                item = cls.get_model()() # 這裡不能只回傳function , 再實例它才可以:()()
                form = cls()

            return form,item,update_layout
        @classmethod
        def get_pagination(cls,total,page=1, per_page=10):     
            #total = cls.get_total()
            return Pagination(page, per_page, total)
            
        @classmethod
        def get_list(cls,page=1,per_page=10,search=None):
            filters = cls.get_search_filters(search)
         
            page,count,rows = cls.get_query(filters,page,per_page) 
            out_rows = cls.get_listrows(rows)

            return page,out_rows, cls.get_pagination(count,page,per_page)   
         
        @classmethod
        def get_template(cls):
            return 'update.html'    
            
        @classmethod
        def format_datetime(cls,_datetime):
            return _datetime.strftime("%Y/%m/%d %H:%M") #not second :%S
        
    class UpdateArticle(BaseForm):
        title = StringField('標題', [
            DataRequired()],render_kw={'class':'form-control'})
        active = BooleanField('有效', 
            render_kw={'class':'form-check-input'})
        category = QuerySelectField('上層', 
            query_factory=ArticleCategory.get_tree_for_article,
            allow_blank=True, 
            render_kw={'class':'form-control'}) #todo: 若是母層, 則不能被指定為文章類別
        content = TextAreaField('內容',[
            DataRequired()],render_kw={'class':'form-control','id':'editor'}) #init ckeditor 必須參照這裡的做法:TextAreaField,'id':'editor'
        
        submit = SubmitField('存檔', 
            render_kw={'class':'btn btn-default'})
        
        @classmethod
        def update_data(cls,form,item):
            form.populate_obj(item)
            #item.author = g.user.email
            item.updated = datetime.datetime.now()  
            db.session.add(item)  
            db.session.commit()

        @classmethod
        def insert_data(cls,form,item):
            form.populate_obj(item)
            item.author = g.user.email
            db.session.add(item)  
            db.session.commit()            
            
        @classmethod
        def get_fields(cls):
            return [('name','名稱'),('category','類別'),('active','有效'),('created','建立日'),('updated','更新日'),('author','作者')]
           
        @classmethod
        def get_model(cls):
            return Article
        
        @classmethod
        def get_search_filters(cls,search):
            model = cls.get_model()
            filters = []
            if search:
                if 'title' in search and search.title.data:
                    filters.append(model.title.like('%{}%'.format(search.title.data)))
                if 'content' in search and search.content.data:
                    filters.append(model.content.like('%{}%'.format(search.content.data)))
                if 'author' in search and search.author.data:
                    filters.append(model.author.like('%{}%'.format(search.author.data)))
                if 'category' in search and search.category.data:
                    statement = db.text(
                    """
                    WITH RECURSIVE category_path (id, path) AS
                    (
                      SELECT id, name as path
                        FROM articlecategory
                        WHERE parent_id ==:id /*IS NULL or ==2*/
                      UNION ALL
                      SELECT c.id,  cp.path|| ' > '|| c.name as path
                        FROM category_path AS cp JOIN articlecategory AS c
                          ON cp.id = c.parent_id
                    )
                    SELECT * FROM category_path
                    ORDER BY path;
                    """)
                    #child = [i.id for i in db.session.execute(statement,{"id":search.category.data.id})]
                    #filters.append(model.category_id.in_(child))
                    filters.append(model.category_id==search.category.data.id)
            return filters
                        
        @classmethod
        def get_listrows(cls,rows):
            out_rows = []
            for row in rows:
                out_rows.append(['<input type="checkbox" name="delete" value="{}">'.format(row.id),
                    '<a href="/admin/update/Articles/Article/{}">{}</a>'.format(row.id,row.title),
                    row.category if row.category else "無" ,'有效' if row.active else '失效',
                    cls.format_datetime(row.created),cls.format_datetime(row.updated),row.author])
            return out_rows
            
        @classmethod
        def get_layout(cls): 
            return [
                    ['title'],['active','category'],['content']
                ]    
 
    class UpdateArticleCategory(BaseForm):
        #todo: 
        # .validate 要加上自己上層不能是自己下層
        # .validate 若有下層不能刪除
        # .validate 若文章目錄有文章, 不能刪除
        name = StringField('名稱', [
            DataRequired()],render_kw={'class':'form-control'})
        parent = QuerySelectField('上層', 
            query_factory=ArticleCategory.get_tree(id),
            allow_blank=True, 
            render_kw={'class':'form-control'})
        is_leaf = BooleanField('文章目錄', 
            render_kw={'class':'form-check-input'})

        submit = SubmitField('存檔', 
            render_kw={'class':'btn btn-default'}) 
                               
        @classmethod
        def get_fields(cls):
            return [('name','名稱'),('parent','上層'),('is_leaf','文章目錄')]
           
        @classmethod
        def get_model(cls):
            return ArticleCategory

        @classmethod
        def get_form(cls,id=None):
            update_layout = cls.get_layout()
            if id: #"""for update"""
                """ 自訂表單輸出:若是母層,把is_leaf 欄位拿掉 
                """
                item = cls.get_model().query.get(id)
                form = cls(obj=item)
                if ArticleCategory.is_has_child(id):
                    del form.is_leaf
                    update_layout[0].remove('is_leaf')

            else: #"""for insert"""
                item = cls.get_model()() # 這裡不能只回傳function , 再實例它才可以:()()
                form = cls()
            return form,item,update_layout
        
        @classmethod
        def get_search_filters(cls,search):
            model = cls.get_model()
            filters = []
            if search:
                if 'name' in search and search.name.data:
                    filters.append(model.name.like('%{}%'.format(search.name.data)))
                if 'parent' in search and search.parent.data:
                    statement = db.text(
                    """
                    WITH RECURSIVE category_path (id, path) AS
                    (
                      SELECT id, name as path
                        FROM articlecategory
                        WHERE parent_id ==:id /*IS NULL or ==2*/
                      UNION ALL
                      SELECT c.id,  cp.path|| ' > '|| c.name as path
                        FROM category_path AS cp JOIN articlecategory AS c
                          ON cp.id = c.parent_id
                    )
                    SELECT * FROM category_path
                    ORDER BY path;
                    """)
                    child = [i.id for i in db.session.execute(statement,{"id":search.parent.data.id})]
                    filters.append(model.id.in_(child))
            return filters
                        
        @classmethod
        def get_listrows(cls,rows):
            out_rows = []
            for row in rows:
                out_rows.append(['<input type="checkbox" name="delete" value="{}">'.format(row.id),
                    '<a href="/admin/update/Articles/ArticleCategory/{}">{}</a>'.format(row.id,row.name),
                row.parent if row.parent else "無",
                "文章目錄" if row.is_leaf else "類別目錄"])
            return out_rows
            
        @classmethod
        def get_layout(cls): 
            return [
                    ['name','parent','is_leaf']
                ]    
    
    class UpdateProductAttribute(BaseForm):
        name = StringField('屬性名稱', [
            DataRequired()],render_kw={'class':'form-control'})
        submit = SubmitField('存檔', 
            render_kw={'class':'btn btn-default'})    
           
        @classmethod
        def get_fields(cls):
            return [('name','名稱')]    
           
        @classmethod
        def get_model(cls):
            return ProductAttribute
        
        @classmethod
        def get_search_filters(cls,search):
            model = cls.get_model()
            filters = []
            if search:
                if 'name' in search and search.name.data:
                    filters.append(model.name.like('%{}%'.format(search.name.data)) )
            return filters

        @classmethod
        def get_listrows(cls,rows):
            out_rows = []
            for row in rows:
                out_rows.append(['<input type="checkbox" name="delete" value="{}">'.format(row.id),
                    '<a href="/admin/update/Products/ProductAttribute/{}">{}</a>'.format(row.id,row.name)])
            return out_rows
            
        @classmethod
        def get_layout(cls): 
            return [
                    ['name']
                ]
            
    class UpdateUser(BaseForm):
    
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
        roles = QuerySelectMultipleField('權限', 
            query_factory=getRoles, 
            render_kw={'class':'form-control'})
        active = BooleanField('有效', 
            render_kw={'class':'form-check-input'})        

        submit = SubmitField('存檔', 
            render_kw={'class':'btn btn-default'})    
        
        @classmethod
        def get_model(cls):
            return User
            
        @classmethod
        def update_data(cls,form,item):
            form.populate_obj(item)
            db.session.add(item)
            item.roles.clear()
            for role in form.roles.data:
                item.roles.append(role)        
            db.session.commit()
            
        @classmethod
        def get_fields(cls):
            return [('name','名稱'),('email','郵箱'),('active','有效'),('source','來源'),('roles','權限')]    

        @classmethod
        def get_search_filters(cls,search):
            filters = []
            if search:
                if 'name' in search and search.name.data:
                    filters.append(User.name==search.name.data)
                if 'email' in search and search.email.data:
                    filters.append(User.email.like('%{}%'.format(search.email.data)) )            
                if 'source' in search and search.source.data:
                    filters.append(User.source==search.source.data)   
                if 'roles' in search and search.roles.data:
                    filters.append(User.roles.any(Roles.role==search.roles.data.role))
                if 'active' in search and search.active.data:
                    filters.append(User.active==search.active.data)    
            return filters

        @classmethod
        def get_listrows(cls,rows):
            out_rows = []
            for row in rows:
                out_rows.append(['<input type="checkbox" name="delete" value="{}">'.format(row.id),
                    '<a href="/admin/update/Accounts/User/{}">{}</a>'.format(row.id,row.name),
                    row.email,'有效' if row.active else '失效',row.source,'<a href="/admin/update/UserRoles/{}">{}</a>'.format(row.id,row.roles)])
            return out_rows
            
        @classmethod
        def get_layout(cls): 
            return [
                    ['name','email','source'],
                    ['roles','active']
                ]

    class UserRolesForm(BaseForm):
        #from ..models.user import Roles,getRoles
        id = HiddenField('id')
        name = StringField('Name', render_kw={'readonly': True})
        roles = QuerySelectMultipleField('Roles', 
                query_factory=getRoles)
        submit = SubmitField('Submit') 
        
        # Custom validate
        def validate(self):
            # ... custom validation
            
            return True 

        @classmethod
        def update_data(cls,form,item):
            item.roles.clear()
            for role in form.roles.data:
                item.roles.append(role)
            db.session.commit()
            
        @classmethod
        def get_form(cls,id):
            item = User.query.get(id)
            return cls(obj=item),item
       
    model_form = {"User":("帳戶",UpdateUser),"UserRoles":("帳戶權限",UserRolesForm)
        ,"ProductAttribute":("商品屬性",UpdateProductAttribute),"Article":("文章",UpdateArticle)
        ,"ArticleCategory":("文章類別",UpdateArticleCategory)}
    return model_form[model]
    
def mapSearchForm(model):    

    class SearchArticleCategory(FlaskForm):
        
        parent = QuerySelectField('上層', 
            query_factory=ArticleCategory.get_tree_for_search,
            allow_blank=True, 
            render_kw={'class':'form-control'})
        name = StringField('名稱', render_kw={'class':'form-control'})

    class SearchArticle(FlaskForm):
        
        category = QuerySelectField('上層', 
            query_factory=ArticleCategory.get_tree_for_article,
            allow_blank=True, 
            render_kw={'class':'form-control'})
        title = StringField('標題', render_kw={'class':'form-control'})
        content = StringField('內容', render_kw={'class':'form-control'})
        
    class SearchProductAttribute(FlaskForm):
        name = StringField('屬性名稱', render_kw={'class':'form-control'})

    class SearchUser(FlaskForm):
        
        """Contact form."""
        name = StringField('名稱', render_kw={'class':'form-control'})
        email = StringField('Email', 
            render_kw={'class':'form-control'}) 
        source = SelectField('帳號來源', 
            render_kw={'class':'form-control'},
            choices = [('',''),('google', 'google'),
                   ('facebook', 'facebook'),
                   ('local', '本地')])
        roles = QuerySelectField('權限', 
            query_factory=getRoles,
            allow_blank=True, 
            render_kw={'class':'form-control'})
        active = SelectField('有效', 
            render_kw={'class':'form-control'},
            choices = [('',''),('1', '有效'),('0', '無效')])

            


    class SearchUserRoles(FlaskForm):
        pass


    model_form = {"User":SearchUser,"UserRoles":SearchUserRoles,"ProductAttribute":SearchProductAttribute
        ,"ArticleCategory":SearchArticleCategory,"Article":SearchArticle}
    return model_form[model]
    


def mapDeleteForm(model):
    
    class DeleteUser():
        @classmethod
        def delete_data(cls,item):
            try:
                """檢查:管理員不能刪除"""
                for user in item:
                    _del = User.query.filter(User.id==user).first()
                    if _del.email == current_app.config['ADMIN']:
                        return "此帳號-{},是管理員,不能刪除!".format(_del.name)
                    if _del.id ==current_user.id:
                        return "此帳號-{},己登入,不能刪除!".format(_del.name)

                str_roles = "delete from user_roles where user_id in (:item);"
                db.session.execute(str_roles,{'item':item})
                stm = User.__table__.delete().where(User.id.in_(item))
                db.session.execute(stm)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                """ 捕獲錯誤, 否則無法回傳
                """
                db.session().rollback()   
                if 'orig' in e.__dict__:
                    return str(e.__dict__['orig'])
                #raise e
                return '刪除失敗!!'
            return None  

    class DeleteUserRoles():
        pass

    class DeleteProductAttribute():
        
        @classmethod
        def delete_data(cls,item):
            try:
                stm = ProductAttribute.__table__.delete().where(ProductAttribute.id.in_(item))
                db.session.execute(stm)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                """ 捕獲錯誤, 否則無法回傳
                """
                db.session().rollback()   
                if 'orig' in e.__dict__:
                    return str(e.__dict__['orig'])
                return '刪除失敗!!'
            return None  

    class DeleteArticleCategory():
        @classmethod
        def delete_data(cls,item):
            try:
                #檢查是否有目錄及文章在此目錄下
                for cat in item:
                    articles = Article.query.filter(Article.category_id == cat).all()
                    if articles:
                        return '刪除失敗!!尚有文章在此目錄下'
                    categories = ArticleCategory.query.filter(ArticleCategory.parent_id == cat).all()
                    if categories:
                        return '刪除失敗!!尚有其它目錄在此目錄下'
                    stm = ArticleCategory.__table__.delete().where(ArticleCategory.id==cat)
                    db.session.execute(stm)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                """ 捕獲錯誤, 否則無法回傳
                """
                db.session().rollback()   
                if 'orig' in e.__dict__:
                    return str(e.__dict__['orig'])
                return '刪除失敗!!'
            return None     

    class DeleteArticle():
        @classmethod
        def delete_data(cls,item):
            try:
                stm = Article.__table__.delete().where(Article.id.in_(item))
                db.session.execute(stm)
                db.session.commit()
            except exc.SQLAlchemyError as e:
                """ 捕獲錯誤, 否則無法回傳
                """
                db.session().rollback()   
                if 'orig' in e.__dict__:
                    return str(e.__dict__['orig'])
                return '刪除失敗!!'
            return None        

    model_form = {"User":DeleteUser,"UserRoles":DeleteUserRoles,"ProductAttribute":DeleteProductAttribute
        ,"ArticleCategory":DeleteArticleCategory,"Article":DeleteArticle}
    return model_form[model]
    
    