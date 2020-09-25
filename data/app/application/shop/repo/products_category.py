from flask import current_app as app
from .baserepo import BaseRepo
from ...models.db_product import ProductAttribute
   
class ProductsCategory(BaseRepo):

    def __init__(self,request):
        super().__init__(request)
        self.title = "{}::商品分類"
        self.template = "/shop/products_category.html"
        self.description = "{} 網站的商品分類:{}"
        self.data = self.gen_data()
        
    def gen_data(self):    
        return {"repo":self.title,
            "title":self.title.format('Your-tom Eshop'),
            "description":self.description.format('Your-tom Eshop','aaa,bbb,ccc,dddd..'),
            "test":"this is data"}
        
    def post(self,action):
        return {"success":"action:{} test OK".format(action)}