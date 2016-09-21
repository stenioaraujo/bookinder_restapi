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
        fields = ('isbn', 'nome', 'autor', 'paginas', 'editora', 'url_img', \
                  'img_file_path', 'res_id')
        

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = models.UserProfile
        fields = ('id', 'user', 'email_facebook', 'email_google', \
                  'first_time')
        read_only_fields = ('user',)


class LibrarySerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = models.Library
        fields = ('id', 'user', 'book', 'favorite', 'tradeable', 'read_pages')
        read_only_fields = ('user',)


class PreferenciaLivroSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = models.PreferenciaLivro
        fields = ('id', 'user', 'book', 'blocked', 'liked', \
                  'owned', 'interested')
        read_only_fields = ('user',)