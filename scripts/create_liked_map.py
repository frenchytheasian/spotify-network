from typing import List
import json
from pathlib import Path

import spotipy

from credentials import get_oauth_manager

def Spotify() -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=get_oauth_manager())

def get_liked_songs() -> List[dict]:
    sp = Spotify()
    results = sp.current_user_saved_tracks(limit=50)
    songs = results['items']
    while results['next']:
        results = sp.next(results)
        songs.extend(results['items'])
    return songs

def create_liked_map(songs: List[dict], filename: str = 'liked_map.txt') -> None:
    song_map = {song['track']['uri']: song['track']['name'] for song in songs}
    filepath = Path(__file__).parent.parent / filename
    json.dump(song_map, open(filepath, 'w'), indent=4)

if __name__ == "__main__":
    songs = get_liked_songs()
    create_liked_map(songs)