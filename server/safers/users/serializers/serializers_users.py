from rest_framework import serializers

from safers.users.models import User, Organization, Role


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "auth_id",
            "email",
            "username",
            "status",
            "accepted_terms",
            "change_password",
            "organization_name",
            "role_name",
            "organization",
            "role",
            "profile",
            "is_citizen",
        )

    auth_id = serializers.UUIDField(
        required=False,
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

    organization = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    role = serializers.SlugRelatedField(
        slug_field="name",
        read_only=True,
    )

    # profile = UserProfileSerializer()

    # def create(self, validated_data):
    #     profile_serializer = self.fields["profile"]
    #     profile_data = validated_data.pop(profile_serializer.source)
    #     instance = User.objects.create(**validated_data)
    #     profile_serializer.update(
    #         instance.profile, dict(user=instance, **profile_data)
    #     )
    #     return instance

    # def update(self, instance, validated_data):
    #     profile_serializer = self.fields["profile"]
    #     profile_data = validated_data.pop(profile_serializer.source)
    #     for field_name, field_value in validated_data.items():
    #         setattr(instance, field_name, field_value)
    #     instance.save()
    #     profile_serializer.update(instance.profile, profile_data)
    #     return instance
