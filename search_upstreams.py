import os
import json

INFILE = 'the_internet_cleaned.json'
OUTFILE = 'top_level_asn.json'

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