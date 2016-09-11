from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
            

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField()


class Book(models.Model):
    title = models.CharField(max_length=256)
    isbn = models.CharField(max_length=11, primary_key=True)
    pages = models.CharField(max_length=4)


class Library(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    favorite = models.BooleanField(default=False)
    tradeable = models.BooleanField(default=False)
    pages_read = models.CharField(max_length=4, default=0)
