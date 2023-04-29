# filter to ASNs with CA or GB as country
python filter_internet.py the_internet.json data/ca_gb/ca_gb.json country CA GB

# clean up orphaned ASNs
python clean.py data/ca_gb/ca_gb.json

# get edge nodes of CA
python edge_node_filter.py data/ca_gb/ca_gb_cleaned_ranked.json CA

# convert to lotus input commands
python load_lotus_network.py data/ca_gb/ca_gb_cleaned_ranked.json data/ca_gb/ca_gb_cleaned_ranked.lotus