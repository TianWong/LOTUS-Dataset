import json
import sys
import networkx as nx
import os.path

def rank(input_file, top_file):
    with open(input_file, 'r') as infile:
        asn_network_data = json.loads(infile.read())

    with open(top_file, 'r') as topfile:
        top_data = json.loads(topfile.read())

    ranked_outfile = f"{os.path.splitext(input_file)[0]}_ranked.json"

    top_list = []
    G = nx.Graph()
    
    for asn_entry in asn_network_data:
        asn = asn_entry["asn"]
        if asn in top_data:
            top_list.append(asn)
        neighbors = set(asn_entry["peers"] + asn_entry["upstreams"])
        G.add_node(asn)
        G.add_edges_from(((asn, str(n)) for n in neighbors))
    
    lengths = nx.multi_source_dijkstra_path_length(G, top_list)
    loop_entries = set()
    for asn_entry in asn_network_data:
        try:
            asn_entry["rank"] = lengths[asn_entry["asn"]]
        except KeyError:
            loop_entries.add(asn_entry["asn"])

    asn_network_data = filter(lambda x: x["asn"] not in loop_entries, asn_network_data)
    
    with open(ranked_outfile, 'w') as outfile:
        json.dump(list(asn_network_data), outfile, indent=2, separators=(',',':'))
        return ranked_outfile

if __name__ == "__main__":
    rank(sys.argv[1], sys.argv[2])