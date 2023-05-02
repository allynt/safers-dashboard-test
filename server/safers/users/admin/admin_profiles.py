from django.contrib import admin
from django.urls import resolve

from safers.core.admin import get_clickable_fk_for_list_display, CannotAddModelAdminBase, CannotDeleteModelAdminBase

from safers.users.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(
    CannotAddModelAdminBase,
    # CannotDeleteModelAdminBase,  # (see `has_delete_permission` below)
    admin.ModelAdmin,
):
    list_display = (
        "get_name_for_list_display",
        "get_user_for_list_display",
    )
    search_fields = (
        "user__email",
        "first_name",
        "last_name",
    )

    @admin.display(description="PROFILE")
    def get_name_for_list_display(self, obj):
        return str(obj)

    @admin.display(description="USER")
    def get_user_for_list_display(self, obj):
        return get_clickable_fk_for_list_display(obj.user)

    def has_delete_permission(self, request, obj=None):
        """
        UserProfiles can be deleted in response to deleting a User from
        the UserAdmin.  But not directly from the UserProfileAdmin.
        """
        view_name = resolve(request.path).view_name
        return view_name in [
            "admin:users_user_changelist",
            "admin:users_user_change",
            "admin:users_user_delete",
        ]