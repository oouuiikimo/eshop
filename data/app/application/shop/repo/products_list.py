from flask import current_app as app
from .baserepo import BaseRepo
from ...models.db_product import ProductAttribute
   
class ProductsList(BaseRepo):

    def __init__(self,request):
        super().__init__(request)
        self.title = "{}::商品列表"
        self.template = "/shop/products_list.html"
        self.description = "{} 網站的商品列表:{}"
        self.data = self.gen_data()
        
    def gen_data(self):    
        return {"repo":self.title,
            "title":self.title.format('Your-tom Eshop'),
            "description":self.description.format('Your-tom Eshop','aaa,bbb,ccc,dddd..'),
            "test":"this is data"}
        
    def post(self,action):
        return {"success":"action:{} test OK".format(action)}