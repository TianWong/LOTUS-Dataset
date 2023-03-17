import json
import os
import sys

if os.path.isfile(sys.argv[1]):
    with open(sys.argv[1], "r") as in_fp:
        asn_network_data = json.load(in_fp)

print(f"filtering for edge of {sys.argv[2]}")
as_country_dict = {int(asn["asn"]):[asn["country"], asn["peers"]+asn["upstreams"]] for asn in asn_network_data}
print(as_country_dict)
edge_ls = []
for key, val in as_country_dict.items():
    print(key, val)
    if val[0] == sys.argv[2]:
        for neighbor in val[1]:
            if as_country_dict[neighbor][0] != sys.argv[2]:
                edge_ls.append(key)
                break

with open(f"{sys.argv[1]}_{sys.argv[2]}_edge_nodes", "w") as out_fp:
    json.dump(edge_ls, out_fp)