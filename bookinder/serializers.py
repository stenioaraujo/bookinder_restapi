from django.contrib.auth.models import User, Group
from rest_framework import serializers

from bookinder import models


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name',\
                  'last_name', 'email')
        read_only_fields = ('is_staff', 'is_superuser')
        write_only_fields = ('password',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Book
        fields = ('isbn', 'title', 'pages')
        

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = models.UserProfile
        fields = ('id', 'age', 'user')
        read_only_fields = ('user',)


class LibrarySerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = models.Library
        fields = ('id', 'user', 'book', 'favorite', 'tradeable', 'pages_read')
        read_only_fields = ('user',)