import luigi
import numpy as np
from collection import FirstNMatches
import json


def read_from_kp(obj, kp):
    kp = kp.split('.')
    for key in kp:
        obj = obj[key]
    return obj


class Feature(luigi.Task):
    n = luigi.IntParameter(default=10000)

    def key(self):
        return 'feature'

    def requires(self):
        return FirstNMatches(n=self.n).requires()

    def output(self):
        return luigi.LocalTarget('datasets/np/{0}_{1}.npy'
                                 .format(self.key(), self.n))

    def value(self, obj):
        return False

    def run(self):
        vals = []
        for inp in self.input():
            f = inp.open('r')
            obj = json.load(f)
            value = self.value(obj)
            vals += value
            f.close()

        arr = np.array(vals)
        out = self.output().open('w')
        np.save(out, arr)
        out.close()


class ChampionFeature(Feature):
    champ_id = luigi.IntParameter()
    keypath = luigi.Parameter()

    def key(self):
        return 'champ_{0}_{1}_feature'.format(self.champ_id, self.keypath)

    def filter(self, obj):
        return obj["championId"] == self.champ_id

    def champ_value(self, obj):
        return read_from_kp(obj, self.keypath)

    def value(self, obj):
        vals = []
        for participant in obj['participants']:
            if self.filter(participant):
                vals.append(self.champ_value(participant))
        return vals


class ChampionVersionFeature(ChampionFeature):
    keypath = 'version'
    def value(self, obj):
        vals = []
        for participant in obj['participants']:
            if self.filter(participant):
                vals.append('.'.join(obj['matchVersion'].split('.')[:2]))
        return vals

NUM_ITEMS = 267
with open('datasets/static/item.json', 'r') as f:
    items = json.load(f)
    item_id_map = {int(k): i for i, k in enumerate(items['data'].keys())}

def item_id_to_index(id):
    if int(id) in item_id_map:
        return item_id_map[id]
    return None


class ChampionItemsFeature(ChampionFeature):
    keypath = 'items'
    def key(self):
        return 'champ_{0}_items_feature'.format(self.champ_id)

    def champ_value(self, obj):
        stats = obj['stats']
        items = [stats["item0"],
                 stats["item1"],
                 stats["item2"],
                 stats["item3"],
                 stats["item4"],
                 stats["item5"],
                 stats["item6"]]
        data = np.zeros((NUM_ITEMS,))
        for item in items:
            data[item_id_to_index(item)] = 1
        return data

if __name__ == '__main__':
    luigi.run()
