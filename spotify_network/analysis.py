import json

import networkx as nx
from matplotlib import pyplot as plt

### Code is not optimized between functions. A lot of repeated work is done.


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

def clustering_coefficient_distribution():
    """Generate a linear and log log plot of the clustering coefficient distribution of the network
    """

    G = nx.read_gml("All.gml")

    clustering_coefficients = nx.clustering(G).values()
    coefficient_counts = dict()
    for coefficient in clustering_coefficients:
        if coefficient not in coefficient_counts:
            coefficient_counts[coefficient] = 0
        coefficient_counts[coefficient] += 1

    x = list(coefficient_counts.keys())
    y = list(coefficient_counts.values())

    plt.plot(x, y, "o")
    plt.xlabel("Clustering Coefficient")
    plt.ylabel("Count")
    plt.title("Clustering Coefficient Distribution")
    plt.savefig("clustering_coefficient_distribution_linear.png")


    plt.loglog(x, y, "o")
    plt.xlabel("Clustering Coefficient")
    plt.ylabel("Count")
    plt.title("Clustering Coefficient Distribution")
    plt.savefig("clustering_coefficient_distribution.png")


def betweenness_centrality_distribution():
    """Generate a log log plot of the betweenness centrality distribution of the network
    """

    G = nx.read_gml("All.gml")

    betweenness_centrality = nx.betweenness_centrality(G).values()
    centrality_counts = dict()
    for centrality in betweenness_centrality:
        if centrality not in centrality_counts:
            centrality_counts[centrality] = 0
        centrality_counts[centrality] += 1

    x = list(centrality_counts.keys())
    y = list(centrality_counts.values())

    plt.loglog(x, y, "o")
    plt.xlabel("Betweenness Centrality")
    plt.ylabel("Count")
    plt.title("Betweenness Centrality Distribution")
    plt.savefig("betweenness_centrality_distribution.png")


def get_largest_hub(G):
    """Get the largest hub in the network

    Args:
        G (nx.Graph): The network to analyze

    Returns:
        str: The name of the largest hub
    """
    degrees = dict(G.degree())
    largest_hub = max(degrees, key=degrees.get)
    degree = degrees[largest_hub]

    second_largest_hub = max(degrees, key=lambda x: degrees[x] if x != largest_hub else 0)
    second_degree = degrees[second_largest_hub]
    
    return [(largest_hub, degree), (second_largest_hub, second_degree)]

def get_biggest_bottleneck(G):
    """Get the biggest bottleneck in the network

    Args:
        G (nx.Graph): The network to analyze

    Returns:
        (str, int): A tuple containing the name of the bottleneck and the betweenness centrality of the bottleneck
    """
    betweenness_centrality = nx.betweenness_centrality(G)
    biggest_bottleneck = max(betweenness_centrality, key=betweenness_centrality.get)
    centrality = betweenness_centrality[biggest_bottleneck]
    return biggest_bottleneck, centrality
    
def generate_erdos_renyi_graph():
    """Generate an Erdos-Renyi graph with n nodes and probability p

    Args:
        n (int): Number of nodes
        p (float): Probability of edge creation

    Returns:
        nx.Graph: The generated graph
    """
    G = nx.fast_gnp_random_graph(13050, p=0.000539)
    nx.write_gml(G, "ErdosRenyi.gml")
    return G

def generate_scale_free_graph():
    """Generate a scale free graph with n nodes and m edges

    Args:
        n (int): Number of nodes
        m (int): Number of edges

    Returns:
        nx.Graph: The generated graph
    """
    G = nx.barabasi_albert_graph(13050, 80)
    nx.write_gml(G, "ScaleFree.gml")
    return G

if __name__ == "__main__":
    generate_scale_free_graph()
