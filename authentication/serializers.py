from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
User = get_user_model()
