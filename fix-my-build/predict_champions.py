import numpy as np
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

import glob
import json

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
    data = np.zeros((len(paths) * 10, 268), dtype='int64')
    i = 0
    for path in paths:
        with open(path, 'r') as p:
            try:
                j = json.load(p)
            except Exception as e:
                print(path)
                raise e
            for participant in j['participants']:
                stats = participant["stats"]
                champ = participant["championId"]
                items = [stats["item0"],
                         stats["item1"],
                         stats["item2"],
                         stats["item3"],
                         stats["item4"],
                         stats["item5"],
                         stats["item6"]]
                data[i, 0] = int(champ)
                for item in items:
                    index = item_id_to_index(item)
                    if index is not None:
                        data[i, index+1] = 1
                i += 1

    return data

svc = LinearSVC()

print('loading data')
data = load_champ_data()
# champ = data[0,0]
# data[data[:,0] != champ, 0] = -1
# data[data[:,0] == champ, 0] = 1
print('splitting data')
train, test = train_test_split(data, test_size=0.25)
print('training')
svc.fit(train[:,1:], train[:,0])
print('testing')
score = svc.predict(test[:,1:])
fpr = {}
tpr = {}
roc_auc = {}

# fpr, tpr, thresholds = roc_curve(test[:, 0], score)
# roc_auc = auc(fpr, tpr)
# print(fpr, tpr)
# plt.plot(fpr, tpr, label='{0}, AUC: {1}'.format(champ, roc_auc))
# plt.legend(loc='lower right')
# plt.show()
fig = plt.figure()
for i, c in enumerate(set(test[:,0])):
    fpr[c], tpr[c], _ = roc_curve(test[:, 0] == c, score == c)
    roc_auc[c] = auc(fpr[c], tpr[c])

    plt.plot(fpr[c], tpr[c], label='{0}, AUC: {1}'.format(c, roc_auc[c]))

    plt.legend(loc='lower right')
    plt.savefig('figs/{c}.png'.format(c=c))
    plt.clf()
# shit is fucked, yo
