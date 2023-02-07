from dataclasses import field
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
User = get_user_model


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'name', 'password', 'gender', 'birth_date')


class MovieSerializer(serializers.Serializer):
    movieId = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    genres = serializers.CharField(max_length=255)
    posterUrl = serializers.CharField(max_length=255)


class RatingSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    userId = serializers.IntegerField()
    movieId = serializers.IntegerField()
    rating = serializers.IntegerField()
    timestamp = serializers.CharField(max_length=255)
