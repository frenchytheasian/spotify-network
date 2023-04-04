import os

import networkx as nx

from parse import parse_all_files
from analysis import *


def create_network(folder: str = "MyData"):
    path = f"{os.getcwd()}/{folder}"
    all_songs = parse_all_files(path)
    G = nx.Graph()
    for i, current in enumerate(all_songs):
        if i == len(all_songs) - 1:
            break

        following = all_songs[i + 1]

        G.add_node(current["track"], artist=current["artist"], album=current["album"])
        G.add_node(following["track"], artist=following["artist"], album=following["album"])

        if G.has_edge(current["track"], following["track"]):
            G[current["track"]][following["track"]]["weight"] += 1
        else:
            G.add_edge(
                current["track"],
                following["track"],
                weight=1,
            )
    return G


def analyze_network(G: nx.Graph):
    get_degree_distribution(G)


def write_network(G: nx.Graph, filename: str = "spotify_network"):
    nx.write_gml(G, f"{filename}.gml")
    nx.write_gexf(G, f"{filename}.gexf")


if __name__ == "__main__":
    G = create_network()
    
