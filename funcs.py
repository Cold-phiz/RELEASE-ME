# 
# Spotify + YouTube Downloader
#
# 15/10/24
# Coldphiz (c)
#

import os
import logging
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from yt_dlp import YoutubeDL
from concurrent.futures import ThreadPoolExecutor
import eyed3

key = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='09c13e8f02cb44889677444f98abcf2a', client_secret='fa31523465de4d2590950e3172c9748f'))

# Helper to sanitize filenames
def sanitize_filename(name):
    return name.translate(str.maketrans('', '', '/\\?%*:|"<>')).strip()[:100]

# Download album cover
def download_album_cover(url, path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(path, 'wb') as f:
            f.write(response.content)
    except Exception as e:
        print(f"Error downloading album cover: {e}")

# Download song
def download_song(url, path):
    track_info = key.track(url)
    track_name = sanitize_filename(track_info['name'])
    album_name = sanitize_filename(track_info['album']['name'])
    dest_file = os.path.join(path, f"{track_name}.mp3")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '320'}],
        'outtmpl': dest_file.replace('.mp3', '.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'logger': logging.getLogger('yt-dlp')
    }

    logging.getLogger('yt-dlp').setLevel(logging.ERROR)

    try:
        with YoutubeDL(ydl_opts) as ydl:
            search_query = f"{track_name} {track_info['artists'][0]['name']} audio"
            ydl.download([f"ytsearch:{search_query}"])

        # Fallback if downloaded as .m4a
        if not os.path.exists(dest_file):
            dest_file = dest_file.replace('.mp3', '.m4a')

        # Set metadata
        audio = eyed3.load(dest_file)
        audio.initTag()
        audio.tag.title = track_name
        audio.tag.album = album_name
        audio.tag.images.set(3, open(os.path.join(path, "album_cover.jpg"), 'rb').read(), 'image/jpeg')
        audio.tag.save(version=eyed3.id3.ID3_V2_3)

    except Exception as e:
        print(f"Error downloading {track_name}: {e}")

# Download album
def download_album(url):
    album_info = key.album(url)
    album_name = album_info['name']
    artist_name = album_info['artists'][0]['name']
    
    # Sanitize names to make them filesystem-safe
    sanitized_album_name = sanitize_filename(album_name)
    sanitized_artist_name = sanitize_filename(artist_name)
    
    # Define album path in the new structure
    album_path = os.path.join("./static/db/artists", sanitized_artist_name, sanitized_album_name)

    if os.path.exists(album_path):
        print(f"Album '{album_name}' by '{artist_name}' already exists in '{album_path}'. Skipping download.")
        return

    os.makedirs(album_path, exist_ok=True)

    # Download album cover
    album_cover_url = album_info['images'][0]['url'] if album_info['images'] else None
    if album_cover_url:
        album_cover_path = os.path.join(album_path, "album_cover.jpg")
        download_album_cover(album_cover_url, album_cover_path)

    # Download each track in the album
    tracks = album_info['tracks']['items']
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(download_song, track['external_urls']['spotify'], album_path) for track in tracks]
        for future in futures:
            try:
                future.result()
            except Exception as e:
                print(f"Error downloading song: {e}")

    print(f"Album '{album_name}' by '{artist_name}' downloaded successfully.")

# Download playlist
def download_playlist(url):
    playlist_info = key.playlist(url)
    playlist_name = playlist_info['name']
    sanitized_playlist_name = sanitize_filename(playlist_name)
    playlist_folder = os.path.join("./static/db/playlists", sanitized_playlist_name)

    # Create the playlist directory
    os.makedirs(playlist_folder, exist_ok=True)

    # Download playlist cover if available
    if playlist_info['images']:
        playlist_cover_url = playlist_info['images'][0]['url']
        cover_path = os.path.join(playlist_folder, "cover.jpg")
        download_album_cover(playlist_cover_url, cover_path)

    # File to store paths to songs in the playlist
    song_paths_file = os.path.join(playlist_folder, "song_paths.txt")

    # Retrieve all tracks in the playlist, handling pagination
    limit = 100
    offset = 0
    total_tracks = playlist_info['tracks']['total']
    tracks = []

    while offset < total_tracks:
        response = key.playlist_tracks(url, limit=limit, offset=offset)
        tracks.extend(response['items'])
        offset += limit

    # Use a set to track downloaded albums
    processed_albums = set()

    # Process and download albums from the playlist
    for item in tracks:
        track = item['track']
        album_name = track['album']['name']
        album_id = track['album']['id']
        artist_name = track['album']['artists'][0]['name']

        # Create a unique key for the album to prevent duplicates
        album_key = (album_name, artist_name)

        if album_key not in processed_albums:
            processed_albums.add(album_key)  # Mark this album as processed

            album_url = f"https://open.spotify.com/album/{album_id}"
            print(f"Downloading album: {album_name} by {artist_name}")
            download_album(album_url)  # Download the album

    # Write song paths to file
    with open(song_paths_file, 'w') as f:
        for item in tracks:
            track = item['track']
            song_name = track['name']
            album_name = track['album']['name']
            artist_name = track['album']['artists'][0]['name']

            # Construct the song file path based on the album and artist
            song_file_path = os.path.join("./static/db/artists", sanitize_filename(artist_name), sanitize_filename(album_name), f"{sanitize_filename(song_name)}.mp3")

            # Check if the song file exists before writing
            if os.path.exists(song_file_path):
                f.write(song_file_path + "\n")

    print(f"Playlist '{playlist_name}' downloaded successfully with song paths saved in '{song_paths_file}'.")
