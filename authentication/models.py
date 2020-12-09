from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class User(AbstractUser):
    USER_ROLES = (
        ('CA', 'COMPANY ADMIN'),
        ('NU', 'NORMAL USER'),
        ('V', 'VENDOR')
    )
  