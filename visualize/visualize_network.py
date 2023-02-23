import json
import os
from matplotlib import pyplot as plt
import networkx as nx

GEXF_NAME = 'arin_network.gexf'

def update_gexf(input_file='../the_internet.json', output_file=GEXF_NAME):
    if os.path.isfile(input_file):
        with open(input_file, 'r') as infile:
            asn_network_data = json.loads(infile.read())

    G = nx.DiGraph()
    for asn in asn_network_data:
        G.add_edges_from([(asn['asn'], peer) for peer in asn['peers']], color="red", label="peers")
        G.add_edges_from([(asn['asn'], upstream) for upstream in asn['upstreams']], color="green", label="provider")

    nx.write_gexf(G, output_file)

def graph_gexf(input_file=GEXF_NAME, output_file='arin_network.png'):
    G = nx.read_gexf(input_file)
    nx.draw(G)
    plt.savefig(output_file)