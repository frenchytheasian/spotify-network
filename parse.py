import json
import os
import re
import datetime
from typing import List


def parse_endsong(filename: str) -> List[dict]:
    """Given a filename, return the processed song data

    Args:
        filename (str): Name of the file to parse

    Returns:
        List[dict]: JSON data from the file
    """
    with open(filename, "r") as f:
        data = json.load(f)

    new_data = []
    for song in data:
        if song["master_metadata_track_name"] == None:
            continue

        # Change timestamp to datetime object to make comparison easier
        song["date"] = datetime.datetime.strptime(song["ts"], "%Y-%m-%dT%H:%M:%SZ")

        # Rename keys
        song["track"] = song.pop("master_metadata_track_name")
        song["artist"] = song.pop("master_metadata_album_artist_name")
        song["album"] = song.pop("master_metadata_album_album_name")

        new_data.append(song)

    return new_data


def parse_all_files(folder: str) -> List[dict]:
    """Given a folder name, iterate through all files and return the processed song data

    Args:
        folder (str): name of a folder containg .json files with song data

    Returns:
        List[dict]: JSON data from all files in the folder
    """
    all_songs = []
    for filename in os.listdir(folder):
        if re.match(r"^(endsong).*\.(json)$", filename):
            all_songs.extend(parse_endsong(os.path.join(folder, filename)))

    return sorted(all_songs, key=lambda k: k["ts"])


def export(data: List[dict]) -> None:
    """Export song data into a new JSON file

    Args:
        data (List): List of song data
    """
    for song in data:
        song.pop("date")

    with open("export.json", "w") as f:
        json.dump(data, f, indent=4)
