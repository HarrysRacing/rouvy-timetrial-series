# 
# Run this to initially set up the Admin User and associated OAuthKey in the databaseFind 
#

# import the Flask library
from flask import Flask, redirect, request

import webbrowser

#import function to retrieve active series data
from services.db_utils import save_rider_auth
from services.rouvy_oauth import get_oauth_url, get_token
from services.rouvy_api import get_rouvy_rider

CALLBACKURL = "http://127.0.0.1:3000/authorize"

app = Flask(__name__)


@app.route("/authorize")
def authorize():
    auth_url = get_oauth_url()
    return redirect(auth_url)


@app.route("/auth/callback")
def callback():

    code = request.args.get("code")

    if not code:
        return "No authorization code received.", 400

    token_data = get_token(code)

    rouvy_rider_profile = get_rouvy_rider(
        token_data["access_token"]
    )

    save_rider_auth(
        token_data,
        rouvy_rider_profile
    )

    return "ROUVY authorisation successful. You can close this browser window and exit the Flask process."


if __name__ == "__main__":

    webbrowser.open(CALLBACKURL)

    app.run(
        debug=False,
        port=3000
    )
