import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = 'YOUR_SPOTIFY_CLIENT_ID'
client_secret = 'YOUR_SPOTIFY_CLIENT_SECRET'
redirect_uri = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

def list_artist_tracks(artist_url):
    try:
        artist_id = artist_url.split('/')[-1].split('?')[0]
        albums = sp.artist_albums(artist_id, album_type='album', limit=50)['items']
        singles = sp.artist_albums(artist_id, album_type='single', limit=50)['items']
        compilations = sp.artist_albums(artist_id, album_type='compilation', limit=50)['items']
        appears_on = sp.artist_albums(artist_id, album_type='appears_on', limit=50)['items']
        
        all_releases = albums + singles + compilations + appears_on
        unique_releases = {album['id']: album for album in all_releases}.values()
        
        for release in unique_releases:
            if artist_id not in [artist['id'] for artist in release['artists']]:
                continue
            
            release_name = release['name']
            release_date = release['release_date']
            release_type = release['album_type']
            release_id = release['id']
            
            print(f"{release_type.capitalize()}: {release_name} (Release Date: {release_date})")
            
            if release_type == 'album':
                tracks = sp.album_tracks(release_id)['items']
                for idx, track in enumerate(tracks):
                    print(f"  {idx + 1}. {track['name']}")
    
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

while True:
    artist_url = input("Please enter the Spotify artist URL (or type 'exit' to quit): ")
    if artist_url.lower() == 'exit':
        break
    list_artist_tracks(artist_url)
