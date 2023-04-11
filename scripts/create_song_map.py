from pathlib import Path
import json
from typing import List, Set
import time

import spotipy

from credentials import get_auth_manager
from classes.DetailedSong import DetailedSong

DATA_PATH = Path(__file__).parent.parent / "MyData"


def Spotify() -> spotipy.Spotify:
    return spotipy.Spotify(auth_manager=get_auth_manager())


def _get_ids(filename: str) -> List[str]:
    """Parse through all data in an endsong and return the track URIs

    Args:
        filename (str): The endsong file to parse

    Returns:
        List[str]: A list of track URIs
    """
    with open(DATA_PATH / filename, "r") as f:
        data = json.load(f)
    return [
        song["spotify_track_uri"].split(":")[2]
        for song in data
        if song["spotify_track_uri"]
    ]


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


def _create_song_set() -> Set[DetailedSong]:
    """Create a set of DetailedSong objects from the endsong data.

    Returns:
        Set[DetailedSong]: A set of DetailedSong objects
    """

    ids = _get_ids("endsong_0.json")

    songs = set()
    for i in range(0, len(ids), 50):
        try:
            request_uris = ids[i : i + 50]
        except IndexError:
            request_uris = ids[i:]

        metadata = _get_tracks(request_uris)
        audio_features = _get_audio_features(request_uris)

        for uri, item in metadata.items():
            song = _construct_detailed_song(uri, item, audio_features[uri])
            songs.add(song)

        print(f"Processed {i + 50}/{len(ids)} songs")
        time.sleep(4.0)  # Rate limit the requests to the spotify API
    return songs


def _get_song_map() -> Set[DetailedSong]:
    """Retrieve the song map from the song_map.txt file.

    Returns:
        Set[DetailedSong]: A set of DetailedSong objects
    """
    song_map = set()
    filepath = DATA_PATH / "song_map.txt"
    if filepath.exists():
        songs_json = json.load(open(filepath, "r"))
        for uri, song in songs_json.items():
            detailed_song = DetailedSong(uri, song["name"])
            song_map.add(detailed_song.from_json(song))
    return song_map


def append_song_map(songs: Set[DetailedSong], filename: str = "song_map.txt") -> None:
    """Append a set of DetailedSong objects to the song map.

    Args:
        songs (Set[DetailedSong]): The set of DetailedSong objects to append
        filename (str, optional): The filename to append to. Defaults to "song_map.txt".
    """
    songs_json = {song.uri: song.to_json() for song in songs}

    filepath = DATA_PATH / filename

    json.dump(songs_json, open(filepath, "a"), indent=4)


def main():
    songs = _create_song_set()
    append_song_map(songs)


if __name__ == "__main__":
    main()
