from flask import jsonify, request, session, redirect
from app import app
import math
import numpy as np
from collections import Counter
import requests
import json
import datetime
from urllib.parse import urlencode

# User class from Orlando V2
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
        # Track IDs for comparison
        self.songsS = None
        self.songsM = None
        self.songsL = None
        self.artistsS = None
        self.artistsM = None
        self.artistsL = None

# Create two player instances
player1 = User()
player2 = User()

# Constants
API_BASE_URL = 'https://api.spotify.com/v1/'

# ===================
# Analysis Functions
# ===================
def idLists(s):
    """Extract song and artist IDs from track data"""
    s_idlist = []
    a_idlist = []
    for i in range(len(s)):
        s_idlist.append(s[i]['id'])
        if s[i]['artists_id'] not in a_idlist:
            a_idlist.append(s[i]['artists_id'])
    return s_idlist, a_idlist

def shareds(p1, p2):
    """Calculate percentage of shared items between two lists"""
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

def top(p1, p2):
    """Find the top common song between users"""
    try:
        for i in range(len(p1)):
            if p1[i] in p2:
                a = i
                b = p2.index(p1[i])
                break
        for i in range(len(p2)):
            if p2[i] in p1:
                B = p1.index(p2[i])
                A = i
                break
        c = a + b
        C = A + B
        # Returns top song
        if c < C:
            return p1[a]
        elif c == C:
            return p1[a]
        else:
            return p2[A]
    except:
        return 'No common songs found'

def pointsLog(pShared):
    """Logarithmic scaling function for similarity scores"""
    if pShared < 1.0471:
        pShared = 1.0471
    return 100 / math.log(100, pShared)

def sharedsV2(a, b):
    """Calculate Jaccard similarity between two sets"""
    inter = len(set(a) & set(b))
    union = len(set(a) | set(b))
    if union == 0:
        union = 1
    return (inter / union) * 100

def simTopSongs(topSongs1, topSongs2):
    """Calculate similarity between top songs"""
    ids1 = [song['id'] for song in topSongs1]
    ids2 = [song['id'] for song in topSongs2]
    return pointsLog(sharedsV2(ids1, ids2))

def simEras(topSongs1, topSongs2, headers):
    """Calculate similarity of music eras between users"""
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
    """Calculate similarity of song characteristics between users"""
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
    """Calculate similarity of genres between users"""
    shared = len(set(genres1).intersection(set(genres2)))
    total = len(set(genres1).union(set(genres2)))
    if total == 0:
        return 0
    return (shared / total) * 100

def produceV2results(genres1, topSongs1, genres2, topSongs2, headers):
    """Calculate overall similarity between users"""
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

    # Get top common song
    ids1 = [song['id'] for song in topSongs1]
    ids2 = [song['id'] for song in topSongs2]
    topSongId = top(ids1, ids2)
    
    # Find song details from ID
    topSongDetails = {}
    for song in topSongs1:
        if song['id'] == topSongId:
            topSongDetails = song
            break
    if not topSongDetails:
        for song in topSongs2:
            if song['id'] == topSongId:
                topSongDetails = song
                break
    
    return {
        'topSongsScore': round(topSongsScore, 2),
        'erasScore': round(erasScore, 2),
        'characteristicsScore': round(characteristicsScore, 2),
        'genresScore': round(genresScore, 2),
        'finalScore': round(finalScore, 2),
        'topSong': topSongDetails if topSongDetails else {"name": "No common song found", "artists_name": ""}
    }

# ======================
# API Routes
# ======================

# Test data for development
json_string = {"data":
        [{'name': 'The Galway Girl', 'id': '1i92xro4lPLyjiOd3y2aqA', 'artists_name': 'Sharon Shannon', 'artists_id': '6gABJRqeRV4XW6T8vP9QEn', 'image': 'https://i.scdn.co/image/ab67616d0000b27369b1fdf0417848e1905aebe7'},
        {'name': 'Tell Me Ma', 'id': '0Z3p6q8nol4dlf3b0WRI1a', 'artists_name': 'Gaelic Storm', 'artists_id': '5dlzTgw97q5k5ws89Ww1UK', 'image': 'https://i.scdn.co/image/ab67616d0000b2737fdb0728b6252787c72ff443'}, 
        {'name': 'The Rocky Road To Dublin', 'id': '2AMHDHBuhSvcEhbv5IVSB1', 'artists_name': 'The High Kings', 'artists_id': '6wXjctGBzxkT0ghwfQ8FC0', 'image': 'https://i.scdn.co/image/ab67616d0000b27379469ad2979872c3fe41c3ad'}, 
        {'name': 'Irish Pub Song', 'id': '6zX3HwSuoQThrabeoHJvCs', 'artists_name': 'The High Kings', 'artists_id': '6wXjctGBzxkT0ghwfQ8FC0', 'image': 'https://i.scdn.co/image/ab67616d0000b273cd95e0a5bb4765ede11154fd'}, 
        {'name': 'Green and Red of Mayo', 'id': '1QfY6hlEyWSdaT8XTVGEa1', 'artists_name': 'The Saw Doctors', 'artists_id': '7jzktaiZ0YO4RquEFi4oKp', 'image': 'https://i.scdn.co/image/ab67616d0000b27334936dd63957a5cdae5461ae'}, 
        {'name': 'Whiskey in the Jar', 'id': '1UzofFX5AkfTDnwjcBkM4J', 'artists_name': 'The Dubliners', 'artists_id': '72RvmgEg2omdlMV9aExO6a', 'image': 'https://i.scdn.co/image/ab67616d0000b2730a6473e2fd56ea8049a234b1'}, 
        {'name': 'The Island', 'id': '1kSkAYLMmGyNdBQ3zP8xoQ', 'artists_name': 'Paul Brady', 'artists_id': '7lauB9o5ZYmU5lTBOw7w8L', 'image': 'https://i.scdn.co/image/ab67616d0000b273b1c97f9036d60197ef06d54e'}, 
        {'name': 'Nothing but the Same Old Story', 'id': '2jAAjATGx5CWxZx6jYdwwz', 'artists_name': 'Paul Brady', 'artists_id': '7lauB9o5ZYmU5lTBOw7w8L', 'image': 'https://i.scdn.co/image/ab67616d0000b2733838a8c2d2dfec47c3b9eaa9'}, 
        {'name': "Donald Where's Your Trousers", 'id': '3gzuSrER3D3Qunaz20bUZn', 'artists_name': 'The Irish Rovers', 'artists_id': '0tkKwWigaADLYB9HdFCjYo', 'image': 'https://i.scdn.co/image/ab67616d0000b2737bb2c012ee757142d3b3a000'}]
}

@app.route("/api/card_data")
def carddata():
    """Return test card data for development"""
    token = get_token_from_header()
    if token:
        # In a real production app, we would fetch this from Spotify API
        # Right now, returning test data
        return jsonify([(song['name'], song['artists_name'], song['image']) for song in json_string["data"]])
    return jsonify({"error": "Unauthorized"}), 401

@app.route("/api/testdata")
def testdata():
    """Test data endpoint"""
    return jsonify([(song['name'], song['image']) for song in json_string["data"]])

# New endpoints for two-user functionality
@app.route("/api/user_status")
def user_status():
    """Return the login status of both users"""
    return jsonify({
        "player1": {
            "saved": player1.saved, 
            "name": player1.name, 
            "picture": player1.picture
        },
        "player2": {
            "saved": player2.saved, 
            "name": player2.name, 
            "picture": player2.picture
        }
    })

@app.route("/api/login/<int:player_id>")
def player_login(player_id):
    """Initiate login flow for a specific player"""
    if player_id not in [1, 2]:
        return jsonify({"error": "Invalid player ID"}), 400
    
    session['current_player'] = player_id
    return redirect('/login')

@app.route("/api/save_user_data")
def save_user_data():
    """Save user data after Spotify login"""
    if 'access_token' not in session:
        return jsonify({"error": "No access token found"}), 401
    
    # Identify which player we're saving data for
    player_id = session.get('current_player', 1)
    
    # Fetch user data from Spotify API
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    try:
        # Get top tracks for different time ranges
        response = requests.get(f"{API_BASE_URL}me/top/tracks?time_range=short_term&limit=50", headers=headers)
        data = response.json()
        shortTracks = []
        for item in data.get("items", []):
            shortTracks.append({
                "name": item["name"],
                "id": item["id"],
                "artists_name": item["artists"][0]["name"],
                "artists_id": item["artists"][0]["id"],
                "image": item["album"]["images"][0]["url"] if item["album"]["images"] else None
            })

        response = requests.get(f"{API_BASE_URL}me/top/tracks?time_range=medium_term&limit=50", headers=headers)
        data = response.json()
        medTracks = []
        for item in data.get("items", []):
            medTracks.append({
                "name": item["name"],
                "id": item["id"],
                "artists_name": item["artists"][0]["name"],
                "artists_id": item["artists"][0]["id"],
                "image": item["album"]["images"][0]["url"] if item["album"]["images"] else None
            })

        response = requests.get(f"{API_BASE_URL}me/top/tracks?time_range=long_term&limit=50", headers=headers)
        data = response.json()
        longTracks = []
        for item in data.get("items", []):
            longTracks.append({
                "name": item["name"],
                "id": item["id"],
                "artists_name": item["artists"][0]["name"],
                "artists_id": item["artists"][0]["id"],
                "image": item["album"]["images"][0]["url"] if item["album"]["images"] else None
            })

        # Get top artists and genres
        response = requests.get(f"{API_BASE_URL}me/top/artists?time_range=medium_term&limit=50", headers=headers)
        data = response.json()
        topGenres = set()
        topArtists = []
        for artist in data.get("items", []):
            topGenres.update(artist["genres"])
            topArtists.append(artist)
        
        # Get user profile
        profile = requests.get(f"{API_BASE_URL}me", headers=headers).json()
        
        # Save data to appropriate player
        player = player1 if player_id == 1 else player2
        player.shortTracks = shortTracks
        player.medTracks = medTracks
        player.longTracks = longTracks
        player.topGenres = list(topGenres)
        player.topArtists = topArtists
        player.name = profile.get('display_name')
        player.picture = profile.get("images")[0]["url"] if profile.get("images") else None
        player.saved = True
        
        # Generate ID lists for comparison
        player.songsS, player.artistsS = idLists(player.shortTracks)
        player.songsM, player.artistsM = idLists(player.medTracks)
        player.songsL, player.artistsL = idLists(player.longTracks)
        
        # Create an access token for redirecting to frontend
        access_token = session['access_token']
        
        # Redirect to the frontend with the token
        return redirect(f"http://localhost:3000/?access_token={access_token}")
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/reset/<int:player_id>")
def reset_player(player_id):
    """Reset a player's data"""
    if player_id == 1:
        player1.__init__()
    elif player_id == 2:
        player2.__init__()
    else:
        return jsonify({"error": "Invalid player ID"}), 400
    
    return jsonify({"success": True})

@app.route("/api/reset_all")
def reset_all():
    """Reset both players' data"""
    player1.__init__()
    player2.__init__()
    return jsonify({"success": True})

@app.route("/api/comparison")
def get_comparison():
    """Get comparison results between the two users"""
    if not player1.saved or not player2.saved:
        return jsonify({"error": "Both users need to be logged in"}), 400
    
    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    
    try:
        # Compute comparisons for all time ranges
        resultsSHORT = produceV2results(player1.topGenres, player1.shortTracks, player2.topGenres, player2.shortTracks, headers)
        resultsMED = produceV2results(player1.topGenres, player1.medTracks, player2.topGenres, player2.medTracks, headers)
        resultsLONG = produceV2results(player1.topGenres, player1.longTracks, player2.topGenres, player2.longTracks, headers)
        
        # Merge results
        return jsonify({
            "success": True,
            "players": {
                "player1": {
                    "name": player1.name,
                    "picture": player1.picture,
                },
                "player2": {
                    "name": player2.name,
                    "picture": player2.picture,
                }
            },
            "short_term": resultsSHORT,
            "medium_term": resultsMED,
            "long_term": resultsLONG,
            "sharedGenres": round(pointsLog(simGenres(player1.topGenres, player2.topGenres)), 2)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/player/<int:player_id>/tracks")
def get_player_tracks(player_id):
    """Get a player's tracks for display"""
    player = player1 if player_id == 1 else player2
    
    if not player.saved:
        return jsonify({"error": "Player not logged in"}), 400
    
    time_range = request.args.get('time_range', 'medium')
    
    if time_range == 'short':
        tracks = player.shortTracks
    elif time_range == 'medium':
        tracks = player.medTracks
    elif time_range == 'long':
        tracks = player.longTracks
    else:
        return jsonify({"error": "Invalid time range"}), 400
    
    return jsonify({
        "success": True,
        "tracks": tracks
    })

def get_token_from_header():
    """Extract token from Authorization header"""
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