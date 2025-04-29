from flask import Flask, redirect, request, jsonify, session, send_from_directory
from flask_session import Session
from flask_cors import CORS
from dotenv import load_dotenv
import os
import urllib.parse
import datetime
import requests
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Use environment variable for CORS origin in production
frontend_url = os.environ.get('FRONTEND_URL', 'https://spotify-comparison-frontend.onrender.com')
CORS(app, supports_credentials=True, origins=[frontend_url], allow_headers=["Authorization", "Content-Type"])

# Load environment variables from .env file
load_dotenv()

# Secret key for Flask Sessions - use environment variable in production
app.secret_key = os.environ.get('SECRET_KEY', '53d355f8-571a-4590-a310-1f9579440851')

# Flask session config
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_USE_SIGNER'] = True
Session(app)


from . import routes

# Retrieve environment variables
client_id = os.environ.get('CLIENT_ID')
client_secret = os.environ.get('CLIENT_SECRET')
# Use environment variable for redirect URI in production
redirect_uri = os.environ.get('REDIRECT_URI')#, 'http://localhost:5000/callback')

# Log configuration
logger.info(f"Client ID: {client_id[:5]}..." if client_id else "CLIENT_ID not set")
logger.info(f"Redirect URI: {redirect_uri}")

# Spotify API URLs
AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'
# =====================
# Authentication Routes
# =====================

@app.route('/login')
def login():
    # Get the current player from session or use player1 as default
    current_player = session.get('current_player', 1)
    logger.debug(f"Login initiated for player {current_player}")
    
    scope = 'user-read-private user-read-email user-top-read'

    # Parameters for the authorization URL
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'scope': scope,
        'redirect_uri': redirect_uri,
        'show_dialog': True,  # Set to False for production
        'state': str(current_player)  # Pass player ID in state
    }

    # Generate authorization URL
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    
    logger.debug(f"Redirecting to Spotify auth URL: {auth_url[:50]}...")

    # Redirect user to Spotify login
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")  # Get player ID from state
    
    logger.debug(f"Callback received. Code present: {bool(code)}, State: {state}")
    
    if not code:
        logger.error("No code in callback request")
        return "No code in request", 400
    
    # Store the player ID in session
    if state:
        session['current_player'] = int(state)
        logger.debug(f"Set current_player in session to {state}")

    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret,
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    logger.debug("Requesting access token from Spotify")
    res = requests.post(TOKEN_URL, data=payload, headers=headers)

    if res.status_code != 200:
        logger.error(f"Failed to get token: {res.status_code} - {res.text}")
        return f"Failed to get token: {res.text}", 400

    token_info = res.json()
    
    # Store tokens in session
    session['access_token'] = token_info['access_token']
    session['refresh_token'] = token_info['refresh_token']
    session['expires_at'] = datetime.datetime.now().timestamp() + token_info['expires_in']
    
    logger.info(f"Successfully obtained access token for player {session.get('current_player')}")
    ##nEW CODE
    frontend_url = os.environ.get('FRONTEND_URL', 'https://spotify-comparison-frontend.onrender.com')
    
    # Add access token as a query parameter for the frontend
    token = session.get('access_token')
    player_id = session.get('current_player', 1)
    
    # Redirect to the frontend with token
    return redirect(f"{frontend_url}?access_token={token}&player_id={player_id}")

    # # Save user data and redirect to frontend
    # return redirect('/api/save_user_data')

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        logger.warning("No refresh token in session")
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:
        logger.debug("Token expired, refreshing...")
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': client_id,
            'client_secret': client_secret
        }

        # Request a new access token using the refresh token
        response = requests.post(TOKEN_URL, data=req_body)
        
        if response.status_code != 200:
            logger.error(f"Failed to refresh token: {response.status_code} - {response.text}")
            return redirect('/login')
            
        new_token_info = response.json()

        # Store the new access token and expiration time
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.datetime.now().timestamp() + new_token_info['expires_in']
        
        logger.debug("Token refreshed successfully")
        return redirect('/api/save_user_data')
    
    return redirect('/api/user_status')

def get_token_from_header():
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return None
    try:
        auth_type, token = auth_header.split()
        if auth_type.lower() != 'bearer':
            return None
        return token
    except ValueError:
        return None

# ==============
# Serve Frontend
# ==============
frontend_folder = os.path.join(os.getcwd(), "..", "Frontend")
dist_folder = os.path.join(frontend_folder, "dist")

@app.route("/", defaults={"filename": ""})
@app.route("/<path:filename>")
def index(filename):
    if not filename:
        filename = "index.html"
    return send_from_directory(dist_folder, filename)

# Import all routes

if __name__ == "__main__":
    app.run(debug=True, port=5000)