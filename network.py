import os

import networkx as nx

from parse import parse_all_files
from analysis import *

def create_network():
    folder = 'MyData-min'
    
    path = f'{os.getcwd()}/{folder}'
    all_songs = parse_all_files(path)
    G = nx.Graph()
    for i, song in enumerate(all_songs):
        if i == len(all_songs) - 1:
            break
        G.add_edge(song['track'], all_songs[i + 1]['track'])
    return G

def analyze_network(G: nx.Graph):
    get_degree_distribution(G)

def write_network(G: nx.Graph, filename: str = 'spotify_network'):
    nx.write_gml(G, f'{filename}.gml')
    nx.write_gexf(G, f'{filename}.gexf')


if __name__ == "__main__":
    G = create_network()
    analyze_network(G)
    
