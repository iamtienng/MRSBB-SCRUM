from flask import Blueprint, request, jsonify

from model.Movie import Movie
from config import db
from security.RegexTools import escapeRegExp

movie_bp = Blueprint('movie_bp', __name__)


@movie_bp.route("/s", methods=['GET'])
def search_movie():
    try:
        query = escapeRegExp(request.args.get('query'))
        if len(query) < 3:
            return "None", 400
        else:
            movieDoc = db['movie'].find({"movieTitle": {'$regex': query, '$options': 'i'}}, {
                                        '_id': False})
            if (movieDoc.count() > 0):
                return list(movieDoc), 200
            return "None", 404
    except:
        return "None", 400


@ movie_bp.route("/d", methods=['GET'])
def get_movie_detail():
    try:
        movie = Movie()
        movie.movieId = int(request.args.get('query'))
        movieDoc = db['movie'].find({"movieId": movie.movieId})
        if (movieDoc.count() > 0):
            movie.get_info_from_db(db, movieDoc[0]['_id'])
            return jsonify(movie.get_info()), 200
        return "None", 404
    except:
        return "None", 400
