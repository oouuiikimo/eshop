from flask import current_app as app
from .baserepo import BaseRepo
from ...models.db_article import Article,ArticleCategory
   
class BlogList(BaseRepo):

    def __init__(self,request):
        super().__init__(request)
        self.title = "Blog列表"
        self.template = "/shop/blog_list.html"
        self.description = "這是一份blog文章列表"
        self.data = self.gen_data()
        
    def gen_data(self):    
        return {"repo":self.title,
            "title":self.title,
            "description":self.description,
            "test":"this is data"}
        
    def post(self,action):
        return {"success":"action:{} test OK".format(action)}