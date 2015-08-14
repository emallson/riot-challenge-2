import luigi
import ratelim
import glob
import os
import json
import requests

API_KEY = '4d8a0cc4-02c2-4132-bd49-2e21b79ee81a'
BASE_URL = 'https://{region}.api.pvp.net'


@ratelim.patient(10, 10)
@ratelim.greedy(500, 600)
def get_match(region, id):
    return requests.get(BASE_URL.format(region=region) +
                        "/api/lol/{region}/v2.2/match/{id}".format(region=region, id=id), params={"api_key": API_KEY, "includeTimeline": True})


def load_data(version):
    ids = []
    for filename in glob.iglob('datasets/ap/{version}/*/*.json'
                               .format(version=version)):
        region = os.path.basename(filename).split('.')[0].lower()
        with open(filename, "r") as f:
            data = json.load(f)
            ids += [(region, id) for id in data]

    return ids


class DownloadMatch(luigi.Task):
    region = luigi.Parameter()
    match_id = luigi.Parameter()

    def output(self):
        return luigi.LocalTarget('datasets/matches/{0}.json'.format(self.match_id))

    def run(self):
        f = self.output().open('w')
        match = get_match(self.region, self.match_id)
        while match.status_code != 200:
            print(match)
            print('retrying...')
            match = get_match(self.region, self.match_id)

        f.write(match.text)
        f.close()


class FirstNMatches(luigi.Task):
    n = luigi.IntParameter(default=10000)

    def requires(self):
        old = load_data('5.11')[:self.n]
        new = load_data('5.14')[:self.n]
        for region, id in old + new:
            yield DownloadMatch(region=region, match_id=id)


# don't use, memory issues >.>
# class AllMatches(luigi.Task):
#     def requires(self):
#         old = load_data('5.11')
#         new = load_data('5.14')
#         for region, id in old + new:
#             yield DownloadMatch(region=region, match_id=id)

if __name__ == '__main__':
    luigi.run()
