from typing import List
import json
from pathlib import Path
import os

import spotipy

from credentials import get_auth_manager
from classes.Song import Song


def Spotify() -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=get_auth_manager())


def get_songs_from_playlists(playlists: List[str]) -> List[str]:
    sp = Spotify()

    songs = set()
    for playlist in playlists:
        response = sp.playlist(playlist)
        tracks = response["tracks"]["items"]
        for song in tracks:
            songs.add(Song(song["track"]["uri"], song["track"]["name"], playlist))
    return songs


def store_song_map(songs: List[Song], filename: str = "current_map.txt") -> None:
    songs_json = {song.uri: song.to_json() for song in songs}

    if not os.path.exists("data"):
        os.mkdir("data")
    filepath = Path(__file__).parent.parent / "data" / filename

    json.dump(songs_json, open(filepath, "w"), indent=4)


if __name__ == "__main__":
    # Current, Nov2022, Apr 2022
    playlists = [
        "spotify:playlist:6ahMVr9euPcvtxVtoDJ1Qf",
        "spotify:playlist:07Qc58sqqLtoM1It1QX7fE",
        "spotify:playlist:5ifdmqV6vTsIEAckZB4Ccy",
    ]
    songs = get_songs_from_playlists(playlists)
    store_song_map(songs)
