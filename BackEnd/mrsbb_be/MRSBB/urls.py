from django.urls import path

from .views import get_api

urlpatterns = [
    path('hello', get_api),
]
