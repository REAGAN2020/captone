from __future__ import unicode_literals


# Create your tests here.
from django.test import TestCase
from .models import *


class TestProfile(TestCase):
    def setUp(self):
        self.user = User(id=1, username='AokoMercyline',
                         password='@moringa2020')
        self.user.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.user, User))

    def test_save_user(self):
        self.user.save()

    def test_delete_user(self):
        self.user.delete()