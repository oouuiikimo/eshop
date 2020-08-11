from sqlalchemy.orm import sessionmaker
from flask import current_app as app
from sqlalchemy import func,exc
from ...share.helpers import Pagination
from sqlalchemy.sql import text

class BaseRepo(object):
    def __init__(self):
        pass
        
    def get_list(self,page=1,per_page=10,search=None,sort=None):
    
        def get_pagination(total,page=1, per_page=10):     
            #total = cls.get_total()
            return Pagination(page, per_page, total)
            
            
        def get_query(session,filters,sort,page,per_page):
            import math
            
            def get_count(q):
                count_q = q.statement.with_only_columns([func.count()]).order_by(None)
                count = q.session.execute(count_q).scalar()
                return count
            
            page=int(page)
            per_page=int(per_page) or 10
            #get all rows before doing pagination !!
            if sort:
                q = session.query(self.model).filter(*filters).order_by(text(f"{sort} desc"))
            else:
                q = session.query(self.model).filter(*filters)
            
            q_count = get_count(q)
            #修正不正確的頁數顯示 
            if (page-1)*per_page > q_count:
                page = math.ceil(q_count / per_page)
            return page,q_count,q.limit(per_page).offset((page-1)*per_page).all()    
            
        def trans_author():
        
            pass
            
        def author_to_dict(rows):
            _dict = {}
            for i in rows:
                _dict.update({i.email:i.name})
            return _dict
        
        def set_out_rows(self,rows):
            # 頭:編輯功能,中間:各repo的顯示欄位,尾:建立, 更新
            out_rows = []
            
            for row in rows:
                _list_rows = self._list_rows(row)
                out_rows.append([f'<div style="width:80px;"><input type="checkbox" name="delete" value="{row.id}">'+
                    f'<a href="javascript:delete_items({row.id});" class="ml-1">'+
                    f"<i class=\"feather icon-x-circle\" data-toggle=\"tooltip\" title=\"刪除{self.title}{_list_rows['title_field']}\"></a></i>"+
                    f'<a href="/captain/update/{self.__class__.__name__.replace("Repo","")}/{row.id}" class="ml-1">'+
                    f"<i class=\"feather icon-edit\" data-toggle=\"tooltip\" title=\"編輯{self.title}{_list_rows['title_field']}\"></a></i></div>"]
                    + _list_rows['fields_value']
                    +[
                        f'{row.created.strftime("%Y/%m/%d %H:%M")}.{row.created_by}',
                        f'{row.updated.strftime("%Y/%m/%d %H:%M")}.{row.updated_by}']
                        )
            return out_rows
        
        filters = self.get_search_filters(search)
        with app.db_session.session_scope() as session: 
            #先依條件查 rows 
            page,count,rows = get_query(session,filters,sort,page,per_page) 
            from ...models.db_user import User
            #轉author email to name, 若沒有(有些表格可能沒有)updated_by,created_by,就不轉
            try:
                creaters = list(dict.fromkeys([i.created_by for i in rows])) #取唯一
                #raise Exception(str(creaters))
                updaters = list(filter(lambda x: x not in creaters, [i.updated_by for i in rows]))
                _authors = author_to_dict(
                    session.query(User.name,User.email).filter(User.email.in_(creaters + updaters)).all()
                    )
                for row in rows: #todo:改成全部在這裡執行完成out_rows
                    row.created_by = _authors[row.created_by] if row.created_by in  _authors else row.created_by#check_user_name(row.created_by,_authors)
                    row.updated_by = _authors[row.updated_by] if row.updated_by in  _authors else row.updated_by          
                
            except AttributeError as e:
                pass
            out_rows = {'fields':self._list_fields()+['建立','更新'],
                        'rows':set_out_rows(self,rows)}    
            #out_rows = self.get_listrows(rows)

        return page,out_rows,count,get_pagination(count,page,per_page)


        
    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)
        

        
        