import pickle
from config import db, mfcf_model
import numpy as np
doc = db["movie"].find()

models = db["model"].find()
for model in models:
    if model['name'] == "W":
        W = np.asarray(pickle.loads(model['value']))
    elif model['name'] == "X":
        X = np.asarray(pickle.loads(model['value']))
    elif model['name'] == "d":
        d = np.asarray(model['value'])
    elif model['name'] == "b":
        b = np.asarray(model['value'])

WW = np.loadtxt('./data/W.csv', delimiter=',')
print(W[:, 6040])
print(W.shape)
print(d.shape)
