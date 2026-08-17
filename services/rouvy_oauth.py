import os
import secrets
import urllib.parse
import requests

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH_URL = "https://api.rouvy.com/oauth/authorize"

TOKEN_URL = "https://api.rouvy.com/oauth/token"

#RouvyOAuthError class defined to inherit from python Exception class and enable easy RouvyOAuthError identification  
class RouvyOAuthError(Exception):
    pass   #do nothing and continue, so allows for basic inheritance nothing else

class RouvyAuthorizationRequired(Exception):
    pass   #do nothing and continue, so allows for basic inheritance nothing else

def exchange_token(refreshToken):

    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refreshToken,
        "grant_type": "refresh_token"
    }

    try:
        response = requests.post(
            TOKEN_URL,
            data=data
        )

    except requests.RequestException as e:
        raise RouvyOAuthError(
            "Unable to contact ROUVY token endpoint"
        ) from error

    # Refresh token was rejected / authorization is no longer valid
    if response.status_code == 400:
        raise RouvyAuthorizationRequired(
            "ROUVY refresh token is no longer valid"
        )

    try:
        response.raise_for_status()
    except requests.RequestException as e:
        raise RouvyOAuthError(
            "ROUVY token request failed"
        ) from error

    token_data = response.json()

    if "access_token" not in token_data:
        raise RouvyOAuthError(
            "ROUVY token response did not contain an access token"
        )

    return token_data

def get_oauth_url():

    state = secrets.token_hex(16)

    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "profile:read activities:read events:read",
        "response_type": "code",
        "state": state
    }

    url = AUTH_URL + "?" + urllib.parse.urlencode(params)

    return url


def get_token(code):

    try:

       token_response = requests.post(
           TOKEN_URL,
           data={
               "grant_type": "authorization_code",
               "client_id": CLIENT_ID,
               "client_secret": CLIENT_SECRET,
               "code": code,
               "redirect_uri": REDIRECT_URI
           },
           timeout = 10
        )

    except requests.RequestException as error:

        raise RouvyOAuthError(
            "Unable to contact ROUVY token endpoint"
        ) from error

    if token_response.status_code != 200:

        raise RouvyOAuthError(
            f"Token exchange failed: "
            f"HTTP {response.status_code}"
        )


    # Return token data in JSON: 
    #             'access_token': {text-key}
    #             'token_type': 'Bearer', 
    #             'expires_in': 3600, 
    #             'refresh_token' {text-key}

    try:

        return token_response.json()

    except ValueError as error:

        raise RouvyOAuthError(
            "ROUVY returned invalid JSON"
        ) from error


    


    
   