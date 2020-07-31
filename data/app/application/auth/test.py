#import facebook
import hashlib
import hmac
from facebook_business import session

def genAppSecretProof(app_secret, access_token):
    h = hmac.new (
        app_secret.encode('utf-8'),
        msg=access_token.encode('utf-8'),
        digestmod=hashlib.sha256
    )
    return h.hexdigest()

app_id = "3047683778598908"
app_secret = "277158fc9e32da563291bd2c4d9059d1"
access_token = "EAArT2i0C1ZCwBAC6EjvEefwkshR57X5jTPSuvJJZAPx6HFBapypKfnZCJk9cxr7XVjZBfN5GNIb3GEvhl8ROTZBMudTJs2LinxurI1nT2isGovJYhkl4dJt3NnuIXfqE8yLAC9fvPYesAf3qNjaQZBkLwp1D3TLxVLHkoqjxNN7AwI0iNelxC2HM9MERnoTUUZD"

fb_session = session.FacebookSession(app_id, app_secret, access_token)
app_secret_proof = fb_session.appsecret_proof
print(app_secret_proof)