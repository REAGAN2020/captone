from django.shortcuts import render,redirect, get_object_or_404
from django.http  import HttpResponse
from .serializers import *
from .models import Profile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
User = get_user_model()
from .permissions import IsCompanyAdmin, IsNormalUser,IsVendor, UserIsOwnerOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import *

# Create your views here.
class UserView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)

class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request,id):
        user = request.user
        try:
            user_profile = get_user_model().objects.get(id=id)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if user_profile != user:
            return Response({'response': "You don't have permission to edit that"})
        if request.method == 'POST':
            
            serializer = ProfileSerializer(data=request.data,context={'request':request})
            data = {}
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class ProfilesView(APIView):
    permission_classes = (IsAuthenticated,IsCompanyAdmin)
    def get(self,request):
        try:
            profiles= Profile.objects.all()
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = ProfileSerializer(profiles, many=True)
            return Response(serializer.data)

class ProfileIdView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        try:
            profile= Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = ProfileSerializer(profile,context={'request':request})
            return Response(serializer.data)

class UpdateProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self,request):
        user = request.user
        try:
            profile= Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'PUT':
            serializer = ProfileSerializer(profile,data=request.data,context={'request':request})
            data = {}
            if serializer.is_valid():
                serializer.save()
                data["success"] = "update sucessful"
                return Response(data=data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST )

class CreateCarView(APIView):
    # permission_classes = (IsAuthenticated,IsCompanyAdmin)
    def post(self,request):
        if request.method == 'POST':
            serializer = CarSerializer(data=request.data)
            data = {}
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class CarAllView(APIView):
    # permission_classes = (IsAuthenticated,IsNormalUser)
    def get(self,request):
        try:
            car_post = Car.objects.all()
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = CarSerializer(car_post, many=True)
            data = {}
            return Response(serializer.data)

class CarIdView(APIView):
    #permission_classes = (IsAuthenticated,IsNormalUser)
    def get(self,request,id):
        try:
            car_post = Car.objects.get(id=id)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = CarSerializer(car_post)
            return Response(serializer.data)

class SmallCarCategoryView(APIView):
    #permission_classes = (IsAuthenticated,IsNormalUser)
    def get(self,request):
        try:
            car_post = Car.objects.filter(car_type='S')
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = CarSerializer(car_post,many=True)
            data = {}
            return Response(serializer.data)

class   MidCarCategoryView(APIView):
    #permission_classes = (IsAuthenticated,IsNormalUser)
    def get(self,request):
        try:
            car_post = Car.objects.filter(car_type='M')
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = CarSerializer(car_post,many=True)
            data = {}
            return Response(serializer.data)

class   LargeCarCategoryView(APIView):
    #permission_classes = (IsAuthenticated,IsNormalUser)
    def get(self,request):
        try:
            car_post = Car.objects.filter(car_type='L')
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = CarSerializer(car_post,many=True)
            data = {}
            return Response(serializer.data)

class   AmbulanceCarCategoryView(APIView):
    #permission_classes = (IsAuthenticated,IsNormalUser)
    def get(self,request):
        try:
            car_post = Car.objects.filter(car_type='A')
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = CarSerializer(car_post,many=True)
            data = {}
            return Response(serializer.data)


class CarDeleteView(APIView):
    #permission_classes = (IsAuthenticated,IsNormalUser)
    def get(self,request,id):
        car = Car.objects.get(id=id)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BookCar(APIView):
    """
    List all Bookings, or Create a booking
    """
    def post(self,request,id):
        user = request.user
        try:
            car_post = Car.objects.get(id=id)
        except Car.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'POST':

            data = request.data.copy()
            data['car'] = car_post.id
            serializer = BookingsSerializer(data=data,context={'request':request})
            # data['car'] = car_post
            data = {}
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserBookingsView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request):
        user = request.user
        try:
            booking= Bookings.objects.get(user=user)
        except Bookings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = BookingsSerializer(booking,context={'request':request})
            return Response(serializer.data)



