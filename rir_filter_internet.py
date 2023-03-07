import json
import sys

def rir_filter_internet(in_fp, output, match_set):
    """
    filter by rirs in a given match_set
    """
    output_d = []
    with open(output, "w") as f:
        asn_set = set()
        d = json.load(in_fp)
        for entry in d:
            if entry["rir"] in match_set:
                output_d.append(entry)
                asn_set.add(int(entry['asn']))
        for entry in output_d:
            entry['peers'] = [peer for peer in entry['peers'] if peer in asn_set]
            entry['upstreams'] = [peer for peer in entry['upstreams'] if peer in asn_set]
        json.dump(output_d, f, indent=2, separators=(',',':'))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {rir_filter_internet} in_file output [rir_name ...]")
    else:
        match_set = set(sys.argv[3:])
        print(f"matching on {match_set}")
        with open(sys.argv[1]) as in_fp:
            rir_filter_internet(in_fp, sys.argv[2], match_set)

# usa_eu.json:
#   python rir_filter_internet.py the_internet_cleaned.json usa_eu.json arin ripencc