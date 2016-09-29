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
    email_facebook = models.CharField(max_length=50, default="", blank=True)
    email_google = models.CharField(max_length=50, default="", blank=True)
    first_time = models.BooleanField(default=True)


class Book(models.Model):
    isbn = models.CharField(max_length=11, primary_key=True)
    paginas = models.IntegerField(default=0)
    autor = models.CharField(max_length=256, default="", blank=True)
    editora = models.CharField(max_length=256, default="", blank=True)
    nome = models.CharField(max_length=256, default="", blank=True)
    img_file_path = models.CharField(max_length=256, default="", blank=True)
    url_img = models.CharField(max_length=256, default="", blank=True)
    res_id = models.IntegerField(default=0)


class Library(models.Model):
    class Meta:
        unique_together = (("user", "book"),)  # Pode ser so a tupla, se for 2
        
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    favorite = models.BooleanField(default=False)
    tradeable = models.BooleanField(default=False)
    blocked = models.BooleanField(default=False)
    liked = models.BooleanField(default=False)
    owned = models.BooleanField(default=False)
    interested = models.BooleanField(default=False)
    read_pages = models.IntegerField(default=0)


class Match(models.Model):
    class Meta:
        # Pode ser so a tupla, se for 2
        unique_together = (("user1", "book1", "user2", "book2"),) 
    
    id = models.CharField(max_length=256, primary_key=True)
    user1 = models.ForeignKey(User, related_name='user1')
    book1 = models.ForeignKey(Book, related_name='book1')
    user2 = models.ForeignKey(User, related_name='user2')
    book2 = models.ForeignKey(Book, related_name='book2')
    accepted = models.BooleanField(default=False)
    user1_accepted = models.BooleanField(default=False)
    user2_accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)
