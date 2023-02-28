from flask import Flask
from flask_cors import CORS
from controller.auth import auth_bp
from controller.movie import movie_bp
from controller.rating import rating_bp
from controller.recommender import recommender_bp
from config import db, mfcf_model, rate_test
import numpy as np
import pickle
import bson

app = Flask(__name__)
CORS(app)
app.config.from_object('config')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(movie_bp, url_prefix='/movie')
app.register_blueprint(rating_bp, url_prefix='/rating')
app.register_blueprint(recommender_bp, url_prefix='/recommender')


if __name__ == "__main__":
    if len(list(db["model"].find())) == 0:
        W = np.loadtxt('./data/W.csv', delimiter=',')
        X = np.loadtxt('./data/X.csv', delimiter=',')
        d = np.loadtxt('./data/d.csv', delimiter=',')
        b = np.loadtxt('./data/b.csv', delimiter=',')

        wf = {"name": "W", "value": bson.Binary(pickle.dumps(W, protocol=2))}
        xf = {"name": "X", "value": bson.Binary(pickle.dumps(X, protocol=2))}
        df = {"name": "d", "value": d.tolist()}
        bf = {"name": "b", "value": b.tolist()}

        db["model"].insert_one(wf)
        db["model"].insert_one(xf)
        db["model"].insert_one(df)
        db["model"].insert_one(bf)
    if db['rating'].find_one(sort=[("userId", 1)])["userId"] != 0:
        for i in db['rating'].find():
            i["userId"] -= 1
            i["movieId"] -= 1
            db['rating'].update_one({"_id": i["_id"]}, {"$set": i})
    if db['movie'].find_one(sort=[("movieId", 1)])["movieId"] != 0:
        for i in db['movie'].find():
            i["movieId"] -= 1
            db["movie"].update_one({"_id": i["_id"]}, {"$set": i})
    print(mfcf_model.evaluate_RMSE(rate_test))
    print(mfcf_model.n_ratings)
    app.run(debug=True)
