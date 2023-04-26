import re
import os
import json
import sys

def json_indent_limit(json_string, indent, limit):
    regex_pattern = re.compile(f'\n({indent}){{{limit}}}(({indent})+|(?=(}}|])))')
    return regex_pattern.sub('', json_string)

def clean(INFILE, OUTFILE):
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
            print(self_asn, peer)
            return False
        if peer in providers and self_asn in providers[peer]:
            print(peer, self_asn)
            return False
        return True

    for entry in asn_network_data_cleaned:
        entry["peers"] = list(filter(lambda peer: provider_filter(peer, int(entry["asn"]), providers), entry["peers"]))

    with open(OUTFILE, 'w') as outfile:
        json_string = json.dumps(asn_network_data_cleaned, indent=1)
        json_string = json_indent_limit(json_string, ' ', 2)
        outfile.write(json_string)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: clean.py infile outfile")
    else:
        clean(sys.argv[1], sys.argv[2])