import os
import secrets
import urllib.parse
import requests

from flask import Flask, redirect, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH_URL = "https://api.rouvy.com/oauth/authorize"

TOKEN_URL = "https://api.rouvy.com/oauth/token"


@app.route("/")
def home():
    return '<a href="/login">Login with ROUVY</a>'


@app.route("/login")
def login():

    state = secrets.token_hex(16)

    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "profile:read activities:read events:read",
        "response_type": "code",
        "state": state
    }

    url = AUTH_URL + "?" + urllib.parse.urlencode(params)

    return redirect(url)


@app.route("/auth/callback")
def callback():

    code = request.args.get("code")

    token_response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "redirect_uri": REDIRECT_URI
        }
    )

    tokens = token_response.json()

    print("TOKENS:")
    print(tokens)
    
    access_token = tokens["access_token"]

    # GET ME Profile
    """  
    profile_response = requests.get(
        "https://api.rouvy.com/me",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    print("PROFILE:")
    print(profile_response.json())
    """
    
    """
    #GET Event Details ME Owns : Pulls Event_ID
    event_response = requests.get(
      "https://api.rouvy.com/me/events",
      headers={
          "Authorization": f"Bearer {access_token}"
        },
        params={
          "role": "owner",
          "status": "offline",
          "startDateTimeUtcFrom": "",
          "startDateTimeUtcTo": "",
          "limit": "100",
          "offset": "0"
        }
    )

    print("EVENT Details:")
    print(event_response.json())  
    print("EVENT Deatils END")
    """

    # GET Event Details using Event_ID
    """
    event_response = requests.get(
      "https://api.rouvy.com/events/4ff690eb-ccbc-48f2-92b0-d5f1176b323c",
      headers={
          "Authorization": f"Bearer {access_token}"
        }
    )

    print("EVENT:")
    print(event_response.json())   
    """
    
    """
    # GET Event Startlist using Event_ID
    event_response = requests.get(
      "https://api.rouvy.com/events/4ff690eb-ccbc-48f2-92b0-d5f1176b323c/startlist",
      headers={
          "Authorization": f"Bearer {access_token}"
        },
        params={
          "limit": "100",
          "offset": "0"
        }
    )
    
    print("EVENT Startlist:")
    print(event_response.json())  
    print("EVENT Startlist END")
    """
    
    # GET Event Activities using Event_ID  
    event_response = requests.get(
      "https://api.rouvy.com/events/4ff690eb-ccbc-48f2-92b0-d5f1176b323c/activities",
      headers={
          "Authorization": f"Bearer {access_token}"
        },
        params={
           "limit": "100",
           "offset": "0"
        }
    )
   
    print("EVENT Activities:")
    print(event_response.json())  
    print("EVENT Activities END")   
    
    return 
    """
    <h1>Authorization successful</h1>
    <p>Check terminal for tokens.</p>
    """


if __name__ == "__main__":
    app.run(port=3000, debug=True)