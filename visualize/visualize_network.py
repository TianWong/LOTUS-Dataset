import json
import os
import sys
from matplotlib import pyplot as plt
import networkx as nx

def update_gexf(input_file, output_file):
    if os.path.isfile(input_file):
        with open(input_file, 'r') as infile:
            asn_network_data = json.loads(infile.read())

    G = nx.DiGraph()
    for asn in asn_network_data:
        if 'rank' not in asn:
            print(asn)
        G.add_edges_from([(asn['asn'], peer) for peer in asn['peers']], color="red", label="peers")
        G.add_edges_from([(asn['asn'], upstream) for upstream in asn['upstreams']], color="green", label="provider")
    for asn in asn_network_data:
        if G.has_node(asn['asn']):
            G.nodes[asn['asn']].update({'rank':asn['rank']})

    nx.write_gexf(G, output_file)

def graph_gexf(input_file, output_file):
    G = nx.read_gexf(input_file)
    nx.draw(G)
    plt.savefig(output_file)

if __name__ == "__main__":
    update_gexf(sys.argv[1], sys.argv[2])