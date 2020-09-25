from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from contextlib import contextmanager
from sqlalchemy.inspection import inspect
# The base class which our objects will be defined on.
Base = declarative_base()
# Create all tables by issuing CREATE TABLE commands to the DB.
#Base.metadata.create_all(engine) 
# create a configured "Session" class
# create a Session


class DB_SESSION():
    def __init__(self,db):
        
        #engine = create_engine('sqlite:////home/user/data/app/application/models/site.db', echo=False)
        self.engine = create_engine(db, echo=False)
   
    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        Session = sessionmaker(bind=self.engine, autoflush=False)
        self.session = Session()
        try:
            yield self.session
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    def rows_to_dict(self,rows,with_relationships=True):
        dict = []
        for row in rows:
            dict.append(self.to_dict(row,with_relationships))
        return dict
        
    def to_dict(self,obj, with_relationships=True):
        d = {}
        for column in obj.__table__.columns:
            if with_relationships and len(column.foreign_keys) > 0:
                 # Skip foreign keys
                continue
            d[column.name] = getattr(obj, column.name)

        if with_relationships:
            for relationship in inspect(type(obj)).relationships:
                val = getattr(obj, relationship.key)
                #若有多筆(多對多時), 是一個list , 需處理for list
                if isinstance(val, list): 
                    _list = []
                    for subitem in val:
                        _list.append(self.to_dict(subitem,False) if val else None)
                    d[relationship.key] = _list
                else: 
                    d[relationship.key] = self.to_dict(val,False) if val else None
                
        return d
            

        
