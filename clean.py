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

    for i, asn in enumerate(asn_network_data):
        cleaned_entry = {"rir": asn["rir"],
                            "country": asn["country"],
                            "asn": asn["asn"],
                            "prefixes": asn["prefixes"]
        }
        cleaned_entry["upstreams"] = [upstream for upstream in asn["upstreams"] if upstream in asns]
        cleaned_entry["peers"] = [peer for peer in asn["peers"] if peer in asns and peer not in cleaned_entry["upstreams"]]
        if len(cleaned_entry["upstreams"]) + len(cleaned_entry["peers"]) > 0:
            asn_network_data_cleaned.append(cleaned_entry)

    with open(OUTFILE, 'w') as outfile:
        json_string = json.dumps(asn_network_data_cleaned, indent=1)
        json_string = json_indent_limit(json_string, ' ', 2)
        outfile.write(json_string)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: clean.py infile outfile")
    else:
        clean(sys.argv[1], sys.argv[2])