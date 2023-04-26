import os
import json
import sys

def search_upstream(INFILE, OUTFILE):
    if os.path.isfile(INFILE):
        with open(INFILE, 'r') as infile:
            asn_network_data = json.loads(infile.read())

    top_level_asns = []

    for asn in asn_network_data:
        if len(asn['upstreams']) == 0:
            print(f'{asn["asn"]}\t{asn["country"]}\t{asn["rir"]}')
            top_level_asns.append(asn['asn'])

    with open(OUTFILE, 'w') as outfile:
        outfile.write(json.dumps(top_level_asns))

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: search_upstream.py infile outfile")
    else:
        search_upstream(sys.argv[1], sys.argv[2])