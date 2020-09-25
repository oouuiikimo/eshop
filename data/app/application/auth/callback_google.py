from oauthlib.oauth2 import WebApplicationClient
from flask import current_app as app
import requests,os
from flask import url_for,json

# Configuration
#GOOGLE_CLIENT_ID = app.config['GOOGLE_CLIENT_ID']
#GOOGLE_CLIENT_SECRET = app.config['GOOGLE_CLIENT_SECRET']
#GOOGLE_DISCOVERY_URL = app.config['GOOGLE_DISCOVERY_URL']
GOOGLE_CLIENT_ID = app.store_config.GOOGLE_CLIENT_ID
GOOGLE_CLIENT_SECRET = app.store_config.GOOGLE_CLIENT_SECRET
GOOGLE_DISCOVERY_URL = app.store_config.GOOGLE_DISCOVERY_URL
#add environment variable OAUTHLIB_INSECURE_TRANSPORT for debug only
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
client = WebApplicationClient(GOOGLE_CLIENT_ID)
    
def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()

def callback_google(request,type):


    # OAuth2 client setup
    
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    _callback = 'https://eshop.your-tom.com/auth/callback/{}/{}'.format('g',type)
    """url_for('auth_bp.callback',
        _external=True,
        _scheme='https',
        type='google')
    """    
        
    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=_callback,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    
    if not userinfo_response:
        return "we have problems login google!",400
        
    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    
    if userinfo_response.json().get("email_verified"):
        response = userinfo_response.json()
        unique_id = response["sub"]
        users_email = response["email"]
        picture = response["picture"]
        users_name = response["given_name"]
        name = response["name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    return {'social_id':unique_id,'email':users_email,'users_name':users_name,'name':name,'picture':picture}
    