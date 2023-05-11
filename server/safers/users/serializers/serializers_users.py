from rest_framework import serializers

from safers.users.models import User, Organization, Role
from safers.users.serializers import UserProfileSerializer  #, OrganizationSerializer, RoleSerializer


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
            "is_citizen",
        )

    organization = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    role = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    profile = UserProfileSerializer()

    def create(self, validated_data):
        profile_serializer = self.fields["profile"]
        profile_data = validated_data.pop(profile_serializer.source)
        instance = User.objects.create(**validated_data)
        # TODO: POSSIBLE RACE CONDITION IN CASE SIGNAL HASN'T COMPLETED YET
        profile_serializer.update(
            instance.profile, dict(user=instance, **profile_data)
        )
        return instance

    def update(self, instance, validated_data):
        profile_serializer = self.fields["profile"]
        profile_data = validated_data.pop(profile_serializer.source)
        for field_name, field_value in validated_data.items():
            setattr(instance, field_name, field_value)
        instance.save()
        profile_serializer.update(instance.profile, profile_data)
        return instance


class UserCreateSerializer(UserSerializer):
    # TODO: DO I REALLY NEED A SEPARATE SERIALIZER IF THESE ARE write_only FIELDS ?
    """
    Includes fields that should not be changed (and are not needed)
    after the initial user creation.
    """
    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + (
            "auth_id",
            "organization_name",
            "role_name",
        )

    auth_id = serializers.UUIDField(
        required=True,
        write_only=True,
    )

    organization_name = serializers.CharField(
        required=False,
        write_only=True,
    )

    role_name = serializers.CharField(
        required=False,
        write_only=True,
    )
