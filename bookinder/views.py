from django.contrib.auth.models import User
from rest_framework import permissions as rest_permissions
from rest_framework import viewsets
from url_filter.integrations.drf import DjangoFilterBackend

from bookinder import models
from bookinder import permissions
from bookinder import serializers


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsOwnerOrSuperUser,)
    
    def get_queryset(self):
        user = self.request.user
        
        if self.request.user.is_superuser:
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
        user = self.request.user
        serializer.save(user=user)

    def get_queryset(self):
        user = self.request.user
        
        if self.request.user.is_superuser:
            return models.UserProfile.objects.all()
        else:
            return models.UserProfile.objects.filter(user=user)


class LibraryViewSet(viewsets.ModelViewSet):
    queryset = models.Library.objects.all()
    serializer_class = serializers.LibrarySerializer
    permission_classes = (permissions.IsOwnerOrSuperUser,)
    filter_backends = [DjangoFilterBackend,]
    filter_fields = ["interested", "blocked"]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
    def get_queryset(self):        
        if self.request.user.is_superuser:
            return models.Library.objects.all()
        else:
            return models.Library.objects.filter(user=self.request.user)
            
            
class MatchViewSet(viewsets.ModelViewSet):
    queryset = models.Match.objects.all()
    serializer_class = serializers.MatchSerializer
    permission_classes = (permissions.IsOwnerOrSuperUser,)
    # Fazer o metodo aqui, so permitir admin criar, mas permitir que usuario
    # faca put patch nos outros campos, e que ele possa ler

            
class CreateMatches(viewsets.ModelViewSet):
    serializer_class = serializers.MatchSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    first_time = True

    def get_queryset(self):
        sql = ("SELECT abs(strftime('%s','now') + random()) AS id,"
               " I1.user_id AS user1, I2.book_id AS book1,"
               " I2.user_id AS user2, I1.book_id AS book2 "
               "FROM bookinder_library AS I1, bookinder_library AS O1,"
               " bookinder_library AS I2, bookinder_library AS O2 "
               "WHERE I1.interested AND I2.interested"
               " AND O1.owned AND O2.owned"
               " AND I1.book_id = O1.book_id AND I2.book_id = O2.book_id"
               " AND I1.user_id = O2.user_id"
               " AND O1.user_id = I2.user_id")
        matchset = models.Library.objects.raw(sql)

        self._save_to_match_table(matchset)

        self.first_time = False

        return list(matchset)

    def _save_to_match_table(self, matchset):
        def not_in(match, s):
            tup1 = (match["user1"].id, match["book1"].isbn,
                    match["user2"].id, match["book2"].isbn)
            tup2 = tup1[2:4] + tup1[0:2]

            if (self.first_time
                and tup1 not in s
                and tup2 not in s):
                print(tup1)
                s.add(tup1)
                return True
            else:
                return False

        match_serializer = serializers.MatchSerializer()
        user_objects = models.User.objects
        book_objects = models.Book.objects
        already_inserted = set()
        for match in matchset:
            try:
                new_match = {
                    "id": match.id,
                    "user1": user_objects.get(id=match.user1),
                    "user2": user_objects.get(id=match.user2),
                    "book1": book_objects.get(isbn=match.book1),
                    "book2": book_objects.get(isbn=match.book2)
                }

                if not_in(new_match, already_inserted):
                    match_serializer.create(new_match)
            except Exception:
                pass
