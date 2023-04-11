from pathlib import Path
import json
from typing import List
import time

import spotipy

from credentials import get_auth_manager
from classes.DetailedSong import DetailedSong

DATA_PATH = Path(__file__).parent.parent / "MyData"


def Spotify() -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=get_auth_manager())


def get_uris(filename: str) -> List[str]:
    with open(DATA_PATH / filename, "r") as f:
        data = json.load(f)
    return [song["spotify_track_uri"] for song in data if song["spotify_track_uri"]]


def create_song_map() -> None:
    sp = Spotify()
    uris = get_uris("endsong_0.json")
    for i in range(0, len(uris), 50):
        request_uris = ",".join(uris[i : i + 50])
        tracks_response = sp.tracks(request_uris)

        metadata = {
            track["uri"]: {
                "name": track["name"],
                "artists": [artist["name"] for artist in track["artists"]],
                "album": track["album"]["name"],
                "explicit": track["explicit"],
                "genres": track["album"]["genres"],
                "popularity": track["popularity"],
            }
            for track in tracks_response["tracks"]
        }

        songs = [
            DetailedSong(uri=key, name=metadata[key]["name"]) for key in metadata.keys()
        ]

        audio_features_response = sp.audio_features(request_uris)
        audio_features = {
            track["uri"]: {
                "acousticness": track["acousticness"],
                "danceability": track["danceability"],
                "energy": track["energy"],
                "instrumentalness": track["instrumentalness"],
                "liveness": track["liveness"],
                "loudness": track["loudness"],
                "speechiness": track["speechiness"],
                "tempo": track["tempo"],
                "valence": track["valence"],
                "time_signature": track["time_signature"],
                "tempo": track["tempo"],
                "mode": track["mode"],
                "key": track["key"],
            }
            for track in audio_features_response["audio_features"]
        }

        for song in enumerate(songs):
            song.set_metadata(metadata[song["uri"]])
            song.set_audio_features(audio_features[song["uri"]])
