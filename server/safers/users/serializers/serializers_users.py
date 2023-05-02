from rest_framework import serializers

from safers.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "status",
            "accepted_terms",
            "change_password",
        )
