from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    """
    Only allow owners to view/edit their tasks.
    """
    def has_object_permission(self, request, view, obj):
        return getattr(obj, 'user_id', None) == getattr(request.user, 'id', None)
