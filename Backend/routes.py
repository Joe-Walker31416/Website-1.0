from flask import jsonify, request, session, redirect
import math
import numpy as np
from collections import Counter
import requests
import json
import datetime
import os
import logging
from urllib.parse import urlencode

from flask import jsonify, request, session, redirect
import logging

from .app import app
# Configure better logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add this as a new dictionary to store tokens
player_tokens = {
    1: None,
    2: None
}

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

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
        # Add extra safety check for empty lists
        if not p1 or not p2:
            return 'No common songs found'
            
        found_common = False
        for i in range(len(p1)):
            if p1[i] in p2:
                a = i
                b = p2.index(p1[i])
                found_common = True
                break
                
        if not found_common:
            return 'No common songs found'
            
        found_common = False
        for i in range(len(p2)):
            if p2[i] in p1:
                B = p1.index(p2[i])
                A = i
                found_common = True
                break
                
        if not found_common:
            return 'No common songs found'
            
        c = a + b
        C = A + B
        # Returns top song
        if c < C:
            return p1[a]
        elif c == C:
            return p1[a]
        else:
            return p2[A]
    except Exception as e:
        logger.error(f"Error finding top song: {str(e)}")
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
    try:
        ids1 = [song['id'] for song in topSongs1]
        ids2 = [song['id'] for song in topSongs2]
        return pointsLog(sharedsV2(ids1, ids2))
    except Exception as e:
        logger.error(f"Error in simTopSongs: {str(e)}")
        return 0

def simEras(topSongs1, topSongs2, headers):
    """Calculate similarity of music eras between users"""
    try:
        def getTrackData(trackIds):
            # Break into chunks of 50 (max allowed by Spotify)
            trackData = []
            for i in range(0, len(trackIds), 50):
                idsChunk = ",".join([track['id'] for track in trackIds[i:i+50]])
                url = f"{API_BASE_URL}tracks?ids={idsChunk}"
                resp = requests.get(url, headers=headers)
                
                # Check if request was successful
                if resp.status_code != 200:
                    logger.error(f"Error fetching track data: {resp.status_code} - {resp.text}")
                    continue
                    
                data = resp.json()
                trackData.extend(data.get("tracks", []))
            return trackData

        def getAlbumYears(albumIds):
            albumYears = {}
            for i in range(0, len(albumIds), 20):  # Albums endpoint limit = 20
                idsChunk = ",".join(albumIds[i:i+20])
                url = f"{API_BASE_URL}albums?ids={idsChunk}"
                resp = requests.get(url, headers=headers)
                
                # Check if request was successful
                if resp.status_code != 200:
                    logger.error(f"Error fetching album data: {resp.status_code} - {resp.text}")
                    continue
                    
                data = resp.json()
                for album in data.get("albums", []):
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
    except Exception as e:
        logger.error(f"Error in simEras: {str(e)}")
        return 0

def simCharacteristics(topSongs1, topSongs2, headers):
    """Calculate similarity of song characteristics between users"""
    try:
        def getAudioFeatures(trackIds):
            features = []
            for i in range(0, len(trackIds), 100):  # 100 is the max batch size for /audio-features
                idsChunk = ",".join(trackIds[i:i+100])
                url = f"{API_BASE_URL}audio-features?ids={idsChunk}"
                resp = requests.get(url, headers=headers)
                
                # Check if request was successful
                if resp.status_code != 200:
                    logger.error(f"Error fetching audio features: {resp.status_code} - {resp.text}")
                    continue
                    
                data = resp.json()
                features.extend([f for f in data.get("audio_features", []) if f])
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
    except Exception as e:
        logger.error(f"Error in simCharacteristics: {str(e)}")
        return 0
   
def simGenres(genres1, genres2):
    """Calculate similarity of genres between users"""
    try:
        # Add extra safety check for empty lists
        if not genres1 or not genres2:
            return 0
            
        shared = len(set(genres1).intersection(set(genres2)))
        total = len(set(genres1).union(set(genres2)))
        if total == 0:
            return 0
        return (shared / total) * 100
    except Exception as e:
        logger.error(f"Error in simGenres: {str(e)}")
        return 0

def produceV2results(genres1, topSongs1, genres2, topSongs2, headers):
    """Calculate overall similarity between users"""
    try:
        # Set up weightings for different similarity components
        weightingsDict = {
            'simTopSongs': 0.35,
            'simEras': 0.2,
            'simCharacteristics': 0,
            'simGenres': 0.45
        }
        
        # Run each similarity function with error handling
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
        
        # Return results with proper rounding
        return {
            'topSongsScore': round(topSongsScore, 2),
            'erasScore': round(erasScore, 2),
            'characteristicsScore': round(characteristicsScore, 2),
            'genresScore': round(genresScore, 2),
            'finalScore': round(finalScore, 2),
            'topSong': topSongDetails if topSongDetails else {"name": "No common song found", "artists_name": ""}
        }
    except Exception as e:
        logger.error(f"Error in produceV2results: {str(e)}")
        # Return a default result structure to prevent frontend errors
        return {
            'topSongsScore': 0,
            'erasScore': 0,
            'characteristicsScore': 0,
            'genresScore': 0,
            'finalScore': 0,
            'topSong': {"name": "No common song found", "artists_name": ""}
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
    """Return card data for development"""
    try:
        token = get_token_from_header()
        if token:
            # In a real production app, we would fetch this from Spotify API
            # Right now, returning test data
            return jsonify([(song['name'], song['artists_name'], song['image']) for song in json_string["data"]])
        return jsonify({"error": "Unauthorized"}), 401
    except Exception as e:
        logger.error(f"Error in card_data endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/testdata")
def testdata():
    """Test data endpoint"""
    try:
        return jsonify([(song['name'], song['image']) for song in json_string["data"]])
    except Exception as e:
        logger.error(f"Error in testdata endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

# New endpoints for two-user functionality
@app.route("/api/user_status")
def user_status():
    """Return the login status of both users"""
    try:
        logger.debug(f"User status request - Player1: {player1.saved}, Player2: {player2.saved}")
        logger.debug(f"Player1 details: name={player1.name}, picture={player1.picture}")
        logger.debug(f"Player2 details: name={player2.name}, picture={player2.picture}")
        
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
    except Exception as e:
        logger.error(f"Error in user_status endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/api/login/<int:player_id>')
def player_login(player_id):
    """Initiate login flow for a specific player"""
    try:
        if player_id not in [1, 2]:
            return jsonify({"error": "Invalid player ID"}), 400
        
        # Get redirect path from query parameters
        redirect_path = request.args.get('redirect', 'compare')
        
        # Store player ID and redirect path in session
        session['current_player'] = player_id
        session['redirect_path'] = redirect_path
        
        logger.debug(f"Starting login flow for player {player_id} with redirect to {redirect_path}")
        return redirect('/login')
    except Exception as e:
        logger.error(f"Error in player_login endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/save_user_data")
def save_user_data():
    """Save user data after Spotify login"""
    try:
        if 'access_token' not in session:
            logger.error("No access token in session")
            return jsonify({"error": "No access token found"}), 401
        
        # Identify which player we're saving data for
        player_id = session.get('current_player', 1)
        # Get the redirect path from session
        redirect_path = session.get('redirect_path', 'compare')
        
        logger.info(f"Saving data for player {player_id} with redirect to {redirect_path}")
        
        # IMPORTANT: Store the token in our player_tokens dictionary
        player_tokens[player_id] = session['access_token']
        logger.info(f"Saved token for player {player_id}")
        
        # Fetch user data from Spotify API
        headers = {
            'Authorization': f"Bearer {session['access_token']}"
        }
        
        # Get profile first to set basic user info
        profile_response = requests.get(f"{API_BASE_URL}me", headers=headers)
        if not profile_response.ok:
            logger.error(f"Failed to get profile: {profile_response.status_code} - {profile_response.text}")
            return jsonify({"error": f"Failed to get profile: {profile_response.status_code}"}), 500
        
        profile = profile_response.json()
        
        # Get top tracks for different time ranges
        short_term_response = requests.get(f"{API_BASE_URL}me/top/tracks?time_range=short_term&limit=50", headers=headers)
        if not short_term_response.ok:
            logger.error(f"Failed to get short-term tracks: {short_term_response.status_code}")
            return jsonify({"error": f"Failed to get tracks: {short_term_response.status_code}"}), 500
        
        short_tracks_data = short_term_response.json()
        shortTracks = []
        for item in short_tracks_data.get("items", []):
            image_url = None
            if item["album"]["images"] and len(item["album"]["images"]) > 0:
                image_url = item["album"]["images"][0]["url"]
            
            shortTracks.append({
                "name": item["name"],
                "id": item["id"],
                "artists_name": item["artists"][0]["name"],
                "artists_id": item["artists"][0]["id"],
                "image": image_url
            })

        # Get medium term tracks
        medium_term_response = requests.get(f"{API_BASE_URL}me/top/tracks?time_range=medium_term&limit=50", headers=headers)
        if not medium_term_response.ok:
            logger.error(f"Failed to get medium-term tracks: {medium_term_response.status_code}")
            return jsonify({"error": f"Failed to get tracks: {medium_term_response.status_code}"}), 500
        
        medium_tracks_data = medium_term_response.json()
        medTracks = []
        for item in medium_tracks_data.get("items", []):
            image_url = None
            if item["album"]["images"] and len(item["album"]["images"]) > 0:
                image_url = item["album"]["images"][0]["url"]
            
            medTracks.append({
                "name": item["name"],
                "id": item["id"],
                "artists_name": item["artists"][0]["name"],
                "artists_id": item["artists"][0]["id"],
                "image": image_url
            })

        # Get long term tracks
        long_term_response = requests.get(f"{API_BASE_URL}me/top/tracks?time_range=long_term&limit=50", headers=headers)
        if not long_term_response.ok:
            logger.error(f"Failed to get long-term tracks: {long_term_response.status_code}")
            return jsonify({"error": f"Failed to get tracks: {long_term_response.status_code}"}), 500
        
        long_tracks_data = long_term_response.json()
        longTracks = []
        for item in long_tracks_data.get("items", []):
            image_url = None
            if item["album"]["images"] and len(item["album"]["images"]) > 0:
                image_url = item["album"]["images"][0]["url"]
            
            longTracks.append({
                "name": item["name"],
                "id": item["id"],
                "artists_name": item["artists"][0]["name"],
                "artists_id": item["artists"][0]["id"],
                "image": image_url
            })

        # Get top artists and genres
        artists_response = requests.get(f"{API_BASE_URL}me/top/artists?time_range=medium_term&limit=50", headers=headers)
        if not artists_response.ok:
            logger.error(f"Failed to get artists: {artists_response.status_code}")
            return jsonify({"error": f"Failed to get artists: {artists_response.status_code}"}), 500
        
        artists_data = artists_response.json()
        topGenres = set()  # Using a set to avoid duplicates
        topArtists = []
        for artist in artists_data.get("items", []):
            topGenres.update(artist.get("genres", []))  # Add multiple genres from each artist
            topArtists.append(artist)
        
        # Save data to appropriate player
        player = player1 if player_id == 1 else player2
        player.shortTracks = shortTracks
        player.medTracks = medTracks
        player.longTracks = longTracks
        player.topGenres = list(topGenres)
        player.topArtists = topArtists
        player.name = profile.get('display_name')
        player.picture = profile.get("images")[0]["url"] if profile.get("images") and len(profile.get("images")) > 0 else None
        player.saved = True
        
        # Generate ID lists for comparison
        player.songsS, player.artistsS = idLists(player.shortTracks)
        player.songsM, player.artistsM = idLists(player.medTracks)
        player.songsL, player.artistsL = idLists(player.longTracks)
        
        logger.info(f"Successfully saved data for player {player_id}")
        
        # Create an access token for redirecting to frontend with the redirect path
        frontend_url = os.environ.get('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f"{frontend_url}?access_token={session['access_token']}&player_id={player_id}&redirect_to={redirect_path}")
    
    except Exception as e:
        logger.exception(f"Error saving user data: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/reset/<int:player_id>")
def reset_player(player_id):
    """Reset a player's data"""
    try:
        if player_id == 1:
            player1.__init__()
            player_tokens[1] = None  # Clear the token
            logger.debug("Reset player 1")
        elif player_id == 2:
            player2.__init__()
            player_tokens[2] = None  # Clear the token
            logger.debug("Reset player 2")
        else:
            return jsonify({"error": "Invalid player ID"}), 400
        
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error in reset_player endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/reset_all")
def reset_all():
    """Reset both players' data"""
    try:
        player1.__init__()
        player2.__init__()
        player_tokens[1] = None  # Clear tokens
        player_tokens[2] = None
        logger.debug("Reset all players")
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Error in reset_all endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/comparison")
def get_comparison():
    """Get comparison results between the two users"""
    try:
        if not player1.saved or not player2.saved:
            logger.error("Attempted comparison but not all users are logged in")
            return jsonify({"error": "Both users need to be logged in"}), 400
        
        # IMPORTANT: Use player1's token for API calls since it was saved first
        # This is the critical fix for the "No access token in session" error
        if player_tokens[1]:
            auth_token = player_tokens[1]
            logger.debug("Using player 1's token for comparison")
        elif player_tokens[2]:
            auth_token = player_tokens[2]
            logger.debug("Using player 2's token for comparison")
        elif 'access_token' in session:
            auth_token = session['access_token']
            logger.debug("Using session token for comparison")
        else:
            logger.error("No access token available for comparison")
            return jsonify({"error": "Authentication required"}), 401
            
        headers = {
            'Authorization': f"Bearer {auth_token}"
        }
        
        # Check if player data is valid
        if not player1.shortTracks or not player2.shortTracks:
            logger.error("Missing short term tracks data")
            return jsonify({"error": "Missing user track data"}), 400
            
        if not player1.medTracks or not player2.medTracks:
            logger.error("Missing medium term tracks data")
            return jsonify({"error": "Missing user track data"}), 400
            
        if not player1.longTracks or not player2.longTracks:
            logger.error("Missing long term tracks data")
            return jsonify({"error": "Missing user track data"}), 400
            
        if not player1.topGenres or not player2.topGenres:
            logger.error("Missing genre data")
            return jsonify({"error": "Missing user genre data"}), 400
        
        # Ensure ID lists are generated
        if not player1.songsS or not player1.songsM or not player1.songsL:
            player1.songsS, player1.artistsS = idLists(player1.shortTracks)
            player1.songsM, player1.artistsM = idLists(player1.medTracks)
            player1.songsL, player1.artistsL = idLists(player1.longTracks)
            
        if not player2.songsS or not player2.songsM or not player2.songsL:
            player2.songsS, player2.artistsS = idLists(player2.shortTracks)
            player2.songsM, player2.artistsM = idLists(player2.medTracks)
            player2.songsL, player2.artistsL = idLists(player2.longTracks)
        
        # Compute comparisons for all time ranges
        logger.debug("Computing comparisons")
        
        resultsSHORT = produceV2results(player1.topGenres, player1.shortTracks, player2.topGenres, player2.shortTracks, headers)
        resultsMED = produceV2results(player1.topGenres, player1.medTracks, player2.topGenres, player2.medTracks, headers)
        resultsLONG = produceV2results(player1.topGenres, player1.longTracks, player2.topGenres, player2.longTracks, headers)
        
        # Merge results
        logger.debug("Comparison complete")
        
        # Return results
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
        logger.exception(f"Error in comparison: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/tracks/<int:player_id>/<string:time_range>")
def get_player_tracks(player_id, time_range):
    """Get tracks for a specific player and time range"""
    if not player_id in [1, 2]:
        return jsonify({"error": "Invalid player ID"}), 400
        
    if not time_range in ["short", "medium", "long"]:
        return jsonify({"error": "Invalid time range"}), 400
    
    try:
        # Check authentication
        token = get_token_from_header()
        if not token:
            return jsonify({"error": "Authentication required"}), 401
            
        # Access the player data from our global variables
        player = player1 if player_id == 1 else player2
        
        # Return the appropriate tracks based on time range
        if time_range == "short":
            return jsonify(player.shortTracks)
        elif time_range == "medium":
            return jsonify(player.medTracks)
        elif time_range == "long":
            return jsonify(player.longTracks)
            
    except Exception as e:
        logger.error(f"Error fetching tracks for player {player_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Modify the comparison endpoint to include full track data
@app.route("/api/comparison_with_tracks")
def get_comparison_with_tracks():
    """Get comparison results with full track data for both users"""
    try:
        if not player1.saved or not player2.saved:
            logger.error("Attempted comparison but not all users are logged in")
            return jsonify({"error": "Both users need to be logged in"}), 400
            
        # Use an available token for API calls
        if player_tokens[1]:
            auth_token = player_tokens[1]
        elif player_tokens[2]:
            auth_token = player_tokens[2]
        elif 'access_token' in session:
            auth_token = session['access_token']
        else:
            logger.error("No access token available for comparison")
            return jsonify({"error": "Authentication required"}), 401
            
        headers = {
            'Authorization': f"Bearer {auth_token}"
        }
        
        # Compute comparisons for all time ranges
        logger.debug("Computing comparisons with track data")
        
        resultsSHORT = produceV2results(player1.topGenres, player1.shortTracks, player2.topGenres, player2.shortTracks, headers)
        resultsMED = produceV2results(player1.topGenres, player1.medTracks, player2.topGenres, player2.medTracks, headers)
        resultsLONG = produceV2results(player1.topGenres, player1.longTracks, player2.topGenres, player2.longTracks, headers)
        
        # Return results with full track data
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
            "short_term": {
                **resultsSHORT,
                "tracks": {
                    "player1": player1.shortTracks,
                    "player2": player2.shortTracks
                }
            },
            "medium_term": {
                **resultsMED,
                "tracks": {
                    "player1": player1.medTracks,
                    "player2": player2.medTracks
                }
            },
            "long_term": {
                **resultsLONG,
                "tracks": {
                    "player1": player1.longTracks,
                    "player2": player2.longTracks
                }
            },
            "sharedGenres": round(pointsLog(simGenres(player1.topGenres, player2.topGenres)), 2)
        })
    
    except Exception as e:
        logger.exception(f"Error in comparison with tracks: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Add these routes to your routes.py file to display users' top tracks
@app.route("/api/user_top_tracks/<int:player_id>/<string:time_range>")
def get_user_top_tracks(player_id, time_range):
    """Get top 10 tracks for a specific player and time range"""
    if player_id not in [1, 2]:
        return jsonify({"error": "Invalid player ID"}), 400
        
    if time_range not in ["short", "medium", "long"]:
        return jsonify({"error": "Invalid time range"}), 400
    
    try:
        # Check if token exists in player_tokens dictionary
        if player_id in player_tokens and player_tokens[player_id]:
            auth_token = player_tokens[player_id]
        # Or fallback to session token if available
        elif 'access_token' in session:
            auth_token = session['access_token']
        else:
            logger.error(f"No access token available for player {player_id}")
            return jsonify({"error": "Authentication required"}), 401
            
        # Access the player data from our global variables
        player = player1 if player_id == 1 else player2
        
        if not player.saved:
            return jsonify({"error": f"Player {player_id} not logged in"}), 400
        
        # Prepare tracks with image URLs
        tracks = []
        
        # Get the appropriate tracks based on time range
        raw_tracks = None
        if time_range == "short":
            raw_tracks = player.shortTracks
        elif time_range == "medium":
            raw_tracks = player.medTracks
        elif time_range == "long":
            raw_tracks = player.longTracks
            
        # Ensure we have track data
        if not raw_tracks:
            logger.error(f"No {time_range} tracks found for player {player_id}")
            return jsonify([])
            
        # Format tracks to include all necessary info including images
        for track in raw_tracks[:10]:  # Limit to top 10
            # Get album image using Spotify API
            try:
                headers = {
                    'Authorization': f"Bearer {auth_token}"
                }
                
                # Get track details to access album cover art
                track_response = requests.get(f"{API_BASE_URL}tracks/{track['id']}", headers=headers)
                
                if track_response.status_code == 200:
                    track_data = track_response.json()
                    # Extract image URL from album
                    image_url = None
                    if 'album' in track_data and 'images' in track_data['album'] and len(track_data['album']['images']) > 0:
                        image_url = track_data['album']['images'][0]['url']
                        
                    # Create formatted track object
                    formatted_track = {
                        'name': track['name'],
                        'id': track['id'],
                        'artists_name': track['artists_name'],
                        'artists_id': track['artists_id'],
                        'image': image_url
                    }
                    
                    tracks.append(formatted_track)
                else:
                    logger.error(f"Failed to get track details: {track_response.status_code}")
                    # Still add track without image
                    tracks.append({
                        'name': track['name'],
                        'id': track['id'],
                        'artists_name': track['artists_name'],
                        'artists_id': track['artists_id'],
                        'image': None
                    })
            except Exception as e:
                logger.error(f"Error processing track {track['name']}: {str(e)}")
                # Still add track without image on error
                tracks.append({
                    'name': track['name'],
                    'id': track['id'],
                    'artists_name': track['artists_name'],
                    'artists_id': track['artists_id'],
                    'image': None
                })
                
        logger.info(f"Returning {len(tracks)} tracks for player {player_id}, time range {time_range}")
        return jsonify(tracks)
            
    except Exception as e:
        logger.error(f"Error fetching tracks for player {player_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500
    
@app.route("/api/all_user_tracks/<int:playerId>")
def get_all_user_tracks_data(playerId):
    """Get all time ranges of tracks for a user at once"""
    logger.debug(f"Request for all tracks from player {playerId}")
    
    if playerId not in [1, 2]:
        logger.error(f"Invalid player ID: {playerId}")
        return jsonify({"error": "Invalid player ID"}), 400
    
    try:
        # Get token from player_tokens or session
        token = None
        if playerId in player_tokens and player_tokens[playerId]:
            token = player_tokens[playerId]
            logger.debug(f"Using saved token for player {playerId}")
        elif 'access_token' in session:
            token = session['access_token']
            logger.debug("Using session token")
            
        if not token:
            logger.error("No authentication token found")
            return jsonify({"error": "Authentication required"}), 401
            
        # Access player data
        player = player1 if playerId == 1 else player2
        
        if not player.saved:
            logger.error(f"Player {playerId} not logged in")
            return jsonify({"error": f"Player {playerId} not logged in"}), 400
        
        # Debug player data
        logger.debug(f"Player {playerId} data: name={player.name}, saved={player.saved}")
        logger.debug(f"Short tracks count: {len(player.shortTracks) if player.shortTracks else 0}")
        logger.debug(f"Medium tracks count: {len(player.medTracks) if player.medTracks else 0}")
        logger.debug(f"Long tracks count: {len(player.longTracks) if player.longTracks else 0}")
            
        # Build response without images for simplicity
        formatted_tracks = {
            "short": player.shortTracks[:10] if player.shortTracks else [],
            "medium": player.medTracks[:10] if player.medTracks else [],
            "long": player.longTracks[:10] if player.longTracks else []
        }
        
        logger.debug(f"Returning formatted tracks for player {playerId}")    
        return jsonify(formatted_tracks)
        
    except Exception as e:
        logger.exception(f"Error fetching all tracks for player {playerId}: {str(e)}")
        return jsonify({"error": str(e)}), 500
        # Helper function to format tracks
        def format_tracks_with_images(raw_tracks):
            result = []
            for track in raw_tracks[:10]:  # Limit to top 10
                try:
                    headers = {'Authorization': f"Bearer {token}"}
                    track_response = requests.get(f"{API_BASE_URL}tracks/{track['id']}", headers=headers)
                    
                    if track_response.status_code == 200:
                        track_data = track_response.json()
                        # Extract image URL
                        image_url = None
                        if 'album' in track_data and 'images' in track_data['album'] and len(track_data['album']['images']) > 0:
                            image_url = track_data['album']['images'][0]['url']
                            
                        # Add formatted track
                        result.append({
                            'name': track['name'],
                            'id': track['id'],
                            'artists_name': track['artists_name'],
                            'artists_id': track['artists_id'],
                            'image': image_url
                        })
                    else:
                        # Add track without image
                        result.append({
                            'name': track['name'],
                            'id': track['id'],
                            'artists_name': track['artists_name'],
                            'artists_id': track['artists_id'],
                            'image': None
                        })
                except Exception as e:
                    logger.error(f"Error processing track {track['name']}: {str(e)}")
                    # Still add track on error
                    result.append({
                        'name': track['name'],
                        'id': track['id'],
                        'artists_name': track['artists_name'],
                        'artists_id': track['artists_id'],
                        'image': None
                    })
            return result
        
        # Format tracks for each time range
        if player.shortTracks:
            formatted_tracks["short"] = format_tracks_with_images(player.shortTracks)
            
        if player.medTracks:
            formatted_tracks["medium"] = format_tracks_with_images(player.medTracks)
            
        if player.longTracks:
            formatted_tracks["long"] = format_tracks_with_images(player.longTracks)
            
        return jsonify(formatted_tracks)
        
    except Exception as e:
        logger.error(f"Error fetching all tracks for player {player_id}: {str(e)}")
        return jsonify({"error": str(e)}), 500