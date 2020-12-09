
 
from __future__ import unicode_literals
import cloudinary
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import  User
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
# from  .models import UserProfile


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

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

class Car(models.Model):
    car_model=models.CharField(max_length=100)
    car_owner=models.CharField(max_length=100)
    car_number=models.CharField(max_length=100)
    Description=models.TextField()
    submissions_date=models.DateTimeField()

    
    
   
class Services(models.Model):
    image = CloudinaryField('image', null=True)
    description = TextField()
    name =models.CharField(max_length=100)
    prices=models.IntegerField()
    
    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
    
    def average_rating(self):
        all_ratings = map(lambda x: x.ratings, self.review_set.all())
        return np.mean(all_ratings)
          
