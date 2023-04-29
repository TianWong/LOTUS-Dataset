import os
import json
import sys

def search_upstream(INFILE):
    top_outfile = f"{os.path.splitext(INFILE)[0]}_top.json"
    if os.path.isfile(INFILE):
        with open(INFILE, 'r') as infile:
            asn_network_data = json.loads(infile.read())

    top_level_asns = []

    for asn in asn_network_data:
        if len(asn['upstreams']) == 0:
            # print(f'{asn["asn"]}\t{asn["country"]}\t{asn["rir"]}')
            top_level_asns.append(asn['asn'])

    with open(top_outfile, 'w') as outfile:
        outfile.write(json.dumps(top_level_asns))
        return top_outfile

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: search_upstream.py infile")
    else:
        search_upstream(sys.argv[1])