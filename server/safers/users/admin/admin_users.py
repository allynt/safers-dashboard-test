from django.contrib import admin
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm as DjangoUserAdminForm
from django.utils.translation import gettext_lazy as _

from safers.core.widgets import DataListWidget, JSONWidget
from safers.users.models import User, Organization, Role

############
# filters #
############


class LocalOrRemoteFilter(admin.SimpleListFilter):
    title = "authentication type"
    parameter_name = "_ignore"  # ignoring parameter_name and computing qs manually

    def lookups(self, request, model_admin):
        return (
            # notice this uses the calculated fields from the custom UserManager
            ("_is_local", _("Local")),
            ("_is_remote", _("Remote")),
        )

    def queryset(self, request, qs):
        value = self.value()
        if value:
            qs = qs.filter(**{value: True})
        return qs


#########
# forms #
#########


class UserAdminForm(DjangoUserAdminForm):
    """
    Custom form w/ some pretty fields; formats the profile
    and lets me choose from valid Organizations & Roles
    """
    class Meta:
        model = User
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["organization_name"].help_text = _(
            "The name of the organization this user belongs to."
        )
        self.fields["organization_name"].widget = DataListWidget(
            name="organization_name",
            options=[
                organization.name for organization in Organization.objects.all()
            ],
        )
        self.fields["role_name"].help_text = _(
            "The name of the role this user belongs to."
        )
        self.fields["role_name"].widget = DataListWidget(
            name="role_name",
            options=[role.name for role in Role.objects.all()],
        )
        self.fields["profile"].widget = JSONWidget()


##########
# admins #
##########
@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    model = User
    form = UserAdminForm
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
                "classes": ("collapse", ),
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"), {
                "classes": ("collapse", ),
                "fields": ("last_login", "date_joined")
            }
        ),
        (
            _("Safers"), {
                "fields": (
                    "organization_name",
                    "role_name",
                    "profile",
                )
            }
        ),
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
        "organization_name",
        "role_name",
    )
    list_filter = (
        LocalOrRemoteFilter,
        "status",
        "organization_name",
        "role_name",
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
    def get_authentication_type_for_list_display(self, instance) -> str:
        authentication_type = "unknown"
        if instance.is_local:
            authentication_type = "local"
        elif instance.is_remote:
            authentication_type = "remote"
        return authentication_type
