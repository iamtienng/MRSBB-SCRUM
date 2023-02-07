from turtle import update
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Case, When
import numpy as np
import json
from MRSBB.serializers import RatingSerializer
from MRSBB.serializers import MovieSerializer
from MRSBB.models import UserAccount
from MRSBB.models import Movie
from MRSBB.models import Rating
from MRSBB.models import XModels
from MRSBB.models import WTModels
from MRSBB.models import bModels
from MRSBB.models import dModels
from MRSBB.mfcf import MatrixFactorization


# Create your views here.
@csrf_exempt
def search_movie(request):
    if request.method == 'GET':
        try:
            query = request.GET.get("query")
            if len(query) > 2:
                qs = Movie.objects.all()
                qs = qs.filter(title__icontains=query)
                data = MovieSerializer(qs, many=True).data
                response = json.dumps(data)
            else:
                response = None

        except:
            response = None
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def create_wt_d_for_user(request):
    if request.method == 'POST':
        try:
            # get userID from request
            body = json.loads(request.body.decode('utf-8'))
            userID = int(body.get('userID'))

            user = UserAccount.objects.get(id=userID)
            user.create_wt_d_for_user()

            response = json.dumps({'status': 'success'})

        except:
            response = json.dumps({'status': 'fail'})
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def train_model_for_user(request):
    if request.method == 'POST':
        try:
            # get userID from request
            body = json.loads(request.body.decode('utf-8'))
            userID = int(body.get('userID'))

            user = UserAccount.objects.get(id=userID)
            user.train_wt_d_for_user()

            response = json.dumps({'status': "trained"})

        except:
            response = json.dumps({'status': 'failed'})

    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def get_movie_detail(request):
    if request.method == 'GET':
        try:
            movieId = request.GET.get("query")
            movie = Movie.objects.get(movieId=movieId)
            data = MovieSerializer(movie, many=False).data
            response = json.dumps(data)

        except:
            response = None
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def create_rating(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            userId = int(body.get('userId'))
            movieId = int(body.get('movieId'))
            rating = int(body.get('rating'))
            newRating = Rating(userId=userId, movieId=movieId, rating=rating)
            newRating.save()
            response = json.dumps({'status': "created"})

        except:
            response = json.dumps({'status': 'failed'})
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def read_rating(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body.decode('utf-8'))
            userId = int(body.get('userId'))
            movieId = int(body.get('movieId'))
            existRating = Rating.objects.filter(
                userId=userId, movieId=movieId)[0]
            data = RatingSerializer(existRating, many=False).data
            response = json.dumps(data)

        except:
            response = None
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def update_rating(request):
    if request.method == 'PUT':
        try:
            body = json.loads(request.body.decode('utf-8'))
            ratingId = int(body.get('ratingId'))
            newRating = int(body.get('newRating'))
            existRating = Rating.objects.get(id=ratingId)
            existRating.rating = newRating
            existRating.save()
            response = json.dumps({'status': "changed"})

        except:
            response = json.dumps({'status': 'failed'})
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def delete_rating(request):
    if request.method == 'DELETE':
        try:
            body = json.loads(request.body.decode('utf-8'))
            ratingId = int(body.get('ratingId'))
            existRating = Rating.objects.get(id=ratingId)
            existRating.delete()
            response = json.dumps({'status': "deleted"})

        except:
            response = json.dumps({'status': 'failed'})
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def pred_top_ten(request):
    if request.method == 'POST':
        try:
            # get userID from request
            body = json.loads(request.body.decode('utf-8'))
            userID = int(body.get('userID'))

            ratingObjs = Rating.objects.all()
            ratings_matrix = np.asmatrix(
                ratingObjs.values_list('userId', 'movieId', 'rating'))
            XObjs = XModels.objects.all()
            X = np.asarray(XObjs.values_list('e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14', 'e15', 'e16', 'e17', 'e18', 'e19', 'e20', 'e21', 'e22', 'e23', 'e24',
                                             'e25', 'e26', 'e27', 'e28', 'e29', 'e30', 'e31', 'e32', 'e33', 'e34', 'e35', 'e36', 'e37', 'e38', 'e39', 'e40', 'e41', 'e42', 'e43', 'e44', 'e45', 'e46', 'e47', 'e48', 'e49', 'e50'))
            WTobjs = WTModels.objects.all()
            WT = np.asarray(WTobjs.values_list('e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14', 'e15', 'e16', 'e17', 'e18', 'e19', 'e20', 'e21', 'e22', 'e23',
                                               'e24', 'e25', 'e26', 'e27', 'e28', 'e29', 'e30', 'e31', 'e32', 'e33', 'e34', 'e35', 'e36', 'e37', 'e38', 'e39', 'e40', 'e41', 'e42', 'e43', 'e44', 'e45', 'e46', 'e47', 'e48', 'e49', 'e50'))
            W = WT.T
            bObjs = bModels.objects.all()
            b = np.asarray(bObjs.values_list('e1'))
            dObjs = dModels.objects.all()
            d = np.asarray(dObjs.values_list('e1'))

            mfcf_model = MatrixFactorization(Y=ratings_matrix, K=50, lam=.01, Xinit=X,
                                             Winit=W, bInit=b, dInit=d, learning_rate=50)
            mfcf_model.b = mfcf_model.b.reshape(mfcf_model.b.shape[0], )
            mfcf_model.d = mfcf_model.d.reshape(mfcf_model.d.shape[0], )

            result = mfcf_model.predTopTen(userID)
            queryset = Movie.objects.filter(movieId__in=result[0])
            movies_data = {
                "movies_data": MovieSerializer(queryset, many=True).data
            }
            movies_order = {
                "movies_order": result[0]
            }
            jsonMerged = {**movies_data, **movies_order}
            response = json.dumps(jsonMerged)

        except:
            response = json.dumps({'status': 'failed'})

    return HttpResponse(response, content_type='application/json')


@ csrf_exempt
def pred(request):
    if request.method == 'GET':
        try:
            XObjs = XModels.objects.all()
            WTobjs = WTModels.objects.all()
            bObjs = bModels.objects.all()
            dObjs = dModels.objects.all()

            X = np.asmatrix(XObjs.values_list('e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14', 'e15', 'e16', 'e17', 'e18', 'e19', 'e20', 'e21', 'e22', 'e23', 'e24',
                            'e25', 'e26', 'e27', 'e28', 'e29', 'e30', 'e31', 'e32', 'e33', 'e34', 'e35', 'e36', 'e37', 'e38', 'e39', 'e40', 'e41', 'e42', 'e43', 'e44', 'e45', 'e46', 'e47', 'e48', 'e49', 'e50'))
            WT = np.asmatrix(WTobjs.values_list('e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14', 'e15', 'e16', 'e17', 'e18', 'e19', 'e20', 'e21', 'e22', 'e23',
                                                'e24', 'e25', 'e26', 'e27', 'e28', 'e29', 'e30', 'e31', 'e32', 'e33', 'e34', 'e35', 'e36', 'e37', 'e38', 'e39', 'e40', 'e41', 'e42', 'e43', 'e44', 'e45', 'e46', 'e47', 'e48', 'e49', 'e50'))
            W = WT.T
            b = np.asarray(bObjs.values_list('e1'))
            d = np.asarray(dObjs.values_list('e1'))

            pred = X[5, :].dot(W[:, 5]) + b[5] + d[5]
            print(pred[0][0])
            response = pred

        except:
            response = None
    return HttpResponse(response, content_type='application/json')
