from pathlib import Path
import json
from typing import Set

PATH = Path(__file__).parent.parent / "MyData"


def _valid(track: dict) -> bool:
    """Determine if a track is valid

    Args:
        track (dict): The track to check

    Returns:
        bool: Whether or not the track is valid
    """
    return (
        track["spotify_track_uri"]
        and track["ms_played"] > 29999
        and track["master_metadata_track_name"] != None
    )


def read_endsong(filename: str) -> Set[str]:
    """Parse through all data in an endsong and return the track URIs

    Args:
        filename (str): The endsong file to parse

    Returns:
        Set[str]: A set of track URIs
    """
    with open(PATH / filename, "r") as f:
        data = json.load(f)

    songs = set()
    for track in data:
        if _valid(track):
            songs.add(track["spotify_track_uri"])

    return songs


def read_endsongs() -> Set[str]:
    """Parse through all endsong files and return the track URIs

    Returns:
        Set[str]: A set of track URIs
    """
    songs = set()
    for filename in PATH.glob("endsong*.json"):
        songs.update(read_endsong(filename))

    return songs


def write_songs(songs: Set[str]) -> None:
    """Write the set of songs to a file

    Args:
        songs (Set[str]): The set of songs to write
    """
    with open(PATH / "song_set.json", "w") as f:
        json.dump(list(songs), f)


if __name__ == "__main__":
    songs = read_endsongs()
    write_songs(songs)
