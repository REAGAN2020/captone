from rest_framework.serializers import ModelSerializer
from rest_framework import generics, permissions, serializers, exceptions
from .models import *
from django.contrib.auth.models import User
from . import models
from django.contrib.auth import authenticate
# from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueTogetherValidator

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        # exclude = ["id" ,"password"]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            # password = validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Invalid Details.")


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ('car_model', 'car_owner', 'car_number',
                  'description', 'submissions_date')


class ServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Services
        fields = ('image', 'description', 'name', 'prices')


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'image', 'post', 'username', 'post_date', 'avatar')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('body', 'title', 'name', 'post_date')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('service', 'pub_date', 'username', 'comment', 'rating')
