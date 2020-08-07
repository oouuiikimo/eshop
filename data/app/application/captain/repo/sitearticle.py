from flask import current_app as app
from flask_login import current_user
from .baserepo import BaseRepo
from ...models.db_article import SiteArticle
from ...models.db_user import User
from .form_sitearticle import SearchForm,UpdateForm
from sqlalchemy import exc
import datetime

class RepoSiteArticle(BaseRepo):
    #public function  ----    
    def __init__(self):
        super().__init__()
        self.title = "網站內文章"
        self.model = SiteArticle
        self.active_menu = "sub_list_sitearticle"
        self.description = """
        說明: 網站內文章列表, 請注意, 若有文章刪除, 前台連結將無法顯示文章內容, 更新亦同。
        """
        #異動tables
        #Base.metadata.create_all(app.db_session.engine)
        #異動data
        #self.init_db()
        
        
    def __repr__(self):
        return self.title
        
    def form_mapper(self,db_data):
        
        form_data = {"title":db_data.title,"link_text":db_data.link_text,"description":db_data.description,
            "content":db_data.content}

        return self.Struct(**form_data)
        
    def update_form(self,id=None):
        db_item = self.find(id)
        form = UpdateForm(obj=db_item)
        #if form has any select choices to fill...
        #example:form.roles.choices = self.get_roles()
        return form,db_item
        
    def search_form(self):
        form = SearchForm()
        #if form has any select choices to fill...
        #form.roles.choices = form.roles.choices + self.get_roles()

        return form

    def get_listrows(self,rows):
        out_rows = []
        with app.db_session.session_scope() as session:
            for row in rows:
                created_by = session.query(User).filter_by(email=row.created_by).first()
                updated_by = session.query(User).filter_by(email=row.updated_by).first()
                if created_by: #更換為姓名
                    row.created_by = created_by.name
                if updated_by: #更換為姓名
                    row.updated_by = updated_by.name
                    
                out_rows.append(['<div style="width:100px;"><input type="checkbox" name="delete" value="{}">'.format(row.id)+
                    '<a href="javascript:delete_items({});" class="ml-1">'.format(row.id)+
                    '<i class="feather icon-x-circle" data-toggle="tooltip" title="刪除-{}-{}"></a></i>'.format(self.title,row.title)+
                    '<a href="/captain/update/SiteArticle/{}" class="ml-1">'.format(row.id)+
                    '<i class="feather icon-edit" data-toggle="tooltip" title="編輯-{}-{}"></a></i></div>'.format(self.title,row.title),
                    row.title,row.link_text,row.created_by,row.created.strftime("%Y/%m/%d %H:%M"),row.updated_by,row.updated.strftime("%Y/%m/%d %H:%M")
                    ])
        return {
            "fields":['文章標題','英文連結','建立者','建立日期','更新者','更新日期'],
            "rows":out_rows
            }
            
    def get_search_filters(self,search):
        filters = []
        if search:
            if 'title' in search and search['title']: #search.email.data:
                filters.append(SiteArticle.title.like('%{}%'.format(search['title'])) )   
            if 'link_text' in search and search['link_text']: #search.email.data:
                filters.append(SiteArticle.link_text.like('%{}%'.format(search['link_text'])) )            

        return filters
  
    def find(self, id=None):
        form_item = None
        if id:
            with app.db_session.session_scope() as session: 
                db_item = session.query(SiteArticle).get(id)
                form_item = self.form_mapper(db_item)
        else:
            db_item = SiteArticle()
            form_item = self.form_mapper(db_item)
        return form_item

    def update(self,item,id=None):
    
        def strip_link_text(link): #不能有空白
            return "_".join(link.split())
        
        try:
            with self.session as session:
                if id and id is not None:
                    db_item = session.query(SiteArticle).get(id)
                else:
                    db_item = SiteArticle()
                    
                db_item.title = item.title
                db_item.link_text = strip_link_text(item.link_text)
                db_item.description = item.description
                db_item.content = item.content
                db_item.updated = datetime.datetime.now()
                db_item.updated_by = current_user.email
            

                if not id:
                    db_item.created_by = current_user.email
                    session.add(db_item)
                    
        except exc.SQLAlchemyError as e:
            """ 捕獲錯誤, 否則無法回傳
            """
            if 'orig' in e.__dict__:
                return str(e.__dict__['orig'])
                #raise Exception(str(e.__dict__['orig']))
            return "更新失敗!"    
            #raise Exception('刪除失敗!!')

    def delete(self, items):
        try:
            """檢查:是否有網站引用,不能刪除"""
            #return str(type(items))
            with self.session as session: 
                for item in items:
                    _del = session.query(SiteArticle).filter(SiteArticle.id==item).first()
                    if _del:
                        session.delete(_del)
                
        except exc.SQLAlchemyError as e:
            """ 捕獲錯誤, 否則無法回傳
            """
            if 'orig' in e.__dict__:
                return str(e.__dict__['orig'])
            #raise e
            return '刪除失敗!!'
        return None  
    
    #custom function -----


    
    