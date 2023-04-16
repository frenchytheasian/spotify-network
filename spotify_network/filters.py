import datetime
from pathlib import Path
import json
from enum import Enum

class Playlist(Enum):
    CURRENT = "spotify:playlist:6ahMVr9euPcvtxVtoDJ1Qf"
    NOV2022 = "spotify:playlist:07Qc58sqqLtoM1It1QX7fE"
    APR2022 = "spotify:playlist:5ifdmqV6vTsIEAckZB4Ccy"

def filter_date(song: dict) -> bool:
    early = datetime.datetime(year=2019, month=8, day=1)
    if song["datetime"] < early:
        return True
    late = datetime.datetime(year=2030, month=8, day=1)
    if song["datetime"] > late:
        return True
    
def is_liked(song: dict) -> bool:
    """Determine if a song is in the user's liked songs

    Args:
        song (dict): Spotify song

    Returns:
        bool: Whether or not the song is liked
    """
    data_path = Path(__file__).parent.parent / "data"
    liked_map = json.load(open(data_path / "liked_map.txt", "r"))
    return song["spotify_track_uri"] in liked_map

def get_current(song: dict) -> str:
    data_path = Path(__file__).parent.parent / "data"
    current_map = json.load(open(data_path / "current_map.txt", "r"))
    if song["spotify_track_uri"] in current_map:
        return Playlist(current_map[song["spotify_track_uri"]]["playlist"]).name
    else:
        return "None"