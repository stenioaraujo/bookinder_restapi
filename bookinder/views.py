from django.contrib.auth.models import User, Group
from rest_framework import viewsets

from bookinder import serializers
from bookinder import models


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if (self.request.user.is_superuser):
            return User.objects.all()
        else:
            return User.objects.filter(username=user)


class BookViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        if (self.request.user.is_superuser):
            return models.UserProfile.objects.all()
        else:
            return models.UserProfile.objects.filter(user=user)


class LibraryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LibrarySerializer
    
    def get_queryset(self):
        user = models.UserProfile.objects.filter(user=self.request.user)
        
        if (self.request.user.is_superuser):
            return models.Library.objects.all()
        else:
            return models.Library.objects.filter(user=user)
    


