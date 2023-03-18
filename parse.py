import json
import os
import re
import datetime
from typing import List


def parse_endsong(filename: str):
    with open(filename, "r") as f:
        data = json.load(f)

    new_data = []
    for song in enumerate(data):
        if song["master_metadata_track_name"] == None:
            continue

        # Change timestamp to datetime object to make comparison easier
        song["ts"] = datetime.datetime.strptime(song["ts"], "%Y-%m-%dT%H:%M:%SZ")

        # Rename keys
        song["track"] = song.pop("master_metadata_track_name")
        song["artist"] = song.pop("master_metadata_artist_name")
        song["album"] = song.pop("master_metadata_album_name")
        new_data.append(song)

    return data


def parse_all_files(folder: str):
    all_songs = []
    for filename in os.listdir(folder):
        if re.match(r"^(endsong).*\.(json)$", filename):
            all_songs.extend(parse_endsong(os.path.join(folder, filename)))

    return sorted(all_songs, key=lambda k: k["ts"])


def export(data: List):
    for song in data:
        song["ts"] = datetime.datetime.strftime(song["ts"], "%Y-%m-%dT%H:%M:%SZ")

    with open("export.json", "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    songs = parse_all_files("MyData")
    export(songs)
