from flask import current_app as app
from .baserepo import BaseRepo
from ...models.db_product import ProductAttribute
   
class MemberAccount(BaseRepo):

    def __init__(self,request):
        super().__init__(request)
        self.title = "會員專區"
        self.template = "/shop/member_account.html"
        self.description = "您在{}網站的會員資料如下, 若有變動請維護正確資訊, 以方便對您的服務正確性, 謝謝您的惠顧。"
        self.data = self.gen_data()
        
    def gen_data(self):    
        return {"repo":self.title,
            "title":self.title,
            "description":self.description.format('Your-tom Eshop'),
            "test":"this is data"}
        
    def post(self,action):
        return {"success":"action:{} test OK".format(action)}