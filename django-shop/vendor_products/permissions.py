from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsVendorOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print("IsVendorOwner", obj.vendor.owner == request.user)

        return obj.vendor.owner == request.user


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Authenticated users only can see list view
        # if request.user.is_authenticated:
        #     return True
        # return False
        print("has_permission")
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request so we'll always
        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            print("has_object_permission SAFE_METHODS", True)
            return True
        # Write permissions are only allowed to the author of a post
        print(obj.vendor.owner, request.user, "==", obj.vendor.owner == request.user)
        if request.user.is_authenticated:
            print("has_object_permission ", True)
            return obj.vendor.owner == request.user
        print("has_object_permission ", False)
        return False
