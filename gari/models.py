from __future__ import unicode_literals
import cloudinary
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
import datetime as dt
from tinymce.models import HTMLField
import numpy as np
from django.contrib.auth import get_user_model
from django import forms
import cloudinary.uploader
from django.db.models import TextField
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
# from pyuploadcare.dj.forms import FileWidget
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# from  .models import UserProfile

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(
        reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )

class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have email address')
        if not username:
            raise ValueError('Users must have username')
        user = self.model(
                email=self.normalize_email(email),
                username=username,
            )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
  
class User(AbstractBaseUser):
    email       = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username    = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name="date-joined", auto_now_add=True)
    last_login   = models.DateTimeField(verbose_name="last-login", auto_now=True)
    is_admin     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyUserManager()
    
    def __str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Car(models.Model):
    car_model = models.CharField(max_length=100)
    car_owner = models.CharField(max_length=100)
    car_number = models.CharField(max_length=100)
    Description = models.TextField()
    submissions_date = models.DateTimeField()


class Services(models.Model):
    image = CloudinaryField('image', null=True)
    description = TextField()
    name = models.CharField(max_length=100)
    prices = models.IntegerField()

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name

    def average_rating(self):
        all_ratings = map(lambda x: x.ratings, self.review_set.all())
        return np.mean(all_ratings)


class Post(models.Model):
    title = models.CharField(max_length=150)
    image = CloudinaryField('image', null=True)
    post = TextField()
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    avatar = CloudinaryField('image', null=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save_profile(self):
        self.user

    def delete_profile(self):
        self.delete()

    @classmethod
    def search_profile(cls, name):
        return cls.objects.filter(user__username__icontains=name).all()


class Comment(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )

    service = models.ForeignKey(Services, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')
    username = models.CharField(max_length=100)
    comment = models.CharField(max_length=200)
    rating = models.IntegerField(choices=RATING_CHOICES)
