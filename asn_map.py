import requests
import time
import json
import networkx

ROOT_URL = 'https://api.bgpview.io/asn/'
DELAY = 0.04

with open('api_access_token', 'r') as infile:
    access_token = infile.read()

def get_asn_data(asn):
    asn_r = requests.get(f'{ROOT_URL}/{asn}', headers={'Authorization': f'Token {access_token}'})
    if asn_r.status_code != 200: return
    asn_data = json.loads(asn_r.text)['data']['rir_allocation']
    peers_r = requests.get(f'{ROOT_URL}/{asn}/peers', headers={'Authorization': f'Token {access_token}'})
    if peers_r.status_code != 200: return
    upstream_r = requests.get(f'{ROOT_URL}/{asn}/upstreams', headers={'Authorization': f'Token {access_token}'})
    if upstream_r.status_code != 200: return

#for thing in loop:
#    get_asn_data(asn)
#    time.sleep(DELAY)