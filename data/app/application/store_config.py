"""Flask config class."""
import os
import json
from collections import namedtuple
from json import JSONEncoder
import os

script_dir = os.path.dirname(os.path.realpath('__file__')) #<-- absolute dir the script is in
rel_path = "/home/user/data/app/config/store.json"
abs_file_path = os.path.join(rel_path)
#print(abs_file_path)
def default_store_keys():
    _keys = {
        #INFO
        "NAME":"Your Eshop","DESCRIPTION":"",
        "ADDRESS":"","CONTACT":"","PHONE":"",
        "FAVICON":"favicon.png","IMAGE":"",
        "CURRENCY":"NTD","TAX":0.05,
        "MEMBER_TEARMS":"","CHECKOUT_TEARMS":"",
        #FUNCTIONAL
        "PRODUCTS_PER_PAGE":10,"SUM_PRODUCTS_ON_CATEGORY":1,
        "COMMENTS":1,"COMMENT_FOR_ANONNYMOUSE":1,"COMMENT_ALERT":1,"MAX_LOGIN":3,"NEW_ACCOUNT_ALERT":1,
        "ADMIN_EMAIL":'tom@your-tom.com',
        #MAIL
        "MAIL_SERVER":'smtp.gmail.com',#,True,'tom@your-tom.com',''
        "MAIL_PORT":465,
        "MAIL_USE_SSL":1,
        "MAIL_USERNAME":'tom@your-tom.com',
        "MAIL_PASSWORD":'',
        #SOCIAL MEDIA
        "FACEBOOK":"","LINE":"",
        #GOOGLE
        "GOOGLE_CLIENT_ID":'459227710478-741udk5m52ed4jdtrl3h4upbsar4fpe4.apps.googleusercontent.com',
        "GOOGLE_CLIENT_SECRET":'NPyEdkGa7cmPyMyY-gZwg_cS',
        "GOOGLE_DISCOVERY_URL":("https://accounts.google.com/.well-known/openid-configuration"),
        #FACEBOOK
        "FACEBOOK_APP_ID":'3047683778598908',
        "FACEBOOK_APP_VERSION":'v7.0'        
        }
    return set_config(_keys)

def store_config(_nametuple=True):
    data = None
    #Assume you received this JSON response
    
    with open(abs_file_path) as json_file:
        if _nametuple is True:
            return json.load(json_file, object_hook=customStoreDecoder)
        else:
            return json.load(json_file)
    
def update_store(_dict):
    _config = store_config(False)
    for f in _dict:
        #print(_config[f])
        if f in _config:
            _config[f] = _dict[f]
    set_config(_config)        
    
def customStoreDecoder(storeDict):
    return namedtuple('STORE', storeDict.keys())(*storeDict.values())
            
# Parse JSON into an object with attributes corresponding to dict keys.
def set_config(data):
    with open(abs_file_path,'w') as _file:
        #_new = json.load(_file)
        #_new["INFO"]["NAME"] = "YourTom"

        #keys = " ".join([name for name in config._fields])
        #values = ",".join(str(getattr(config, name)) for name in config._fields)
        #json_config = {"keys":keys,"values":values}
        json.dump(data,_file, indent=4)
        #_file.write('{"keys":[{}]}'.format(keys))
        
if __name__ == "__main__":
    
    #data = store_config()._asdict()
    #data["NAME"] = "YOUR-TOM"
    #print("After Converting JSON Data into Custom Python Object")
    #print(data.SQLALCHEMY_DATABASE_URI)
    default_store_keys()
    #_dict = {"NAME":"NEW ESHOP"}
    #update_store(_dict)


    



