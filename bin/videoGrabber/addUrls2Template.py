#!/usr/bin/env python3
import json
import sys

BASE = sys.argv[1]
URLS = sys.argv[2].split(',')
TEMPLATE = BASE + "/config/pbvgTemplate.json"
PBVG_CNF = BASE + "/config/pbvgConfig.json"

for url in URLS:
    if not url.lower().startswith("http"):
        #print("URL List Error")
        exit(-1)

with open(TEMPLATE, 'r') as file:
    config = json.load(file)

config["DLbase"] = BASE + "/ytDL/"
config["Grupes"]["PBVG"]["urls"] = URLS

pretty = json.dumps(config, indent=2)
with open(PBVG_CNF, 'w') as out:
    out.write(pretty)
print(PBVG_CNF)
exit(0)

