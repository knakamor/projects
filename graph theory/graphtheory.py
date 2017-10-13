import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from  collections import Counter, defaultdict
import pandas as pd

def load_data(filename):
    return nx.read_edgelist(filename, delimiter= '\t')

def get_degree(G):
    degree = G.degree()
    plt.hist(degree.values())
    plt.xlim(0,400)
    #plt.show()

def get_most_important(G):
    return Counter(nx.degree_centrality(G)).most_common(5)

def num_connected(G):
    total_num = []
    for i in  nx.connected_components(G):
        total_num.append(i)
    return len(total_num[0])

def hist_connected(G):
    list_connections = []
    for i in list(nx.connected_components(G))[0]:
        list_connections.append(len(i))
    series_connections = pd.Series(list_connections)
    series_connections[series_connections<1000].hist(bins=50)
    plt.show()

def get_betweenness(G):
    return Counter(nx.betweenness_centrality(G)).most_common(5)

def get_eigenvector_centrality(G):
    return Counter(nx.eigenvector_centrality(G)).most_common(5)







if __name__=='__main__':
    G = load_data('small_actor_edges.tsv')

    # degree = get_degree(G)

    most_important_5 = get_most_important(G)

    connected_components=num_connected(G)

    hist_connected=hist_connected(G)

    most_important_5_betweenness = get_betweenness(G)

    most_important_5_eigenvectoe = get_eigenvector_centrality(G)
