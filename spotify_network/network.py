import os
import datetime
import json
import argparse

import networkx as nx

from parse import parse_all_files
from analysis import analyze_network


def create_network(folder: str = "MyData"):
    path = f"{os.getcwd()}/{folder}"
    lookup_path = f"{os.getcwd()}/{folder}/song_map.json"

    lookup = json.load(open(lookup_path, "r"))

    all_songs = parse_all_files(path)
    G = nx.Graph()
    for i, current in enumerate(all_songs):
        if i == len(all_songs) - 1:
            break

        # Ignore songs that are played for less than 30 seconds
        if current["ms_played"] < 30000:
            continue

        following = all_songs[i + 1]

        G.add_node(
            current["track"],
            id=current["spotify_track_uri"],
            artist=current["artist"],
            album=current["album"],
            liked=current["liked"],
            current=current["current"],
            popularity=lookup[current["spotify_track_uri"]]["popularity"],
            acousticness=int(
                lookup[current["spotify_track_uri"]]["acousticness"] * 100
            ),
            danceability=int(
                lookup[current["spotify_track_uri"]]["danceability"] * 100
            ),
            energy=int(lookup[current["spotify_track_uri"]]["energy"] * 100),
            instrumentalness=int(
                lookup[current["spotify_track_uri"]]["instrumentalness"] * 100
            ),
            liveness=int(lookup[current["spotify_track_uri"]]["liveness"] * 100),
            loudness=int(lookup[current["spotify_track_uri"]]["loudness"] * 100),
            speechiness=int(lookup[current["spotify_track_uri"]]["speechiness"] * 100),
            tempo=int(lookup[current["spotify_track_uri"]]["tempo"]),
            valence=int(lookup[current["spotify_track_uri"]]["valence"] * 100),
            time_signature=lookup[current["spotify_track_uri"]]["time_signature"],
            mode=lookup[current["spotify_track_uri"]]["mode"],
            key=lookup[current["spotify_track_uri"]]["key"],
            played=1,
        )

        G.add_node(
            following["track"],
            id=following["spotify_track_uri"],
            artist=following["artist"],
            album=following["album"],
            liked=following["liked"],
            current=following["current"],
            popularity=lookup[current["spotify_track_uri"]]["popularity"],
            acousticness=int(
                lookup[current["spotify_track_uri"]]["acousticness"] * 100
            ),
            danceability=int(
                lookup[current["spotify_track_uri"]]["danceability"] * 100
            ),
            energy=int(lookup[current["spotify_track_uri"]]["energy"] * 100),
            instrumentalness=int(
                lookup[current["spotify_track_uri"]]["instrumentalness"] * 100
            ),
            liveness=int(lookup[current["spotify_track_uri"]]["liveness"] * 100),
            loudness=int(lookup[current["spotify_track_uri"]]["loudness"] * 100),
            speechiness=int(lookup[current["spotify_track_uri"]]["speechiness"] * 100),
            tempo=int(lookup[current["spotify_track_uri"]]["tempo"]),
            valence=int(lookup[current["spotify_track_uri"]]["valence"] * 100),
            time_signature=lookup[current["spotify_track_uri"]]["time_signature"],
            mode=lookup[current["spotify_track_uri"]]["mode"],
            key=lookup[current["spotify_track_uri"]]["key"],
            played=0,
        )

        if G.has_edge(current["track"], following["track"]):
            G[current["track"]][following["track"]]["weight"] += 1
        else:
            # Only add edge if the next song is played within 1 hour. An edge is added if the next song is played in the same session
            if following["datetime"] - current["datetime"] > datetime.timedelta(
                hours=1
            ):
                continue

            if following["reason_start"] not in ["trackdone", "fwdbtn"]:
                continue

            G.add_edge(
                current["track"],
                following["track"],
                weight=1,
            )
    return G


def write_network(G: nx.Graph, filename: str = "spotify_network"):
    nx.write_gexf(G, f"{filename}.gexf")


def get_options():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filename",
        type=str,
        default="spotify_network",
        help="Filename to save network to",
    )
    return parser.parse_args()


if __name__ == "__main__":
    options = get_options()
    G = create_network()
    write_network(G, options.filename)
