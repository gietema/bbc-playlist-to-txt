import os

import click
import spotipy
from dotenv import load_dotenv
from Levenshtein import distance
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials and settings
load_dotenv()

# Scope required for creating and modifying playlists
scope = 'playlist-modify-public'
username = os.getenv('USERNAME')


@click.command()
@click.option("--playlist", type=click.STRING, help="Name of the playlist file")
@click.option("--playlist-name", type=click.STRING, help="Name of the playlist to be created")
def main(playlist: str, playlist_name: str):
    # Authenticating with Spotify
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                                                client_secret=os.getenv('CLIENT_SECRET'),
                                                redirect_uri=os.getenv('REDIRECT_URI'),
                                                scope=scope,
                                                username=username))

    # Reading the .txt file
    with open(playlist, 'r') as file:
        song_names = [line.strip() for line in file]

    # Searching for songs and collecting URIs
    track_uris = []
    artists = []
    for song in song_names:
        result = sp.search(q=song, limit=5)
        tracks = result['tracks']['items']
        if tracks:
            name = tracks[0]['name']
            artist = tracks[0]['artists'][0]['name']
            # only add if the song name and artist name match
            name = name.split("-")[0].strip()
            original_title = song.split("-")[1].strip().lower()
            original_artist = song.split("-")[0].strip().lower()
            # check if there is some sort of match, levenstein distance maybe
            if not match(name, original_title) or not match(artist, original_artist):
                print(f"Couldn't find {original_title} by {original_artist}")
                continue
            track_uris.append(tracks[0]['uri'])
            artists.append(artist)

    # Creating a new playlist
    playlist = sp.user_playlist_create(user=username, name=playlist_name, public=True,
                                       description="Songs by " + ", ".join(artists))
    playlist_id = playlist['id']

    # Adding songs to the playlist
    if track_uris:
        sp.user_playlist_add_tracks(user=username, playlist_id=playlist_id, tracks=track_uris)

    print("Playlist created and tracks added successfully!")


def match(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()

    # remove any special characters
    # remove feat
    if "feat" in str1:
        str1 = str1.split("(feat")[0].strip()
    if "feat" in str2:
        str2 = str2.split("(feat")[0].strip()
    if "(live" in str1:
        str1 = str1.split("(live")[0].strip()
    if "(live" in str2:
        str2 = str2.split("(live")[0].strip()
    if "&" in str1:
        str1 = str1.replace("&", "and")
    if "&" in str2:
        str2 = str2.replace("&", "and")

    str1 = ''.join(e for e in str1 if e.isalnum())
    str2 = ''.join(e for e in str2 if e.isalnum())

    if str1 == str2:
        return True
    elif str1 in str2 or str2 in str1:
        return True
    else:
        # check levenstein distance to account for small typos
        if distance(str1, str2) <= 3:
            return True
        else:
            return False
        

if __name__ == '__main__':
    main()
