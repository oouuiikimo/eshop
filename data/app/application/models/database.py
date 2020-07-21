
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker, joinedload
from contextlib import contextmanager

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
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        try:
            yield self.session
            self.session.commit()
        except:
            self.session.rollback()
            raise
        finally:
            self.session.close()

    @classmethod
    def to_dict(row):
            dict = {}
            dict.update(row.__dict__)
            if "_sa_instance_state" in dict:
                del dict['_sa_instance_state']
            return dict
        
