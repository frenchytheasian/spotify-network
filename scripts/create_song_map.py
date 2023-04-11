from pathlib import Path
import json
from typing import List
import time
import os

import spotipy

from credentials import get_auth_manager
from classes.DetailedSong import DetailedSong

DATA_PATH = Path(__file__).parent.parent / "MyData"


def Spotify() -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=get_auth_manager())


def _get_ids(filename: str = "song_set.json") -> List[str]:
    """Parse through all data in an endsong and return the track URIs

    Args:
        filename (str): The endsong file to parse

    Returns:
        List[str]: A list of track URIs
    """
    with open(DATA_PATH / filename, "r") as f:
        data = json.load(f)
    return data


def _get_tracks(request_uris: str) -> dict:
    """Retrieve track info given a list of track URIs.

    Args:
        request_uris (str): A comma-separated list of track URIs.

    Returns:
        dict: The track info that we are interested in.
    """
    sp = Spotify()
    tracks_response = sp.tracks(request_uris)
    metadata = {
        track["uri"]: {
            "name": track["name"],
            "artists": [artist["name"] for artist in track["artists"]],
            "album": track["album"]["name"],
            "explicit": track["explicit"],
            "genres": track["album"].get("genres", []),
            "popularity": track["popularity"],
        }
        for track in tracks_response["tracks"]
    }

    return metadata


def _get_audio_features(request_uris: str) -> dict:
    """Retrieve audio features for a list of tracks.

    Args:
        request_uris (str): A comma-separated list of track URIs.

    Returns:
        dict: The audio features for each track.
    """
    sp = Spotify()
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
        for track in audio_features_response
    }
    return audio_features


def _construct_detailed_song(
    uri: str, metadata: dict, audio_features: dict
) -> DetailedSong:
    """Construct a DetailedSong object from the metadata and audio features.

    Args:
        uri (str): The track URI
        metadata (dict): The track metadata
        audio_features (dict): The track audio features

    Returns:
        DetailedSong: The DetailedSong object
    """
    song = DetailedSong(uri, metadata["name"])
    song.set_metadata(metadata)
    song.set_audio_features(audio_features)
    return song


def _get_state() -> int:
    if not os.path.exists("state.txt"):
        return 0
    with open("state.txt", "r") as f:
        return int(f.read())


def create_song_map() -> None:
    """Create a set of DetailedSong objects from the endsong data.

    Returns:
        Set[DetailedSong]: A set of DetailedSong objects
    """

    ids = _get_ids()

    for i in range(_get_state(), len(ids), 50):
        try:
            request_uris = ids[i : i + 50]
        except IndexError:
            request_uris = ids[i:]

        metadata = _get_tracks(request_uris)
        audio_features = _get_audio_features(request_uris)

        songs = []
        for uri, item in metadata.items():
            song = _construct_detailed_song(uri, item, audio_features[uri])
            songs.append(song)

        append_to_map(songs)

        with open("state.txt", "w") as f:
            f.write(str(i + 50))
        print(f"Processed {i + 50}/{len(ids)} songs")
        time.sleep(4.0)  # Rate limit the requests to the spotify API


def append_to_map(songs: List[DetailedSong], filename: str = "song_map.json") -> None:
    """Append a set of DetailedSong objects to the song map.

    Args:
        songs (Set[DetailedSong]): The set of DetailedSong objects to append
        filename (str, optional): The filename to append to. Defaults to "song_map.txt".
    """
    songs_json = {song.uri: song.to_json() for song in songs}

    filepath = DATA_PATH / filename

    data = {}
    if filepath.exists():
        with open(filepath, "r") as f:
            data = json.load(f)
        data.update(songs_json)
    else:
        data = songs_json

    json.dump(data, open(filepath, "w"))


if __name__ == "__main__":
    create_song_map()
