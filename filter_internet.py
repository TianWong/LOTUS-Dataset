import json
import sys

def filter_internet(in_fp, output, attribute, match_set):
    """
    filter by attribute in a given match_set
    """
    output_d = []
    with open(output, "w") as f:
        asn_set = set()
        d = json.load(in_fp)
        for entry in d:
            if entry[attribute] in match_set:
                output_d.append(entry)
                asn_set.add(int(entry['asn']))
        for entry in output_d:
            entry['peers'] = [peer for peer in entry['peers'] if peer in asn_set]
            entry['upstreams'] = [peer for peer in entry['upstreams'] if peer in asn_set]
        json.dump(output_d, f, indent=2, separators=(',',':'))

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(f"Usage: filter_internet.py input output attribute [rir_name ...]")
    else:
        match_set = set(sys.argv[4:])
        print(f"matching on {match_set}")
        with open(sys.argv[1]) as in_fp:
            filter_internet(in_fp, sys.argv[2], sys.argv[3], match_set)
