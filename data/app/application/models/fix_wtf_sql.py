""" fix Flask WTForms and WTForms-SQLAlchemy QuerySelectField produce too many values to unpack """
import wtforms_sqlalchemy.fields as f                                                                                                                                                                                                                                                                    
def get_pk_from_identity(obj):
    cls, key = f.identity_key(instance=obj)[:2]
    return ':'.join(f.text_type(x) for x in key) 

def fix_wtfsql():    
    f.get_pk_from_identity = get_pk_from_identity