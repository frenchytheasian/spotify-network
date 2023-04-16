import json

import networkx as nx
from matplotlib import pyplot as plt


def analyze_network():
    G = nx.read_gml("All.gml")

    attributes = {
        "node_count": nx.number_of_nodes(G),
        "edge_count": len(nx.edges(G)),
        "density": nx.density(G),
        "average_degree": sum(dict(G.degree()).values()) / nx.number_of_nodes(G),
        "average_weighted_degree": sum(dict(G.degree(weight="weight")).values())
        / nx.number_of_nodes(G),
        "average_clustering_coefficient": nx.average_clustering(G),
    }

    json.dump(attributes, open("network_attributes.json", "w"), indent=4)


def degree_distribution():
    """Generate a log log plot of the degree distribution of the network

    Args:
        G (nx.Graph): The network to analyze
    """
    G = nx.read_gml("All.gml")

    degrees = dict(G.degree()).values()
    degree_counts = dict()
    for degree in degrees:
        if degree not in degree_counts:
            degree_counts[degree] = 0
        degree_counts[degree] += 1

    x = list(degree_counts.keys())
    y = list(degree_counts.values())

    plt.loglog(x, y, "o")
    plt.xlabel("Degree")
    plt.ylabel("Count")
    plt.title("Degree Distribution")
    plt.savefig("degree_distribution.png")


def shortest_path_distribution():
    """Generate a log log plot of the shortest path distribution of the network
    """

    G = nx.read_gml("All.gml")

    shortest_paths = nx.shortest_path_length(G)
    path_lengths = dict()
    for _, paths in shortest_paths:
        for _, length in paths.items():
            if length not in path_lengths:
                path_lengths[length] = 0
            path_lengths[length] += 1

    x = list(path_lengths.keys())
    y = list(path_lengths.values())

    plt.loglog(x, y, "o")
    plt.xlabel("Path Length")
    plt.ylabel("Count")
    plt.title("Shortest Path Distribution")
    plt.savefig("shortest_path_distribution.png")


if __name__ == "__main__":
    shortest_path_distribution()
