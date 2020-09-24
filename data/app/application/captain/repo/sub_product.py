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
                    "isvariant":'1' if bool(db_data.isvariant) == True else '0',
                    "active":'1' if bool(db_data.active) == True else '0'}
        
    def details(self,dic_replace,template):
        return
        
    def prepare_form(self,obj):
        return self.update_form(obj=obj)
        
    def skip_details(self):
        #有時雖有details功能, 但特殊情況下跳過, 直接進入form
        return False
        
class SubBasic(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.update_form = Update_basic_Form
    
    def update(self,session,db_item,item):
        db_item.name = item.name
        db_item.sku = item.sku
        db_item.description = item.description
        db_item.order = item.order
        db_item.isvariant = True if item.isvariant=='1' else False
        db_item.active = True if item.active=='1' else False
        category = session.query(ProductCategory).filter(ProductCategory.id==item.category).first()
        db_item.category = category
        #raise Exception(category)
        """todo: 如果, 要檢查什麼? sku,category,image,
        if db_item.active == True:
        
        """
        

    def prepare_form(self,obj):
        if int(self.parent_id)==0:
            #編輯時使用表單(有些欄位不能再更改,但要顯示...如何做)
            self.update_form = Insert_basic_Form
        form = self.update_form(obj=obj)    
        prductCategory = RepoProductCategory()
        form.category.choices = form.category.choices + prductCategory.get_tree_for_form() #get_tree()
        return form
        
class SubCategory(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.update_form = Update_subcategory_Form
        
    def form_data(self):
        if self.detail_id and int(self.detail_id)>0:
            with self.app.db_session.session_scope() as session:
                db_data = session.query(SubProductCategory).get(self.detail_id)
                #raise Exception(db_data.id)
                return {"subcategory":db_data.id,"original":db_data.id}
        else:
            db_data = SubProductCategory()
            return {"subcategory":"","original":0}
                
    def prepare_form(self,obj):
        #新增時使用表單

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
        #若沒有改變, 則退出
        if int(item.subcategory) == int(item.original):
            raise Exception("分類沒有改變,取消更新") 
        
        #檢查是否己有同id
        subcategory = session.query(SubProductCategory).filter(SubProductCategory.id==item.subcategory).first()
        if subcategory not in db_item.sub_categorys:
            #刪除舊的:original, 新增新的:subcategory
            if int(item.original)>0:
                original = session.query(SubProductCategory).filter(SubProductCategory.id==item.original).first()
                db_item.sub_categorys.remove(original)
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
        self.update_form = Update_variant_Form
    
    def form_data(self):
        if self.detail_id and int(self.detail_id)>0:
            with self.app.db_session.session_scope() as session:
                db_data = session.query(Variant).get(self.detail_id)
                return {"variant":db_data.id,"original":db_data.id}
        else:
            db_data = ProductSku()
            return {"variant":db_data.id,"original":0}
                
    def prepare_form(self,obj):
        form = self.update_form(obj=obj)
        with self.app.db_session.session_scope() as session:
            choices = [(str(i.id),i.variant) for i in session.query(Variant).all()]
            form.variant.choices = form.variant.choices + choices
        return form
    
    def validate_update(self,db_item,item):
        #todo: 檢查是否己有sku, 或己銷售, 若有, 則不能更新, 需視為新商品另增一個
        if db_item.skus:
            raise Exception("己有庫存, 屬性禁止更新, 若有不同屬性商品請另建新商品!")
                
    def update(self,session,db_item,item):
        self.validate_update(db_item,item)
        #若沒有改變, 則退出
        if int(item.variant) == int(item.original):
            raise Exception("所選屬性沒有改變,取消更新") 
        
        #檢查是否己有同id
        variant = session.query(Variant).filter(Variant.id==item.variant).first()
        if variant not in db_item.variants:
            
            #刪除舊的:original, 新增新的:subcategory
            if int(item.original)>0:
                original = session.query(Variant).filter(Variant.id==item.original).first()
                db_item.variants.remove(original)
            db_item.variants.append(variant)
        else:
            raise Exception("己有同樣屬性, 無法再新增")
            
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
        
    def delete(self,session,db_item,dels):
        self.validate_update(db_item,dels)
        for _del in dels:
            variant = session.query(Variant).filter(Variant.id==_del).first()
            db_item.variants.remove(variant)
            #raise Exception(str(variant))

class SubSku(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.update_form = Update_sku_Form
        self.update_form_js = 'sku.js'
        self.isvariant = False
        with self.app.db_session.session_scope() as session:
            product = self.parent(session)
            self.isvariant = product.isvariant
        if self.isvariant:
            self.update_form = Update_skus_Form
    
    def form_data(self):
        with self.app.db_session.session_scope() as session:
            if self.detail_id and int(self.detail_id)>0:
                db_data = session.query(ProductSku).get(self.detail_id)
            else:
                db_data = ProductSku()
                
            data = {"sku":db_data.sku,"price":db_data.price,"quantity":db_data.quantity,
                    "lot_maintain":'1' if bool(db_data.lot_maintain) == True else '0',
                    "active":'1' if bool(db_data.active) == True else '0'}
            if db_data.values:
                #編輯頁時, 顯示value名稱
                data.update({"values":','.join([str(i.value) for i in db_data.values])})
            return data    
                
    def validate_update(self,db_item,item):
        #todo: 檢查是否己有sku, 或己銷售, 若有, 則不能更新, 需視為新商品另增一個
        if db_item.skus:
            raise Exception("己有庫存, 屬性禁止更新, 若有不同屬性商品請另建新商品!")
                
    def update(self,session,db_item,item):
        #self.validate_update(db_item,item)
        #values,sku 只限新增,更新不可
        if int(self.detail_id)==0:
            sku = ProductSku()
            sku.sku = item.sku
            sku.id_product = db_item.id
            
            if self.isvariant:
            #todo:新增variant values,並檢查是否都有齊全,且不得重複
                values = str(item.values).split(',')
                for v in values:
                    value = session.query(VariantValues).filter(VariantValues.id==int(v)).first()
                    sku.values.append(value)
            
        else:
            sku = session.query(ProductSku).filter(ProductSku.id==self.detail_id).first()
        #編輯只限更新以下...    
        sku.price = int(item.price)
        sku.quantity = int(item.quantity)
        sku.lot_maintain = True if item.lot_maintain=='1' else False
        sku.active = True if item.active=='1' else False
        
        session.add(sku)
       
            
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
    
    def prepare_form(self,obj):
        def get_variantvalues():
            #新增sku時, 提供選項, 
            #若是編輯時, 則只提供sku 的values
            variants = []
            with self.app.db_session.session_scope() as session:
                
                if int(self.detail_id)>0: #編輯狀態
                    sku = session.query(ProductSku).get(self.detail_id)
                    for value in sku.values:
                        variants.append((value.id,f'{value.Variant.variant}_{value.value}'))
                else: #新增狀態,
                    product = self.parent(session)
                    for variant in product.variants:
                        for value in variant.values: #要如何分辨不同的variant?
                            variants.append((value.id,f'{variant.variant}_{value.value}'))
            #raise Exception(variants)                
            return variants
        

        form = self.update_form(obj=obj)    
        if self.isvariant:
            choices = get_variantvalues()
            form.variantvalues_source.choices = form.variantvalues_source.choices + get_variantvalues()
        #form.variantvalues_source.default = choices[0][0]
        return form
    
    def delete(self,session,db_item,dels):
        #self.validate_update(db_item,dels)
        for _del in dels:
            #delete cascade sku.values
            sku = session.query(ProductSku).filter(ProductSku.id==_del).first()
            session.delete(sku)
        
    def skip_details(self):
        #檢查, 是否沒有屬性, 即不需進入details, 直接進入form
        #且必須填充 self.detail_id
        with self.app.db_session.session_scope() as session:
            product = self.parent(session)
            if not product.isvariant:
                self.detail_id = product.skus[0].id if product.skus else 0
                return True
        return False
        
class SubImage(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.update_form = Update_image_Form
        self.update_form_js = 'image.js'
    
    def form_data(self):
        if self.detail_id and int(self.detail_id)>0:
            with self.app.db_session.session_scope() as session:
                db_data = session.query(ProductImage).get(self.detail_id)
                #raise Exception(db_data.id)
                return {"file_name":db_data.file_name,"active":'1' if bool(db_data.active) == True else '0'}
        else:
            db_data = SubProductCategory()
            return {"file_name":"","active":'1'}
    
class SubArticle(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.update_form = Update_article_Form
    
    #def form_data(self):
    #    pass
    
class SubActive(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
        self.update_form = Update_active_Form
        
    
    #def form_data(self):
    #    pass
    
class SubOther(BaseSub):
    def __init__(self,app,id,detail_id):
        super().__init__(app,id,detail_id)
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