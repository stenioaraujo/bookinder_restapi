from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField()


class Book(models.Model):
    title = models.CharField(max_length=256)
    isbn = models.CharField(max_length=11, primary_key=True)
    pages = models.CharField(max_length=4)


class Library(models.Model):
    user = models.ForeignKey(UserProfile)
    book = models.ForeignKey(Book)
    favorite = models.BooleanField(default=False)
    tradeable = models.BooleanField(default=False)
    pages_read = models.CharField(max_length=4, default=0)
