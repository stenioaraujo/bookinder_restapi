from rest_framework import permissions


class IsOwnerOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated() or request.method == "POST":
            return True
        
            
            
    def has_object_permission(self, request, view, obj):
        try:
            return (obj == request.user
                    or obj.user == request.user)
        except:
            return request.user.is_superuser
