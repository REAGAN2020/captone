from __future__ import unicode_literals
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User, AbstractUser
from django.db.models import Q
from rest_framework.decorators import api_view
from .serializers import *
from knox.models import AuthToken
from rest_framework.response import Response
from rest_framework import generics, permissions, status, viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.sites.shortcuts import get_current_site
from .utils import Util
from .models import *
from .forms import *
from django.http import HttpResponseRedirect, HttpResponse
from csv import DictReader
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.generics import GenericAPIView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.views import APIView
from .permissions import IsAdminOrReadOnly
from django.urls import reverse_lazy, reverse, path, include
from django.contrib.auth.decorators import login_required
from django.conf import settings
from . import views
from knox import views as knox_views
from tinymce.models import HTMLField
DATETIME_FORMAT = '%m/%d/%Y %H:%M'


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        context = {
            "user": serializer.data,
            "token": AuthToken.objects.create(user)[1]
        }
        return Response(context)
    


class ServicesList(APIView):
    def get(self, request, format=None, *args, **kwargs):
        all_services = Services.objects.all()
        serializers = ServicesSerializer(all_services, many=True)
        context = {
            "service": serializers.data
        }
        return Response(context)

    def post(self, request, format=None, *args, **kwargs):

        serializers = ServicesSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            context = {
                "service": serializers.data,
                "status": status.HTTP_201_CREATED
            }
            return Response(context)

        context = {
            "service": serializers.errors,
            "status": status.HTTP_400_BAD_REQUEST
        }
        return Response(context)


def ServicesViewSet(GenericViewSet, CreateModelMixin,  RetrieveModelMixin, UpdateModelMixin, ListModelMixin):
    serializer_class = ServicesSerializer
    queryset = Services.object.all


# Create your views here.
class UserProfileAPI(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['user_id'])
        profile_serializer = UserProfileSerializer(UserProfile)

        return Response(profile_serializer.data)

    def create(self, validated_data):

        user = models.UserProfile(


            email=validated_data['email'],
            name=validated_data['name']

        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(viewsets.ModelViewSet):
    # api endpoint that allows users to be viewed or edited
    queryset = User.objects.all().order_by()
    serializer_class = UserSerializer


class UserAPI(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = serializer.data
        # user = request.user
        context = {
            "user": serializer.data,
            "status": status.HTTP_201_CREATED,
            "token": AuthToken.objects.create(user)[1]
        }
        return Response(context)
       

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentList(APIView):
    def get(self, request, format=None):
        all_comment = Comment.objects.all()
        serializers = CommentSerializer(all_comment, many=True)
        return Response(serializers.data)


class PostList(APIView):
    def get(self, request, format=None):
        all_posts = Post.objects.all()
        serializers = PostSerializer(all_posts, many=True)
        return Response(serializers.data)
