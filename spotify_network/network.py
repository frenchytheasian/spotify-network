import os
import datetime

import networkx as nx

from spotify_network.parse import parse_all_files
from spotify_network.analysis import analyze_network


def create_network(folder: str = "MyData"):
    path = f"{os.getcwd()}/{folder}"
    all_songs = parse_all_files(path)
    G = nx.Graph()
    for i, current in enumerate(all_songs):
        if i == len(all_songs) - 1:
            break

        following = all_songs[i + 1]

        G.add_node(
            current["track"],
            artist=current["artist"],
            album=current["album"],
            liked=current["liked"],
            current=current["current"],
        )
        G.add_node(
            following["track"],
            artist=following["artist"],
            album=following["album"],
            liked=following["liked"],
            current=following["current"],
        )

        if G.has_edge(current["track"], following["track"]):
            G[current["track"]][following["track"]]["weight"] += 1
        else:
            # Ignore songs that are played for less than 30 seconds
            if current["ms_played"] < 30000:
                continue

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
    nx.write_gml(G, f"{filename}.gml")
    nx.write_gexf(G, f"{filename}.gexf")


if __name__ == "__main__":
    G = create_network()
    write_network(G, "filter")
