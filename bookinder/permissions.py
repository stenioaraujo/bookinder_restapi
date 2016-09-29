from rest_framework import permissions


class IsOwnerOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated() or request.method == "POST":
            return True
            
    def has_object_permission(self, request, view, obj):
        def same(att = None):
            if att is None:
                return obj == request.user
            else:
                return hasattr(obj, att) and getattr(obj, att) == request.user

        allowed = (request.user.is_superuser
                   or same() or same("user") or same("user2"))

        return allowed

 
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser or request.method == "GET":
            return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.method == "GET"
