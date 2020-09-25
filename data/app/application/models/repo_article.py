
class RepoSiteArticle():

    @validates('is_leaf')
    def validate_is_leaf(self, key, is_leaf):
        has_articles = 0
        if is_leaf is False:
            has_articles = Article.query.filter(Article.category_id==self.id).count()
            if has_articles>0:
                raise Exception('這個類別尚有文章, 請先清空再取消文章類別')
        return is_leaf
    
    @classmethod
    def is_has_child(cls,id):
        has_child = BlogCategory.query.filter(BlogCategory.parent_id==id).count()
        #result = BlogCategory.query.filter(BlogCategory.id.in_([i.parent_id for i in has_child])).count()
        return has_child #.with_entities(func.count(BlogCategory.id)).scalar()
    
    @classmethod
    def get_tree(cls,id=None):
        """更新或新增表單用,顯示上層目錄供歸屬:
            .不能列出參考列的下層,只能列上層, is_leaf=True, 不然會形成迴圏, 
        """
        def func():
            statement = text(
            """
            WITH RECURSIVE category_path (id, path) AS
            (
              SELECT id, name as path
                FROM blog_category
                WHERE parent_id ==:id /*IS NULL or ==2*/
                
              UNION ALL
              SELECT c.id,  cp.path|| ' > '|| c.name as path
                FROM category_path AS cp JOIN blog_category AS c
                  ON cp.id = c.parent_id
            )
            SELECT * FROM category_path
            ORDER BY path;
            """)
            if id:
                child = [i.id for i in db.session.execute(statement,{"id":id})]
                child.append(id) #自己以及下層, 都不能出現
                return BlogCategory.query.filter(BlogCategory.id.notin_(child),BlogCategory.is_leaf==False).all()
            else:
                #is_leaf 不能出現
                return BlogCategory.query.filter(BlogCategory.is_leaf == False ).all()
        
        return func

    @classmethod
    def get_tree_for_search(cls):
        """搜尋表單, 欄位下接選擇項:不需列出最下層 is_leaf is False
        """
        #has_child = db.session.query(BlogCategory.parent_id).distinct()
        #return BlogCategory.query.filter(BlogCategory.id.in_([i.parent_id for i in has_child])).all()
        return BlogCategory.query.filter(BlogCategory.is_leaf == False).all()

    @classmethod
    def get_tree_for_article(cls):
        """文章表單用:不列出含有下層目錄的母層, 只列子層-> is_leaf is True
        """

        #注意以下, notin 裡面必須排除掉 null 否則, 結果會不正確
        #has_child = db.session.query(BlogCategory.parent_id).filter(BlogCategory.parent_id.isnot(None)).distinct()
        #return BlogCategory.query.filter(BlogCategory.id.notin_(has_child)).all()
        return BlogCategory.query.filter(BlogCategory.is_leaf == True).all()
        
    def __repr__(self):
        statement = text(
        """
        WITH RECURSIVE category_path (id, path) AS
        (
          SELECT id, name as path
            FROM blog_category
            WHERE parent_id IS NULL
          UNION ALL
          SELECT c.id,  cp.path|| ' > '|| c.name as path
            FROM category_path AS cp JOIN blog_category AS c
              ON cp.id = c.parent_id
        )
        SELECT * FROM category_path
        where id == :id;
        """)
        if self.parent:
            tree = db.session.execute(statement,{"id":self.id}).first()
            return tree.path

        return self.name