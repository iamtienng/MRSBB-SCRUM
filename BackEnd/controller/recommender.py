from flask import Blueprint, jsonify, request
from config import db, mfcf_model
from pymongo import ReturnDocument
import numpy as np
import bson
import pickle
import json

recommender_bp = Blueprint('recommender_bp', __name__)


@recommender_bp.route("/predict/one/", methods=['POST'])
def recommender_predict():
    try:
        data = request.get_json()
        userId = data['userId']
        movieId = data['movieId']
        pred = mfcf_model.pred(userId, movieId)
        return pred, 200
    except:
        return None, 500


@recommender_bp.route("/user/create/", methods=['POST'])
def create_wt_d_for_user():
    # try:
    data = request.get_json()
    userId = data['userId']
    # mfcf_model.W = np.append(mfcf_model.W, np.random.randn(
    #     mfcf_model.W.shape[0], 1), axis=1)
    mfcf_model.W = np.append(mfcf_model.W, np.zeros(
        [mfcf_model.W.shape[0], 1], dtype=float), axis=1)
    mfcf_model.d = np.append(mfcf_model.d, np.random.randn(1), axis=0)
    # mfcf_model.updateWdUserU(userId)
    db["model"].find_one_and_update({'name': "W"}, {
                                    '$set': {"value": bson.Binary(pickle.dumps(mfcf_model.W, protocol=2))}})
    db["model"].find_one_and_update(
        {'name': "d"}, {'$set': {"value": mfcf_model.d.tolist()}})
    return jsonify({"status": "success"}), 200
    # except:
    #     return jsonify({"status": "fail"}), 500


@recommender_bp.route("/user/train/", methods=['POST'])
def train_model_for_user():
    data = request.get_json()
    userId = data['userId']
    status = mfcf_model.updateWdUserU(userId)
    if status == False:
        return jsonify({"status": "fail"}), 500
    db["model"].find_one_and_update({'name': "W"}, {
                                    '$set': {"value": bson.Binary(pickle.dumps(mfcf_model.W, protocol=2))}})
    db["model"].find_one_and_update(
        {'name': "d"}, {'$set': {"value": mfcf_model.d.tolist()}})
    return jsonify({"status": "success"}), 200


@recommender_bp.route("/predict/topten/", methods=['POST'])
def recommender_predict_top_ten():
    data = request.get_json(force=True)
    userId = data['userId']
    result = mfcf_model.predTopTen(userId)
    movieCursor = db["movie"].find(
        {"movieId": {"$in": result[0]}}, {'_id': False})
    response = {"movies_data": [], "movies_order": []}
    movies_data = []
    for movie in movieCursor:
        movies_data.append(movie)
    response["movies_data"] = (movies_data)
    movies_order = result[0]
    response["movies_order"] = (movies_order)
    return jsonify(response), 200
