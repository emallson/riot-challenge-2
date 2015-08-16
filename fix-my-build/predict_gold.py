#!/usr/bin/env python2
import numpy as np
from sklearn import svm, metrics, grid_search
from sklearn.cross_validation import train_test_split
# todo: metrics

import glob
import json

CHAMP = 1
NUM_ITEMS = 267

with open('../datasets/static/item.json', 'r') as f:
    items = json.load(f)
    item_id_map = {int(k): i for i, k in enumerate(items['data'].keys())}

def item_id_to_index(id):
    if int(id) in item_id_map:
        return item_id_map[id]
    return None

def load_champ_data():
    paths = glob.glob('matches/*.json')[:10000]
    inputs = []
    outputs = []
    for path in paths:
        with open(path, 'r') as p:
            j = json.load(p)
            for participant in j['participants']:
                stats = participant['stats']
                champ = participant['championId']
                if not champ == CHAMP:
                    continue
                items = [stats["item0"],
                         stats["item1"],
                         stats["item2"],
                         stats["item3"],
                         stats["item4"],
                         stats["item5"],
                         stats["item6"]]
                gold = stats['goldEarned']

                inp = np.zeros((NUM_ITEMS,))
                for item in items:
                    inp[item_id_to_index(item)] = 1
                inputs.append(inp)
                outputs.append(gold)
    return np.array(inputs), np.array(outputs)

grid = [
    {'kernel': ['linear'], 'C': np.logspace(1, 10)},
    {'kernel': ['rbf', 'poly'], 'gamma': np.linspace(1e-5, 1), 'C': np.logspace(1, 10)}
]

if __name__ == '__main__':
    N = svm.SVR()
    M = grid_search.GridSearchCV(N, grid[0], lambda M, X, y: metrics.mean_squared_error(y, M.predict(X)))

    print('loading data')
    npz = np.load('gold.npz')
    inputs, outputs = (npz['inputs'], npz['outputs'])
    print('splitting')
    in_train, in_test, out_train, out_test = train_test_split(inputs, outputs, test_size=0.25)
    print('training')
    M.fit(in_train, out_train)
    print('testing')
    result = M.predict(in_test)

    print('Explained Variance Score: ', metrics.explained_variance_score(out_test, result))
    print('Mean Squared Error: ', metrics.mean_squared_error(out_test, result))
