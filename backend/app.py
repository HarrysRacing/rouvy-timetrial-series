import os
import secrets
import urllib.parse

from flask import Flask, redirect, request

app = Flask(__name__)

from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH_URL = "https://api.rouvy.com/oauth/authorize"


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
    state = request.args.get("state")

    return f"Received code: {code}<br>State: {state}"


if __name__ == "__main__":
    app.run(port=3000, debug=True)