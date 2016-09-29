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
        fields = ('isbn', 'nome', 'autor', 'paginas', 'editora', 'url_img',
                  'img_file_path', 'res_id')
        

class UserProfileSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = models.UserProfile
        fields = ('id', 'user', 'email_facebook', 'email_google',
                  'first_time')
        read_only_fields = ('user',)


class LibrarySerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = models.Library
        fields = ('id', 'user', 'book', 'blocked', 'liked',
                  'owned', 'interested', 'favorite', 'tradeable', 'read_pages')
        read_only_fields = ('user',)


class MatchSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = models.Match
        fields = ('id', 'user1', 'book1', 'user2', 'book2',
                  'accepted', 'user1_accepted', 'user2_accepted','rejected')

    def create(self, validated_data):
        user1 = validated_data.get('user1', None)
        user2 = validated_data.get('user2', None)
        instance = self.Meta.model(**validated_data)
        if user1 == user2:
            raise serializers.ValidationError(("User_tem needs to be"
                                               " different than User_quer."))
        instance.save()
        return instance

    def update(self, instance, validated_data):        
        user1 = validated_data.get('user1', None)
        print(user1)
        user2 = validated_data.get('user2', None)
        if user1 == user2:
            raise serializers.ValidationError(("User_tem needs to be"
                                               " different than User_quer."))
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        user1_accepted = validated_data.get('user1_accepted')
        user2_accepted = validated_data.get('user2_accepted')
        decided = user1_accepted and user2_accepted

        setattr(instance, "accepted", decided)

        instance.save()
        return instance
