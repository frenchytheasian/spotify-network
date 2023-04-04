import networkx as nx
from matplotlib import pyplot as plt

def analyze_degree(G: nx.Graph):
    degrees = G.degree()
    degrees = sorted(degrees, key=lambda x: x[1])
    print(degrees)

def get_degree_distribution(G: nx.Graph):
    degree_distribution = nx.degree_histogram(G)
    bins, counts = zip(*enumerate(degree_distribution))
    analyze_degree(G)
    plt.bar(bins, counts, width=0.80, color='b')
    plt.show()