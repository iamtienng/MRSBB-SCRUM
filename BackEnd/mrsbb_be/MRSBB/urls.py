from django.urls import path

from .views import delete_rating, update_rating, create_wt_d_for_user, create_rating, get_movie_detail, read_rating, pred_top_ten, search_movie, pred, train_model_for_user

urlpatterns = [
    path('cr', create_rating),
    path('rr', read_rating),
    path('ur', update_rating),
    path('dr', delete_rating),
    path('s', search_movie),
    path('d', get_movie_detail),
    path('p', pred),
    path('train-user-model', train_model_for_user),
    path('create-new-user-model', create_wt_d_for_user),
    path('pred-top-ten', pred_top_ten),
]
