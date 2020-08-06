from flask import current_app as app
from .baserepo import BaseRepo
from ...models.db_product import ProductAttribute
   
class CartCheckout(BaseRepo):

    def __init__(self,request):
        super().__init__(request)
        self.title = "{}::購物車內容"
        self.template = "/shop/cart_checkout.html"
        self.description = "您在 {} 網站中目前添購了{}項商品, 共{}元,請依指引完成結帳動作, 謝謝您的惠顧。"
        self.data = self.gen_data()
        
    def gen_data(self):    
        return {"repo":self.title,
            "title":self.title.format('Your-tom Eshop'),
            "description":self.description.format('Your-tom Eshop','10','1538'),
            "test":"this is data"}
        
    def post(self,action):
        return {"success":"action:{} test OK".format(action)}