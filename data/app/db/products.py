import sys
sys.path.append("/home/user/data/app")
from utility.db import DB

class PRODUCTS(DB):
    def exec_func(self,parm):
        sql="SELECT * from orders where id =%(id)s ;"
        
        self.cur.execute(sql,parm)
        return self.cur.fetchone()
        
if __name__ == '__main__':        
    db = PRODUCTS()        
    parm={'id':1}
    print(db.connect(db.exec_func,parm))