from flask import Flask, request, redirect, url_for, session, render_template_string, send_file
import requests
import pandas as pd
import io

app = Flask(__name__)
app.secret_key = 'XXXXX'  # You can generate your own secret key
CLIENT_ID = 'XXXXXXXXXX'  # From the spotify dev app
CLIENT_SECRET = 'XXXXXXXX'  # From the spotify dev app
REDIRECT_URI = 'http://localhost:5000/callback'  # Make sure this is your callback
SCOPE = 'playlist-read-private'

# HTML template
HTML_TEMPLATE = """
<!doctype html>
<html>
    <head>
        <title>Spotify Playlist Backup</title>
        <link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='styles.css') }}">
    </head>
    <body>
        <div class="content">
            <div class="title">
                <h1>Backup Your Spotify Playlists</h1>
            </div>
            <div class="button-container">
                {% if 'access_token' in session %}
                    <form method="POST" action="{{ url_for('backup_playlist') }}">
                        <input type="text" name="playlist_id" placeholder="Enter Playlist ID" class="text-input">
                        <input type="submit" value="Backup Playlist" class="button">
                    </form>
                    <form method="POST" action="{{ url_for('backup_all') }}">
                        <input type="submit" value="Backup All Playlists" class="button">
                    </form>
                {% else %}
                    <a href="{{ url_for('login') }}"><button class="button">Login with Spotify</button></a>
                {% endif %}
            </div>
        </div>
    </body>
</html>
"""

def fetch_playlists(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.spotify.com/v1/me/playlists", headers=headers)
    response.raise_for_status()
    return response.json()

def fetch_playlist_tracks(playlist_id, access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", headers=headers)
    response.raise_for_status()
    playlist_data = response.json()
    tracks = playlist_data['items']
    track_details = []
    
    for track in tracks:
        if track['track'] is not None:  # Ensure track is not None
            track_details.append({
                'Track Name': track['track']['name'],
                'Artists': ', '.join([artist['name'] for artist in track['track']['artists']]),
                'Album': track['track']['album']['name']
            })
    return track_details

@app.route('/')
def index():
    if 'access_token' in session:
        return render_template_string(HTML_TEMPLATE)
    return render_template_string(HTML_TEMPLATE)

@app.route('/login')
def login():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope={SCOPE}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = "https://accounts.spotify.com/api/token"
    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    token_headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(token_url, data=token_data, headers=token_headers)
    response.raise_for_status()
    tokens = response.json()
    session['access_token'] = tokens['access_token']
    return redirect(url_for('index'))

@app.route('/backup_playlist', methods=['POST'])
def backup_playlist():
    if 'access_token' not in session:
        return redirect(url_for('index'))
    
    access_token = session['access_token']
    playlist_id = request.form['playlist_id']
    tracks = fetch_playlist_tracks(playlist_id, access_token)
    
    df = pd.DataFrame(tracks)
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_buffer.seek(0)
    
    return send_file(csv_buffer, as_attachment=True, download_name=f'playlist_{playlist_id}.csv', mimetype='text/csv')

@app.route('/backup_all', methods=['POST'])
def backup_all():
    if 'access_token' not in session:
        return redirect(url_for('index'))
    
    access_token = session['access_token']
    playlists = fetch_playlists(access_token)['items']
    all_tracks = []

    for playlist in playlists:
        tracks = fetch_playlist_tracks(playlist['id'], access_token)
        all_tracks.extend(tracks)
    
    df = pd.DataFrame(all_tracks)
    csv_buffer = io.BytesIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8')
    csv_buffer.seek(0)
    
    return send_file(csv_buffer, as_attachment=True, download_name='all_playlists.csv', mimetype='text/csv')

if __name__ == '__main__':
    app.run(debug=True)