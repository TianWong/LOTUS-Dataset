import re
import os
import json
import copy

def json_indent_limit(json_string, indent, limit):
    regex_pattern = re.compile(f'\n({indent}){{{limit}}}(({indent})+|(?=(}}|])))')
    return regex_pattern.sub('', json_string)

INFILE = 'the_internet.json'
OUTFILE = 'the_internet_cleaned.json'

if os.path.isfile(INFILE):
    with open(INFILE, 'r') as infile:
        asn_network_data = json.loads(infile.read())

asn_network_data_cleaned = copy.deepcopy(asn_network_data)

asns = [int(asn['asn']) for asn in asn_network_data]

missing = set()
present = set()

for i, asn in enumerate(asn_network_data):
    present.add(int(asn['asn']))
    for upstream in asn['upstreams']:
        if upstream not in asns:
            asn_network_data_cleaned[i]['upstreams'].remove(upstream)
            missing.add(upstream)
    for peer in asn['peers']:
        if peer not in asns:
            missing.add(peer)
            asn_network_data_cleaned[i]['peers'].remove(peer)

print(len(missing))
print(len(present))

with open(OUTFILE, 'w') as outfile:
    json_string = json.dumps(asn_network_data_cleaned, indent=1)
    json_string = json_indent_limit(json_string, ' ', 2)
    outfile.write(json_string)