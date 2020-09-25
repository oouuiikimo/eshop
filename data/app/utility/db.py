import sys
sys.path.append("/home/user/data/app")
import psycopg2
from utility.config import config
 
class DB():
    # read connection parameters 
    def __init__(self):
        self._config = config()
    
    def connect(self,func,parm):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
     
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')

            self.conn = psycopg2.connect(host=self._config["host"],database=self._config["database"],
                user=self._config["user"], password=self._config["password"])
          
            # create a cursor
            self.cur = self.conn.cursor()
            
            # execute a statement
            return func(parm)
           
           # close the communication with the PostgreSQL
            self.cur.close()
        #except (Exception, psycopg2.DatabaseError) as error:
        #    print(error)
        finally:
            if self.conn is not None:
                self.conn.close()
                print('Database connection closed.')
 
if __name__ == '__main__':
    class TESTDB(DB):
        def exec_func(self,parm):
            sql="SELECT * from orders where id =%(id)s ;"
            
            self.cur.execute(sql,parm)
            return self.cur.fetchone()
            
    db = TESTDB()        
    parm={'id':1}
    print(db.connect(db.exec_func,parm))