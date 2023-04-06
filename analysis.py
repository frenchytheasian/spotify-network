import networkx as nx
from matplotlib import pyplot as plt

def analyze_degree(G: nx.Graph):
    degrees = G.degree()
    degrees = sorted(degrees, key=lambda x: x[1])
    print(degrees)

def get_degree_distribution(G: nx.Graph):
    degree_distribution = nx.degree_histogram(G)
    analyze_degree(G)
    plt.bar(range(0, len(degree_distribution)), degree_distribution, width=0.80, color='b')
    plt.show()

def analyze_network(G: nx.Graph):
    get_degree_distribution(G)