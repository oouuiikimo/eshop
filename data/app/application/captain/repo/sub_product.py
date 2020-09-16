from .form_product import *
from ...models.db_product import *
from .productcategory import RepoProductCategory
from .subproductcategory import RepoSubProductCategory
from flask import jsonify

class BaseSub():
    def __init__(self,app,id,detail_id):
        self.title = None
        self.app = app
        self.parent_id = int(id)
        self.detail_id = detail_id
        self.update_form_js = None
    
    def parent(self,session):
        if self.parent_id>0:
            return session.query(Product).filter(Product.id==self.parent_id).first()

    def form_data(self):
        with self.app.db_session.session_scope() as session: 
            if self.parent_id>0:
                db_data = session.query(Product).get(self.parent_id)
            else:
                db_data = Product()

            return {"name":db_data.name,"sku":db_data.sku,"description":db_data.description,
                    "order":db_data.order,
                    "category":db_data.category.id if db_data.category else "",
                    "active":'1' if bool(db_data.active) == True else '0'}
        
    def details(self,dic_replace,template):
        return
        
    def set_form_choice(self,obj):
        return self.update_form(obj=obj)
        
class SubBasic(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.title = "基本資訊"
        self.update_form = Update_basic_Form
    
    def update(self,session,db_item,item):
        db_item.name = item.name
        db_item.sku = item.sku
        db_item.description = item.description
        db_item.order = item.order
        db_item.active = True if item.active=='1' else False
        category = session.query(ProductCategory).filter(ProductCategory.id==item.category).first()
        db_item.category = category
        #raise Exception(category)
        """todo: 如果, 要檢查什麼? sku,category,image,
        if db_item.active == True:
        
        """

    def set_form_choice(self,obj):
        form = self.update_form(obj=obj)
        prductCategory = RepoProductCategory()
        form.category.choices = form.category.choices + prductCategory.get_tree_for_form() #get_tree()
        return form
        
class SubCategory(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.title = "目錄"
        self.update_form = Update_subcategory_Form
        
    def form_data(self):
        if self.detail_id and int(self.detail_id)>0:
            with self.app.db_session.session_scope() as session:
                db_data = session.query(SubProductCategory).get(self.detail_id)
                #raise Exception(db_data.id)
                return {"subcategory":db_data.id}
        else:
            db_data = SubProductCategory()
            return {"subcategory":""}
                
    def set_form_choice(self,obj):
        form = self.update_form(obj=obj)
        subprductCategory = RepoSubProductCategory()
        form.subcategory.choices = form.subcategory.choices + subprductCategory.get_tree_for_form()
        return form

    def details(self,dic_replace,template): 
        details = []
        with self.app.db_session.session_scope() as session:
            product = self.parent(session)
            for row in product.sub_categorys:
                dic_replace.update({"parent_id":product.id,
                    "tooltip_title":row.name,
                    "rowid":row.id})
                    
                details.append([template(dic_replace)]+
                    [row.name])
                   
        return {'fields':['分類'],'data':details}    
        
    def update(self,session,db_item,item):
        #todo: 要檢查是否己有同id
        subcategory = session.query(SubProductCategory).filter(SubProductCategory.id==item.subcategory).first()
        if subcategory not in db_item.sub_categorys:
            db_item.sub_categorys.append(subcategory)
        else:
            raise Exception("己有同樣分類, 無法再新增")
        
    def delete(self,session,db_item,dels):
        for _del in dels:
            subcategory = session.query(SubProductCategory).filter(SubProductCategory.id==_del).first()
            db_item.sub_categorys.remove(subcategory)
    
class SubVariant(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.title = "屬性"
        self.update_form = Update_variant_Form
    
    def form_data(self):
        if self.detail_id and int(self.detail_id)>0:
            with self.app.db_session.session_scope() as session:
                db_data = session.query(ProductSku).get(self.detail_id)
                #raise Exception(db_data.id)
                return {"sku":db_data.sku,"price":db_data.price,"quantity":db_data.quantity}
        else:
            db_data = ProductSku()
            return {"sku":db_data.sku,"price":db_data.price,"quantity":db_data.quantity}
            
    def details(self,dic_replace,template): 
        details = []
        with self.app.db_session.session_scope() as session:
            product = self.parent(session)
            for row in product.variants:
                dic_replace.update({"parent_id":product.id,
                    "tooltip_title":row.variant,
                    "rowid":row.id})
                    
                details.append([template(dic_replace)]+[row.variant])
        return {'fields':['屬性'],'data':details}          

class SubSku(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.title = "庫存"
        self.update_form = Update_sku_Form
        self.update_form_js = 'sku.js'
    
    def form_data(self):
        if self.detail_id and int(self.detail_id)>0:
            with self.app.db_session.session_scope() as session:
                db_data = session.query(ProductSku).get(self.detail_id)
                #raise Exception(db_data.id)
                return {"sku":db_data.sku,"price":db_data.price,"quantity":db_data.quantity}
        else:
            db_data = ProductSku()
            return {"sku":db_data.sku,"price":db_data.price,"quantity":db_data.quantity}
        
    def details(self,dic_replace,template): 
        details = []
        with self.app.db_session.session_scope() as session:
            product = self.parent(session)
            for row in product.skus:
                dic_replace.update({"parent_id":product.id,
                    "tooltip_title":row.sku,
                    "rowid":row.id})
                    
                details.append([template(dic_replace)]+
                    [row.sku,row.price,row.quantity])
                   
        return {'fields':['副型號','售價','存量'],'data':details}     
    
    def set_form_choice(self,obj):
        def get_variantvalues():
            #新增sku時, 提供選項, 
            #若是編輯時, 則只提供sku 的values
            variants = []
            with self.app.db_session.session_scope() as session:
                
                if int(self.detail_id)>0: #編輯狀態
                    sku = session.query(ProductSku).get(self.detail_id)
                    for value in sku.values:
                        variants.append((value.id,f'{value.variant.variant}_{value.value}'))
                else: #新增狀態,
                    product = session.query(Product).filter(Product.id==id).first()
                    for variant in product.variants:
                        for value in variant.VariantValues: #要如何分辨不同的variant?
                            variants.append((value.id,f'{variant.variant}_{value.value}'))
            #raise Exception(variants)                
            return variants
            
        form = self.update_form(obj=obj)    
        form.variantvalues_source.choices = form.variantvalues_source.choices + get_variantvalues()
        return form
    
class SubImage(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.title = "圖片"
        self.update_form = Update_image_Form
    
    #def form_data(self):
    #    pass
    
class SubArticle(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.title = "文章"
        self.update_form = Update_article_Form
    
    #def form_data(self):
    #    pass
    
class SubActive(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.title = "上架"
        self.update_form = Update_active_Form
        
    
    #def form_data(self):
    #    pass
    
class SubOther(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.title = "基本資訊"
        self.update_form = Update_basic_Form
    
    def form_data(self):
        pass
                    

sub_repo = {
        "basic":{"class":SubBasic,"menu":"基本資訊"},
        "subcategory":{"class":SubCategory,"menu":"其它分類"},
        "variant":{"class":SubVariant,"menu":"屬性"},
        "sku":{"class":SubSku,"menu":"庫存"},
        "image":{"class":SubImage,"menu":"圖片"},
        "article":{"class":SubArticle,"menu":"文章"}
        } 