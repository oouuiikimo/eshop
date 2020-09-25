from flask import current_app as app
from .baserepo import BaseRepo
from ...models.db_product import ProductAttribute
   
class CartWishlist(BaseRepo):

    def __init__(self,request):
        super().__init__(request)
        self.title = "暫存購買清單"
        self.template = "/shop/cart_wishlist.html"
        self.description = "您在{}網站中目前暫存了{}項購買商品, 共{}元,可依需要喜好儘快購買, 謝謝您的惠顧。"
        self.data = self.gen_data()
        
    def gen_data(self):    
        return {"repo":self.title,
            "title":self.title,
            "description":self.description.format('Your-tom Eshop','10','1538'),
            "test":"this is data"}
        
    def post(self,action):
        return {"success":"action:{} test OK".format(action)}