from flask import Flask, redirect, request, jsonify, session, send_from_directory
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import urllib.parse
import datetime
import requests

app = Flask(__name__)
CORS(app)
# Load environment variables from .env file
load_dotenv()

# Secret key for Flask Sessions
app.secret_key = '53d355f8-571a-4590-a310-1f9579440851'

# Flask session config
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)

# Retrieve environment variables
client_id = os.getenv('CLIENT_ID')
client_secret = os.getenv('CLIENT_SECRET')
redirect_uri = os.getenv('REDIRECT_URI')

# Spotify API URLs
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email'

    # Parameters for the authorization URL
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': redirect_uri,
        'show_dialog': True  # Set to False for running application
    }

    # Generate authorization URL
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    # Redirect user to Spotify login
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    if not code:
        return "No code in request", 400

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    res = requests.post("https://accounts.spotify.com/api/token", data=payload, headers=headers)

    if res.status_code != 200:
        return f"Failed to get token: {res.text}", 400

    access_token = res.json().get("access_token")

    return redirect(f"http://localhost:3000/?access_token={access_token}")


frontend_folder=os.path.join(os.getcwd(),"..","Frontend")
dist_folder=os.path.join(frontend_folder,"dist")

@app.route("/",defaults={"filename":""})
@app.route("/<path:filename>")
def index(filename):
    if not filename:
        filename="index.html"
    return send_from_directory(dist_folder,filename)

import routes


if __name__ == "__main__":
    app.run(debug=True)