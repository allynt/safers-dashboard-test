from rest_framework import serializers

from safers.core.models import SafersSettings


class SafersSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SafersSettings
        fields = (
            "allow_signin",
            "allow_signup",
            "allow_password_change",
            "require_terms_acceptance",
            "request_timeout",
        )
