import pickle
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from mlmodel.mfcf import MatrixFactorization
from pymongo import MongoClient
import os

secret_key = os.urandom(32)

# enable debug mode
DEBUG = True

# connect to the database
client = MongoClient("localhost", 27017)
db = client["MRSBBDB"]

# mfcf Model
W = np.asarray([])
X = np.asarray([])
d = np.asarray([])
b = np.asarray([])
for model in db["model"].find():
    if model['name'] == "W":
        W = np.asarray(pickle.loads(model['value']))
    elif model['name'] == "X":
        X = np.asarray(pickle.loads(model['value']))
    elif model['name'] == "d":
        d = np.asarray(model['value'])
    elif model['name'] == "b":
        b = np.asarray(model['value'])
ratings_cursor = db['rating'].find()
ratings_dataframe = pd.DataFrame(list(ratings_cursor), columns=[
    'userId', 'movieId', 'rating', 'timestamp']).astype({'userId': int, 'movieId': int, 'rating': int, })
ratings_matrix = np.asmatrix(ratings_dataframe)
rate_train, rate_test = train_test_split(
    ratings_matrix, test_size=0.2, random_state=10)
mfcf_model = MatrixFactorization(
    Y=ratings_matrix, K=50, lam=.01, Xinit=X, Winit=W, bInit=b, dInit=d, learning_rate=50, max_iter=30)
