# =======
# Imports
# =======
from flask import Flask, redirect, request, jsonify, session
from flask_session import Session
from dotenv import load_dotenv
import os
import urllib.parse
import datetime
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import math
import json
from collections import Counter
import numpy as np

# ==========
# User Class
# ==========
class User:
    def __init__(self):
        self.saved = False
        self.picture = None
        self.name = None
        self.longTracks = None
        self.medTracks = None
        self.shortTracks = None
        self.topGenres = None
        self.topArtists = None
        self.playlists = None
        self.followed_artists = None

player1 = User()
player2 = User()

# ==================
# Analysis Functions
# ==================
def idLists(s):
  #produces a list of the item ids for each user
  s_idlist=[]
  a_idlist=[]
  for i in range(len(s)):
    s_idlist.append(s[i]['id'])
    if s[i]['artists_id'] not in a_idlist:
      a_idlist.append(s[i]['artists_id'])
  return s_idlist, a_idlist

def shareds(p1, p2):
    # produces a list of all songs shared by users
    a = p1
    b = p2
    sharedc = 0
    for i in range(len(a)):
        if a[i] in b:
            sharedc += 1
    denominator = len(a) + len(b) - 2 * sharedc
    if denominator == 0:
        denominator = 1
    percentage = (sharedc / denominator) * 100
    return percentage

def top(p1,p2):
  #finds the top common songs between users
  try:
      for i in range(len(p1)):
        if p1[i] in p2:
          a=i
          b=p2.index(p1[i])

          break
      for i in range(len(p2)):
        if p2[i] in p1:
          B=p1.index(p2[i])
          A=i
          break
      c=a+b
      C=A+B
      #returns toppest song
      if c<C:
        return(p1[a])
      elif c==C:
        return p1[a]
      else:
        return p2[A]
  except:
      return 'probably radiohead idk'

def produceResults(res,a1,a2,s1,s2):
  #find the results for each data set, returning a dictionary
  res["sharedartists"]=shareds(a1,a2)
  res["sharedsongs"]=shareds(s1,s2)
  res["topsong"]=top(s1,s2)
  return res

# =====================
# V2 Analysis Functions
# =====================
def sharedsV2(a, b):
    inter = len(set(a) & set(b))
    union = len(set(a) | set(b))
    if union == 0:
        union = 1
    return (inter / union) * 100

def produceV2results(genres1, topSongs1, genres2, topSongs2, headers):
    weightingsDict = {
        'simTopSongs': 0.35,
        'simEras': 0.2,
        'simCharacteristics': 0,
        'simGenres': 0.45
    }
    # Run each similarity function
    topSongsScore = simTopSongs(topSongs1, topSongs2)
    erasScore = pointsLog(simEras(topSongs1, topSongs2, headers))
    characteristicsScore = pointsLog(simCharacteristics(topSongs1, topSongs2, headers))
    genresScore = pointsLog(simGenres(genres1, genres2))

    # Weighted average
    finalScore = (
        topSongsScore * weightingsDict['simTopSongs'] +
        erasScore * weightingsDict['simEras'] +
        characteristicsScore * weightingsDict['simCharacteristics'] +
        genresScore * weightingsDict['simGenres']
    )

    topSong = top(topSongs1, topSongs2)

    return {
        'topSongsScore': round(topSongsScore, 2),
        'erasScore': round(erasScore, 2),
        'characteristicsScore': round(characteristicsScore, 2),
        'genresScore': round(genresScore, 2),
        'finalScore': round(finalScore, 2),
        'topSong':topSong
    }

def simTopSongs(topSongs1, topSongs2):
    ids1 = [song['id'] for song in topSongs1]
    ids2 = [song['id'] for song in topSongs2]
    return pointsLog(sharedsV2(ids1, ids2))

def simEras(topSongs1, topSongs2, headers):
    def getTrackData(trackIds):
        # Break into chunks of 50 (max allowed by Spotify)
        trackData = []
        for i in range(0, len(trackIds), 50):
            idsChunk = ",".join([track['id'] for track in trackIds[i:i+50]])
            url = f"{API_BASE_URL}tracks?ids={idsChunk}"
            resp = requests.get(url, headers=headers).json()
            trackData.extend(resp.get("tracks", []))
        return trackData

    def getAlbumYears(albumIds):
        albumYears = {}
        for i in range(0, len(albumIds), 20):  # Albums endpoint limit = 20
            idsChunk = ",".join(albumIds[i:i+20])
            url = f"{API_BASE_URL}albums?ids={idsChunk}"
            resp = requests.get(url, headers=headers).json()
            for album in resp.get("albums", []):
                release = album.get("release_date", "")[:4]
                try:
                    year = int(release)
                    decade = (year // 10) * 10
                    albumYears[album["id"]] = decade
                except ValueError:
                    continue  # Skip if year is invalid
        return albumYears

    def getDecadeCounts(trackIds):
        tracks = getTrackData(trackIds)
        albumIds = [t["album"]["id"] for t in tracks if "album" in t]
        albumDecades = getAlbumYears(albumIds)
        decades = [albumDecades.get(t["album"]["id"]) for t in tracks if t["album"]["id"] in albumDecades]
        return Counter(filter(None, decades))  # Remove None values

    # Get frequency counts per decade
    counts1 = getDecadeCounts(topSongs1)
    counts2 = getDecadeCounts(topSongs2)

    if not counts1 or not counts2:
        return 0

    # Compute weighted similarity
    sharedDecades = set(counts1) & set(counts2)
    totalDecades = set(counts1) | set(counts2)

    sharedWeight = sum(min(counts1[d], counts2[d]) for d in sharedDecades)
    totalWeight = sum((counts1 | counts2).values())  # Union counts (max of each)

    return (sharedWeight / totalWeight) * 100

def simCharacteristics(topSongs1, topSongs2, headers):
    def getAudioFeatures(trackIds):
        features = []
        for i in range(0, len(trackIds), 100):  # 100 is the max batch size for /audio-features
            idsChunk = ",".join(trackIds[i:i+100])
            url = f"{API_BASE_URL}audio-features?ids={idsChunk}"
            resp = requests.get(url, headers=headers).json()
            features.extend([f for f in resp.get("audio_features", []) if f])
        return features

    # Spotify audio features to compare
    FEATURE_KEYS = [
        "acousticness", "danceability", "energy", "instrumentalness",
        "liveness", "speechiness", "valence", "tempo"
    ]

    def extractFeatureVector(features):
        vectors = []
        for f in features:
            try:
                vec = [f[k] for k in FEATURE_KEYS]
                vectors.append(vec)
            except KeyError:
                continue
        return np.mean(vectors, axis=0) if vectors else None

    # Get features and mean vectors
    features1 = getAudioFeatures([track["id"] for track in topSongs1])
    features2 = getAudioFeatures([track["id"] for track in topSongs2])
    vec1 = extractFeatureVector(features1)
    vec2 = extractFeatureVector(features2)

    if vec1 is None or vec2 is None:
        return 0

    # Cosine similarity
    dot = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    similarity = dot / (norm1 * norm2)

    return similarity * 100

def simGenres(genres1, genres2):
    shared = len(set(genres1).intersection(set(genres2)))
    total = len(set(genres1).union(set(genres2)))
    if total == 0:
        return 0
    return (shared / total) * 100

# ===============
# Other Functions
# ===============

def lookupSong(songID):
    try:
        if 'access_token' not in session:
            raise Exception("No access token found in session")

        accessToken = session['access_token']
        spClient = spotipy.Spotify(auth=accessToken)

        track = spClient.track(songID)
        songName = track['name']
        artistName = track['artists'][0]['name']
        return songName, artistName
    except Exception as e:
        print(f"Error looking up song: {e}")
        return None, None

def pointsLog(pShared):
    if pShared < 1.0471:
        pShared = 1.0471
    return 100/math.log(100, pShared)

# ===========
# Flask Setup
# ===========
app = Flask(__name__)

# =========
# Api Setup
# =========

# Load environment variables from .env file
load_dotenv()

# Secret key for Flask Sessions
app.secret_key = 'bd46ac363ef444e68b256539b213b9bb'

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

# ============
# WebApp Pages
# ============
@app.route('/')
def index():
    player1.saved = False
    player2.saved = False
    return redirect('/home')

@app.route('/home')
def home():
    if not player1.saved:
        return "Welcome! Player 1: <a href='/login'>Login with Spotify</a>"
    elif not player2.saved:
        return "Player 2: <a href='/login'>Login with Spotify</a>"
    else:
        return "<a href='/analysis'>Start Analysis</a>"

@app.route('/login')
def login():
    scope = 'user-read-private user-read-email user-top-read'

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

@app.route('/callback')
def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})

    if 'code' in request.args:
        # Exchange authorization code for access token
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri,
            'client_id': client_id,
            'client_secret': client_secret
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        # Store tokens and expiration time in Session
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.datetime.now().timestamp() + token_info['expires_in']

        return redirect('/save_data')

@app.route('/menu')
def menu():
    return "<a href='/save_data'>Save your data</a> "

@app.route('/save_data')
def get_data():
    if 'access_token' not in session:
        return redirect('/login')

    # If the access token has expired, refresh it
    if datetime.datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    # Make request to get top tracks
    response = requests.get(API_BASE_URL + 'me/top/tracks?time_range=short_term', headers=headers)
    data = response.json()
    shortTracks = []
    for item in data["items"]:
        shortTracks.append({"name":item["name"],"id":item["id"],"artists_name":item["artists"][0:][0]["name"],"artists_id":item["artists"][0:][0]["id"]})

    response = requests.get(API_BASE_URL + 'me/top/tracks?time_range=medium_term', headers=headers)
    data = response.json()
    medTracks = []
    for item in data["items"]:
        medTracks.append({"name":item["name"],"id":item["id"],"artists_name":item["artists"][0:][0]["name"],"artists_id":item["artists"][0:][0]["id"]})

    response = requests.get(API_BASE_URL + 'me/top/tracks?time_range=long_term', headers=headers)
    data = response.json()
    longTracks = []
    for item in data["items"]:
        longTracks.append({"name":item["name"],"id":item["id"],"artists_name":item["artists"][0:][0]["name"],"artists_id":item["artists"][0:][0]["id"]})

    # Make request to get top artists and genres
    response = requests.get(API_BASE_URL + 'me/top/artists?time_range=medium_term', headers=headers)
    data = response.json()
    topGenres = set()  # Using a set to avoid duplicates
    topArtists = []
    for artist in data["items"]:
        topGenres.update(artist["genres"])  # Add multiple genres from each artist
        topArtists.append(artist)
    topGenres = list(topGenres)  # Convert set back to a list if needed

    if not player1.saved:
        player1.shortTracks = shortTracks
        player1.medTracks = medTracks
        player1.longTracks = longTracks
        player1.topGenres = topGenres
        player1.topArtists = topArtists
        player1.saved = True
        player1.name = requests.get(API_BASE_URL + 'me', headers=headers).json()['display_name']


        profile = requests.get(API_BASE_URL + 'me', headers=headers).json()
        player1.picture = profile["images"][0]["url"] if profile.get("images") else None

        #player1.playlists = playlists
    elif not player2.saved:
        player2.shortTracks = shortTracks
        player2.medTracks = medTracks
        player2.longTracks = longTracks
        player2.topGenres = topGenres
        player2.topArtists = topArtists
        player2.saved = True
        player2.name = requests.get(API_BASE_URL + 'me', headers=headers).json()['display_name']


        profile = requests.get(API_BASE_URL + 'me', headers=headers).json()
        player2.picture = profile["images"][0]["url"] if profile.get("images") else None

    print("Player 1 Long History:")
    print(player1.longTracks)
    print("Player 2 Long History:")
    print(player2.longTracks)
    print("Player 1 Med History:")
    print(player1.medTracks)
    print("Player 2 Med History:")
    print(player2.medTracks)
    print("Player 1 Short History:")
    print(player1.shortTracks)
    print("Player 2 Short History:")
    print(player2.shortTracks)
    print()
    print("Player 1 Top Genres:")
    print(player1.topGenres)
    print("Player 2 Top Genres:")
    print(player2.topGenres)
    return redirect('/home')

@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')

    if datetime.datetime.now().timestamp() > session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': client_id,
            'client_secret': client_secret
        }

        # Request a new access token using the refresh token
        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()

        # Store the new access token and expiration time
        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/get_data')

@app.route('/analysis')
def analysis():

    # Ensure access token is still valid
    if 'access_token' not in session:
        return redirect('/login')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    # Assign data directly from track attributes
    player1.songsM, player1.artistsM = idLists(player1.medTracks)
    player2.songsM, player2.artistsM = idLists(player2.medTracks)
    player1.songsS, player1.artistsS = idLists(player1.shortTracks)
    player2.songsS, player2.artistsS = idLists(player2.shortTracks)
    player1.songsL, player1.artistsL = idLists(player1.longTracks)
    player2.songsL, player2.artistsL = idLists(player2.longTracks)

    # Produce a dictionary to compile the results using the new comparison functions
    resultsMED = produceV2results(player1.topGenres, player1.medTracks, player2.topGenres, player2.medTracks, headers)
    resultsSHORT = produceV2results(player1.topGenres, player1.shortTracks, player2.topGenres, player2.shortTracks, headers)
    resultsLONG = produceV2results(player1.topGenres, player1.longTracks, player2.topGenres, player2.longTracks, headers)

    # Gather shared genres (you can keep this function or modify based on your use case)
    results = {}
    results["sharedgenres"] = shareds(player1.topGenres, player2.topGenres)

    # Compile the results for display
    results["medium"] = resultsMED
    results["short"] = resultsSHORT
    results["long"] = resultsLONG
    results["player1Image"] = player1.picture
    results["player2Image"] = player2.picture

    # Return the HTML results
    return f"""
    <h1>Spotify Comparison Results</h1>

    <h2>Short Term</h2>
    <p>Top Songs Similarity: {resultsSHORT["topSongsScore"]}%</p>
    <p>Genres Similarity: {resultsSHORT["genresScore"]}%</p>
    <p>Characteristics Similarity: {resultsSHORT["characteristicsScore"]}%</p>
    <p>Era Similarity: {resultsSHORT["erasScore"]}%</p>
    <p>Overall Similarity: {resultsSHORT["finalScore"]}%</p>
    <p>Top Song: {resultsSHORT["topSong"]}%</p>

    <h2>Medium Term</h2>
    <p>Top Songs Similarity: {resultsMED["topSongsScore"]}%</p>
    <p>Genres Similarity: {resultsMED["genresScore"]}%</p>
    <p>Characteristics Similarity: {resultsMED["characteristicsScore"]}%</p>
    <p>Era Similarity: {resultsMED["erasScore"]}%</p>
    <p>Overall Similarity: {resultsMED["finalScore"]}%</p>
    <p>Top Song: {resultsMED["topSong"]}%</p>

    <h2>Long Term</h2>
    <p>Top Songs Similarity: {resultsLONG["topSongsScore"]}%</p>
    <p>Genres Similarity: {resultsLONG["genresScore"]}%</p>
    <p>Characteristics Similarity: {resultsLONG["characteristicsScore"]}%</p>
    <p>Era Similarity: {resultsLONG["erasScore"]}%</p>
    <p>Overall Similarity: {resultsLONG["finalScore"]}%</p>
    <p>Top Song: {resultsLONG["topSong"]}%</p>

    <h2>Images</h2>
    <p>Player 1: {player1.picture}</p>
    <p>Player 2: {player2.picture}</p>
    <br>
    <a href='/'>Back to Home</a>
    """

# ==========
# Run WebApp
# ==========
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)