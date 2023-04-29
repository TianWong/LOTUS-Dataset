import re
import networkx as nx
import os.path
import json
import sys

from search_upstreams import search_upstream
from rank import rank

MIN_SIZE = 10

def json_indent_limit(json_string, indent, limit):
    regex_pattern = re.compile(f'\n({indent}){{{limit}}}(({indent})+|(?=(}}|])))')
    return regex_pattern.sub('', json_string)

def clean(INFILE):
    cleaned_outfile = f"{os.path.splitext(INFILE)[0]}_cleaned.json"
    if os.path.isfile(INFILE):
        with open(INFILE, 'r') as infile:
            asn_network_data = json.loads(infile.read())

    asn_network_data_cleaned = []

    asns = set([int(asn['asn']) for asn in asn_network_data])

    providers = {}

    for asn in asn_network_data:
        cleaned_entry = {"rir": asn["rir"],
                            "country": asn["country"],
                            "asn": asn["asn"],
                            "prefixes": asn["prefixes"]
        }
        cleaned_entry["upstreams"] = [upstream for upstream in asn["upstreams"] if upstream in asns]
        providers[int(cleaned_entry["asn"])] = cleaned_entry["upstreams"]
        cleaned_entry["peers"] = [peer for peer in asn["peers"] if peer in asns and peer not in cleaned_entry["upstreams"]]
        asn_network_data_cleaned.append(cleaned_entry)

    def provider_filter(peer, self_asn, providers):
        if self_asn in providers and peer in providers[self_asn]:
            # print(self_asn, peer)
            return False
        if peer in providers and self_asn in providers[peer]:
            # print(peer, self_asn)
            return False
        return True

    for entry in asn_network_data_cleaned:
        entry["peers"] = list(filter(lambda peer: provider_filter(peer, int(entry["asn"]), providers), entry["peers"]))

    G = nx.Graph()
    for asn_entry in asn_network_data_cleaned:
        neighbors = asn_entry["peers"] + asn_entry["upstreams"]
        asn = asn_entry["asn"]
        G.add_node(asn)
        G.add_edges_from(((asn, str(n)) for n in neighbors))

    removed = set()
    for component in list(nx.connected_components(G)):
        if len(component) < MIN_SIZE:
            for node in component:
                G.remove_node(node)
                removed.add(node)

    asn_network_data_cleaned = list(filter(lambda x: x["asn"] not in removed, asn_network_data_cleaned))

    with open(f"graphlet_distance/{os.path.splitext(cleaned_outfile)[0].split('/')[-1]}_edges.txt", "w") as edgefile:
        for x, y in G.edges():
            print(f"{x} {y}", file=edgefile)

    with open(cleaned_outfile, 'w') as outfile:
        json_string = json.dumps(asn_network_data_cleaned, indent=1)
        json_string = json_indent_limit(json_string, ' ', 2)
        outfile.write(json_string)
        return cleaned_outfile

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: clean.py infile")
    else:
        cleaned_outfile = clean(sys.argv[1])
        top_outfile = search_upstream(cleaned_outfile)
        ranked_outfile = rank(cleaned_outfile, top_outfile)