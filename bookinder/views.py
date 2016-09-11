from django.contrib.auth.models import User
from rest_framework import permissions as rest_permissions
from rest_framework import viewsets

from bookinder import models
from bookinder import permissions
from bookinder import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsOwnerOrSuperUser,)
    
    
    def get_queryset(self):
        user = self.request.user
        
        if (self.request.user.is_superuser):
            return User.objects.all()
        else:
            return User.objects.filter(username=user)
        


class BookViewSet(viewsets.ModelViewSet):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer
    permission_classes = (rest_permissions.IsAuthenticated,)


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializer
    permission_classes = (permissions.IsOwnerOrSuperUser,)
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

            
    def get_queryset(self):
        user = self.request.user
        
        if (self.request.user.is_superuser):
            return models.UserProfile.objects.all()
        else:
            return models.UserProfile.objects.filter(user=user)


class LibraryViewSet(viewsets.ModelViewSet):
    queryset = models.Library.objects.all()
    serializer_class = serializers.LibrarySerializer
    permission_classes = (permissions.IsOwnerOrSuperUser,)
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
    def get_queryset(self):        
        if (self.request.user.is_superuser):
            return models.Library.objects.all()
        else:
            return models.Library.objects.filter(user=self.request.user)



