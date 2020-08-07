from sqlalchemy.orm import sessionmaker
from flask import current_app as app
from sqlalchemy import func,exc
from ...share.helpers import Pagination

class BaseRepo(object):
    def __init__(self):
        pass
        
    def get_list(self,page=1,per_page=10,search=None):
    
        def get_pagination(total,page=1, per_page=10):     
            #total = cls.get_total()
            return Pagination(page, per_page, total)
            
            
        def get_query(session,filters,page,per_page):
            import math
            
            def get_count(q):
                count_q = q.statement.with_only_columns([func.count()]).order_by(None)
                count = q.session.execute(count_q).scalar()
                return count
            
            page=int(page)
            per_page=int(per_page) or 10
            #get all rows before doing pagination !!
            
            q = session.query(self.model).filter(*filters)
            
            q_count = get_count(q)
            #修正不正確的頁數顯示
            if (page-1)*per_page > q_count:
                page = math.ceil(q_count / per_page)
            return page,q_count,q.limit(per_page).offset((page-1)*per_page).all()    
        
        filters = self.get_search_filters(search)
        with app.db_session.session_scope() as session: 
            page,count,rows = get_query(session,filters,page,per_page) 
            out_rows = self.get_listrows(rows)

        return page,out_rows,count,get_pagination(count,page,per_page)

        
    class Struct:
        def __init__(self, **entries):
            self.__dict__.update(entries)
        

        
        