from django.shortcuts import render
from django.http  import HttpResponse
from .serializers import RegistrationSerializer
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .permissions import IsCompanyAdmin, IsNormalUser,IsVendor
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class RegisterView(APIView):
    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "success registration"
            data['email'] = user.email
            data['username'] = user.username
        else:
            data = serializer.errors
            return Response(data,status=status.HTTP_404_NOT_FOUND)
        return Response(data)

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
           
            token = RefreshToken()
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
