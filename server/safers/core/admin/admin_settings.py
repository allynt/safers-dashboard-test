from django.contrib import admin

from safers.core.models import SafersSettings


@admin.register(SafersSettings)
class OrbisonSettingsAdmin(admin.ModelAdmin):
    fields = (
        "allow_signin",
        "allow_signup",
        "allow_password_change",
        "require_terms_acceptance",
        "allow_logout_via_get",
        "request_timeout",
    )