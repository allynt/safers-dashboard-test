from rest_framework import serializers

from safers.users.models import User
from safers.users.serializers import UserProfileSerializer


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
            "organization",
            "role",
            "profile",
        )

    profile = UserProfileSerializer()