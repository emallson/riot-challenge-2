import json
import requests
import ratelim
import glob
import os
from time import sleep

API_KEY = '4d8a0cc4-02c2-4132-bd49-2e21b79ee81a'
BASE_URL = 'https://na.api.pvp.net'

@ratelim.greedy(10, 10)
@ratelim.greedy(500, 600)
def get_match(region, id):
    return requests.get(BASE_URL + "/api/lol/{region}/v2.2/match/{id}".format(region=region, id=id), params={"api_key": API_KEY, "includeTimeline": True})

def load_data():
    ids = []
    for filename in glob.iglob('../datasets/ap/*/*/*.json'):
        region = os.path.basename(filename).split('.')[0].lower()
        with open(filename, "r") as f:
            data = json.load(f)
            ids += [(region, id) for id in data]

    return ids

def download_match((region, id)):
    print(region, id)
    with open('matches/{id}.json'.format(id=id), 'w') as outfile:
        match = get_match(region, id)
        while match.status_code != 200:
            print(match)
            print("retrying...")
            match = get_match(region, id)
        outfile.write(match.text)

def download_all():
    matches = load_data()
    start = matches.index(('br', 542567252))
    matches = matches[start+1:]
    map(download_match, matches)

download_all()
