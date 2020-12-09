from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User, AbstractUser
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile', blank=True)
    name = models.CharField(max_length=80, blank=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = CloudinaryField('image')


    def __str__(self):
            return f'{self.user.username} profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
            if created:
                Profile.objects.create(user=instance)
    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
            instance.profile.save()

class Car(models.Model):

    CHOICES = (
        ('Manual','M'),
        ( 'Auto', 'A'),
        
    )
    CHOICES2 = (
        ('Petrol', 'P'),
        ('Diesel', 'D'),
        
    )
    CHOICES3 = (
        ('S', 'Sports Car'),
        ('M', 'Mid-size Vehicle'), 
        ('L', 'Large Vehicle'),
        ('A', 'Ambulance'),  
        
    ) 
    name = models.CharField(max_length=100)
    image = CloudinaryField('image')
    seats = models.TextField(null=True)
    doors = models.TextField(null=True)
    transmission = models.CharField(max_length=300, choices = CHOICES,null=True)
    fuel = models.CharField(max_length=300, choices = CHOICES2,null=True)
    car_type = models.CharField(max_length=300, choices = CHOICES3,null=True)
    daily_rent = models.IntegerField()
    is_available = models.BooleanField()

    def get_absolute_url(self):
        return reverse('car-details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Bookings(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookedcar', blank=True,null=True, unique=False)
    user = models.ForeignKey( settings.AUTH_USER_MODEL,  on_delete=models.CASCADE, related_name='client', blank=True, null=True, unique=False)
    startdate = models.DateField(verbose_name=('Start Date'),help_text='Borrowed is on ..',null=True,blank=False)
    returndate = models.DateField(verbose_name=('Return Date'),help_text='will be returned on ...',null=True,blank=False)
    cell_no = models.CharField(max_length=15)
    address = models.TextField()

