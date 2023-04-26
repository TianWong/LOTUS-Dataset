# filter to ASNs with CA or GB as country
python filter_internet.py the_internet.json data/ca_gb/ca_gb.json country CA GB

# clean up orphaned ASNs
python clean.py data/ca_gb/ca_gb.json data/ca_gb/ca_gb_cleaned.json

# filter to top level ASNs in dataset
python search_upstreams.py data/ca_gb/ca_gb_cleaned.json data/ca_gb/ca_gb_top.json

# use top level ASNs to compute ASN rank
python rank.py data/ca_gb/ca_gb_cleaned.json data/ca_gb/ca_gb_cleaned_ranked.json data/ca_gb/ca_gb_top.json

# convert to lotus input commands
python load_lotus_network.py data/ca_gb/ca_gb_cleaned_ranked.json data/ca_gb/ca_gb_cleaned_ranked.lotus