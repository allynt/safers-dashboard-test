from django.utils.translation import gettext_lazy as _

from rest_framework.permissions import BasePermission


class IsUserOrAdmin(BasePermission):
    """
    Allows a user to access themselves.  Allows an admin to access anybody.
    """
    def has_object_permission(self, request, view, obj):
        user = request.user
        return obj == user or user.is_superuser
