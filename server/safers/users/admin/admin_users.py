from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from safers.users.models import User


class LocalOrRemoteFilter(admin.SimpleListFilter):
    title = "authentication type"
    parameter_name = "_ignore"  # ignoring parameter_name and computing qs manually

    def lookups(self, request, model_admin):
        return (
            ("_is_local", _("Local")),
            ("_is_remote", _("Remote")),
        )

    def queryset(self, request, qs):
        value = self.value()
        if value:
            qs = qs.filter(**{value: True})
        return qs


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    actions = ()
    add_fieldsets = ((
        None,
        {
            "classes": ("wide", ),
            "fields": (
                "email",
                "password1",
                "password2",
                "accepted_terms",
                "change_password",
                "status",
            ),
        },
    ), )
    fieldsets = (
        (None, {
            "fields": ("id", "auth_id", "email", "username", "password")
        }),
        (_("General info"), {
            "fields": (
                "status",
                "change_password",
            )
        }),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {
            "fields": ("last_login", "date_joined")
        }),  # (
  #     _("Safers"),
  #     {
  #         "fields": ()
  #     }
  # ),
    )
    filter_horizontal = (
        "groups",
        "user_permissions",
        # "favorite_alerts",
        # "favorite_events",
        # "favorite_camera_medias",
    )
    list_display = (
        "email",
        "is_staff",
        "is_active",
        "accepted_terms",
        "status",
        "get_authentication_type_for_list_display",
    )
    list_filter = (
        LocalOrRemoteFilter,
        "status",
    ) + DjangoUserAdmin.list_filter
    readonly_fields = (
        "id",
        "auth_id",
    ) + DjangoUserAdmin.readonly_fields
    search_fields = (
        "email",
        "username",
    )
    ordering = ("email", )

    @admin.display(description="AUTHENTICATION TYPE")
    def get_authentication_type_for_list_display(self, instance):
        if instance.is_local:
            return "local"
        elif instance.is_remote:
            return "remote"
