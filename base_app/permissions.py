from rest_framework.permissions import BasePermission


class IsBoss(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='boss'):
            return True
        return False


class IsLabeler(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='labeler'):
            return True
        return False


class IsUploader(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.groups.filter(name='uploader'):
            return True
        return False
