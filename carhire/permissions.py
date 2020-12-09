from rest_framework.permissions import BasePermission

from django.contrib.auth import get_user_model
User = get_user_model()


class IsCompanyAdmin(BasePermission):
    
  
    def has_permission(self, request, view):
        """ check if the object has permission """

        role = request.user.role
        if role == 'CA':
            return True
        else:
            
            return False

class IsNormalUser(BasePermission):


    def has_permission(self, request, view):
        """ check if the object has permission """

        role = request.user.role
        if role == 'NU':
            return True
        else:
            
            return False

class IsVendor(BasePermission):


    def has_permission(self, request, view):
        """ check if the object has permission """

        role = request.user.role
        if role == 'V':
            return True
        else:
            return False

class UserIsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id