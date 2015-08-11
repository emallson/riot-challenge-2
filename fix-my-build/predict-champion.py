import numpy as np
from sklearn.svm import LinearSVC
from sklearn.cross_validation import train_test_split
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

import glob
import json

def load_champ_data():
    paths = glob.glob('matches/*.json')[:1000]
    data = np.ndarray((len(paths) * 10, 8), dtype='int64')
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
                items.sort()
                data[i, 0] = int(champ)
                data[i, 1:] = map(int, items)
                i += 1

    return data

svc = LinearSVC()

print('loading data')
data = load_champ_data()
champ = data[0,0]
data[data[:,0] != champ, 0] = -1
data[data[:,0] == champ, 0] = 1
print('splitting data')
train, test = train_test_split(data, test_size=0.25)
print('training')
svc.fit(train[:,1:], train[:,0])
print('testing')
score = svc.decision_function(test[:,1:])
fpr = {}
tpr = {}
roc_auc = {}

fig = plt.figure()
fpr, tpr, thresholds = roc_curve(test[:, 0], score)
roc_auc = auc(fpr, tpr)
plt.plot(fpr, tpr, label='{0}, AUC: {1}'.format(champ, roc_auc))
plt.legend(loc='lower right')
plt.show()
# for c in set(test[:,0]):
#     cs = c_samples = (test[:, 0] == c)
#     print(test.shape)
#     print(test[cs, 0].shape, score[cs].squeeze().shape)
#     fpr[c], tpr[c] = roc_curve(test[cs, 0], score[cs, c])
#     roc_auc[c] = auc(fpr[c], tpr[c])

#     plt.plot(fpr[c], tpr[c], label='{0}, AUC: {1}'.format(c, roc_auc[c]))

plt.show()
# shit is fucked, yo
