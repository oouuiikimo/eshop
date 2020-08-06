from flask import current_app as app
from .baserepo import BaseRepo
from ...models.db_product import ProductAttribute
   
class ProductsShow(BaseRepo):

    def __init__(self,request):
        super().__init__(request)
        self.title = "{}::-{}"
        self.template = "/shop/products_show.html"
        self.description = "{}" #應該說些具體的內容, 簡短規格,價格...等等
        self.data = self.gen_data()
        
    def gen_data(self):    
        test = self.request.args.get('test')
        return {"repo":self.title,
            "title":self.title.format('Your-tom Eshop',"AAABBBCCC"),
            "description":self.description.format('商品AAABBBCCC'),
            "test":test if test else "this is data"}
        
    def post(self,action):
        
        return {"success":"action:{} test OK".format(action)}