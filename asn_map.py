import requests
import time
import json
import re
import os

# A bit of code to make JSON indentation look a lot more human-readable
# Courtesy of https://stackoverflow.com/questions/13249415/how-to-implement-custom-indentation-when-pretty-printing-with-the-json-module
def json_indent_limit(json_string, indent, limit):
    regex_pattern = re.compile(f'\n({indent}){{{limit}}}(({indent})+|(?=(}}|])))')
    return regex_pattern.sub('', json_string)

ROOT_URL = 'https://api.bgpview.io/asn'
DELAY = 1
IP_VERSION = 4

# with open('api_access_token', 'r') as infile:
#    access_token = infile.read()

# auth = requests.auth.HTTPBasicAuth('user', access_token)

def get_asn_data(asn):
    #asn_r = requests.get(f'{ROOT_URL}/{asn}') #, headers={'Authorization': f'Token {access_token}'})
    #if asn_r.status_code != 200: return
    #asn_data = json.loads(asn_r.text)['data']
    #name = asn_data['name']
    #country = asn_data['country_code']
    #rir = asn_data['rir_allocation']['rir_name']

    prefix_r = requests.get(f'{ROOT_URL}/{asn}/prefixes') #, headers={'Authorization': f'Token {access_token}'})
    if prefix_r.status_code != 200: return
    prefix_data = json.loads(prefix_r.text)['data']
    prefixes = [prefix['prefix'] for prefix in prefix_data[f'ipv{IP_VERSION}_prefixes']]
    
    peers_r = requests.get(f'{ROOT_URL}/{asn}/peers') #, headers={'Authorization': f'Token {access_token}'})
    if peers_r.status_code != 200: return
    peers_data = json.loads(peers_r.text)['data']
    peers = [peer['asn'] for peer in peers_data[f'ipv{IP_VERSION}_peers']]

    upstream_r = requests.get(f'{ROOT_URL}/{asn}/upstreams') #, headers={'Authorization': f'Token {access_token}'})
    if upstream_r.status_code != 200: return
    upstream_data = json.loads(upstream_r.text)['data']
    upstreams = [upstream['asn'] for upstream in upstream_data[f'ipv{IP_VERSION}_upstreams']]

    return prefixes, peers, upstreams #name, country, rir, prefixes, peers, upstreams

with open('nro-delegated-stats', 'r') as infile:
    data = infile.read()

as_rows = data.split('\n')[4:]

# Format:
# registry|cc|type|start|value|date|status|opaque-id
# See https://www.nro.net/wp-content/uploads/nro-extended-stats-readme5.txt

# example of lines in the file:
# arin|US|asn|2|1|19910110|assigned|c3a16289a7ed6fb75fec2e256e5b5101|e-stats
# arin|US|ipv4|98.16.0.0|524288|20070205|assigned|6c065d5b54b877781f05e7d30ebfff28|e-stats
# arin|US|ipv6|2620:63:6000::|48|20190104|assigned|bc22d5239e4066079d58e60f791983c7|e-stats

asn_network_data = []

checkpoint_asn = -1
if os.path.isfile('the_internet.json'):
    with open('the_internet.json', 'r') as infile:
        asn_network_data = json.loads(infile.read())
        checkpoint_asn = int(asn_network_data[-1]['asn'])

try:
    for as_row in as_rows:
        rir, country, service_type, asn, _, _, allocation, _, _ = as_row.split('|')
        if allocation != 'assigned': continue
        if service_type != 'asn': continue
        if int(asn) <= checkpoint_asn: continue
        print(asn)
        asn_data = None
        tries = 0
        while asn_data == None:
            tries += 1
            if tries > 10: break
            time.sleep(DELAY)
            asn_data = get_asn_data(asn)
        if asn_data == None: continue
        prefixes, peers, upstreams = asn_data
        if len(prefixes) == 0: continue
        info = {'rir':rir, 'country':country, 'asn':asn, 'prefixes':prefixes, 'peers':peers, 'upstreams':upstreams}
        asn_network_data.append(info)
except Exception as e:
    print(e)
finally:
    with open('the_internet.json', 'w') as outfile:
        json_string = json.dumps(asn_network_data, indent=1)
        json_string = json_indent_limit(json_string, ' ', 2)
        outfile.write(json_string)