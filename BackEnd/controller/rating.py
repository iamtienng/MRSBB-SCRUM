from flask import Blueprint, jsonify, request

from model.Rating import Rating
from config import db


rating_bp = Blueprint('rating_bp', __name__)


@rating_bp.route("/create/", methods=['POST'])
def create_rating():
    data = request.get_json(force=True)
    rating = Rating(data['userId'], data['movieId'])
    if (rating.create(db, data['rating'])):
        return jsonify(rating.get_info()), 200
    return {'status': 'failed'}, 400


@rating_bp.route("/read/", methods=['POST'])
def read_rating():
    data = request.get_json(force=True)
    if len(data) < 2:
        return {'status': 'failed'}, 401
    rating = Rating(data['userId'], data['movieId'])
    if (rating.get_info_from_db(db)):
        return jsonify(rating.get_info()), 200
    return {'status': 'failed'}, 400


@ rating_bp.route("/update/", methods=['PUT'])
def update_rating():
    data = request.get_json(force=True)
    rating = Rating(data['userId'], data['movieId'])
    if (rating.update(db, data['rating'])):
        return {'status': 'updated'}, 200
    return {'status': 'failed'}, 400


@ rating_bp.route("/delete/", methods=['DELETE'])
def delete_rating():
    data = request.get_json(force=True)
    rating = Rating(data['userId'], data['movieId'])
    if (rating.delete(db)):
        return {'status': 'deleted'}, 200
    return {'status': 'failed'}, 400
