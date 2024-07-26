import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = 'CLIENT_ID'
client_secret = 'CLIENT_SECRET'
redirect_uri = 'http://localhost:8888/callback'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri))

def get_all_items(func, *args, **kwargs):
    results = []
    limit = kwargs.get('limit', 20)
    offset = 0
    while True:
        response = func(*args, limit=limit, offset=offset, **kwargs)
        results.extend(response['items'])
        if len(response['items']) < limit:
            break
        offset += limit
    return results

def list_artist_tracks(artist_url):
    try:
        artist_id = artist_url.split('/')[-1].split('?')[0]

        albums = get_all_items(sp.artist_albums, artist_id, album_type='album')
        singles = get_all_items(sp.artist_albums, artist_id, album_type='single')
        compilations = get_all_items(sp.artist_albums, artist_id, album_type='compilation')
        appears_on = get_all_items(sp.artist_albums, artist_id, album_type='appears_on')

        album_count = len(albums)
        single_count = len(singles)
        compilation_count = len(compilations)
        appears_on_count = len(appears_on)

        print("Albums:")
        for album in albums:
            print(f"  {album['name']} (Release Date: {album['release_date']})")
            tracks = get_all_items(sp.album_tracks, album['id'])
            for idx, track in enumerate(tracks):
                print(f"    {idx + 1}. {track['name']}")

        print("Singles:")
        for single in singles:
            print(f"  {single['name']} (Release Date: {single['release_date']})")

        print("Compilations:")
        for compilation in compilations:
            print(f"  {compilation['name']} (Release Date: {compilation['release_date']})")

        print("Appears On:")
        for appearance in appears_on:
            print(f"  {appearance['name']} (Release Date: {appearance['release_date']})")

        print(f"\nTotal Albums: {album_count}")
        print(f"Total Singles: {single_count}")
        print(f"Total Compilations: {compilation_count}")
        print(f"Total Appearances: {appears_on_count}")

    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

while True:
    artist_url = input("Please enter the Spotify artist URL :")
    if artist_url.lower() == 'exit':
        break
    list_artist_tracks(artist_url)
