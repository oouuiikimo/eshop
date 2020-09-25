from flask import current_app as app
from .baserepo import BaseRepo
from ...models.db_article import Article,ArticleCategory
   
class BlogShow(BaseRepo):

    def __init__(self,request):
        super().__init__(request)
        self.title = "Blog文章"
        self.template = "/shop/blog_show.html"
        self.description = "這是一篇blog文章.."
        self.data = self.gen_data()
        
    def gen_data(self):    
        return {"repo":self.title,
            "title":self.title,
            "description":self.description,
            "test":"this is data"}
        
    def post(self,action):
        return {"success":"action:{} test OK".format(action)}