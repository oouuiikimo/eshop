
def get_menu(menu=None,submenu=None):
    activemenu={'mainTitle':None,'subTitle':None}
    leftmenu = {
        "Accounts":{"title":"會員管理","icon":"fa-users","open":"","active":"",
        "submenu":{
            "User":{"title":"帳戶管理","href":"/admin/Accounts/User","icon":"fa-user","active":""}
            }},
        "Products":{"title":"商品管理","icon":"fa-gift","open":"","active":"",
        "submenu":{
            "ProductAttribute":{"title":"商品屬性","href":"/admin/Products/ProductAttribute","icon":"fa-magic","active":""},
            "ProductType":{"title":"商品類別","href":"/admin/Products/ProductType","icon":"fa-th","active":""},
            "Product":{"title":"商品設定","href":"/admin/Products/Product","icon":"fa-gift","active":""},
            "Variant":{"title":"商品存貨","href":"/admin/Products/Variant","icon":"fa-paperclip","active":""},
            "ProductCategory":{"title":"商品目錄","href":"/admin/Products/ProductCategory","icon":"fa-tags","active":""}
            }},
        "Articles":{"title":"文章管理","icon":"fa-newspaper","open":"","active":"",
        "submenu":{
            "filemanager":{"title":"filemanager","href":"/files/filemanager","icon":"fa-folder-open","active":""},
            "ArticleCategory":{"title":"ArticleCategory","href":"/admin/Articles/ArticleCategory","icon":"fa-th-large","active":""},
            "Article":{"title":"Article","href":"/admin/Articles/Article","icon":"fa-pen-square","active":""}
            }},
        "Orders":{"title":"訂單管理","icon":"fa-shopping-cart","open":"","active":"",
        "submenu":{
            "Orders":{"title":"Orders","href":"/admin/Orders/Orders","icon":"fa-truck","active":""}
            }},
        "Tests":{"title":"功能測試","icon":"fa-question-circle","open":"","active":"",
        "submenu":{
            "ckeditor":{"title":"ckeditor","href":"/admin/ckeditor","icon":"fa-pencil-alt","active":""},
            "Trumbowyg":{"title":"Trumbowyg","href":"/admin/Trumbowyg","icon":"fa-edit","active":""}
            }}
        }

    if menu is not None and menu in leftmenu:
        leftmenu[menu]["open"]="menu-open"
        leftmenu[menu]["active"]="active"
        activemenu["mainTitle"]=leftmenu[menu]["title"]
        if submenu is not None and submenu in leftmenu[menu]["submenu"]:
            leftmenu[menu]["submenu"][submenu]["active"]="active"
            activemenu["subTitle"]=leftmenu[menu]["submenu"][submenu]["title"]
    return {'leftmenu':leftmenu,'active':activemenu}