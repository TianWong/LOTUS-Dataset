import os
import json

INFILE = 'the_internet.json'
OUTFILE = 'the_internet.lotus'

if os.path.isfile(INFILE):
    with open(INFILE, 'r') as infile:
        asn_network_data = json.loads(infile.read())

peer_connections = []

with open(OUTFILE, 'w') as outfile:
    for asn in asn_network_data:
        outfile.write(f'addAS {asn["asn"]}\n')
    for asn in asn_network_data:
        for upstream in asn['upstreams']:
            outfile.write(f'addConnection down {upstream} {asn["asn"]}\n')
    for asn in asn_network_data:
        for peer in asn['peers']:
            peer_connection = set((peer, asn['asn']))
            if peer_connection not in peer_connections:
                peer_connections.append(peer_connection)
                outfile.write(f'addConnection peer {asn["asn"]} {peer}\n')