from rest_framework import permissions

SAFE_METHODS = ['GET', 'PUT']

class IsAdminOrReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_superuser:
            return True
        else:
            return False

class IsUserOrReadOnly(permissions.BasePermission):    

    def has_object_permission(self, request, view, obj):
        
        return obj.user == request.user