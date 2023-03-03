import os
import json

OUTFILE = 'situation.lotus'
with open('top_level_asn.json') as infile:
    ASPA_SOURCES = json.load(infile)
ATTACKER = 4134 # this is just random right now
ASPA_TARGETS = [21434] # this is just random right now
HOPS = 1
PRIORITY = 1

auto_aspa = '''autoASPA {} {}
'''

set_aspv = '''setASPV {} on {}
'''

attack = '''genAttack utilize {} {}
'''

initialize = '''addAllASInit
'''

start = '''run
showASList
'''

situation = ''
for aspa_source in ASPA_SOURCES:
    situation += auto_aspa.format(aspa_source, HOPS)
for aspa_target in ASPA_TARGETS:
    situation += set_aspv.format(aspa_target, PRIORITY)
situation += initialize
for aspa_target in ASPA_TARGETS:
    situation += attack.format(ATTACKER, aspa_target)
situation += start

with open(OUTFILE, 'w') as outfile:
    outfile.write(situation)
