from flask import current_app as app
from .baserepo import BaseRepo
from ...models.db_product import Article,ArticleCategory,ProductAttribute
   
class CartList(BaseRepo):

    def __init__(self):
        super().__init__()
        self.title = "購物車內容"
        self.template = "/shop/cart.html"
        self.description = ""
        self.data = self.gen_data()
        
    def gen_data(self):    
        return {"repo":self.title,"test":"this is data"}
        
    def post(self,action):
        return {"success":"action:{} test OK".format(action)}