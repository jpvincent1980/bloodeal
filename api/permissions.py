from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAnonymous(BasePermission):
    """
    Custom permission to allow anonymous users to retrieve data lists.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return False


class IsRequester(BasePermission):
    """
    Custom permission to allow users to update data they requested.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.requested_by == request.user


class IsUser(BasePermission):
    """
    Custom permission to allow users to update their favorites.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
