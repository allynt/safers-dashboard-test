"""
All the serializers used for the auth views.  Note that these are _not_
ModelSerializers; They are used for validation of request data only. 
Interacting with the underlying models is not done by DRF but by proxying
the requests to the actual FusionAuth endpoints.
"""

from django.contrib.auth.password_validation import validate_password as django_validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from drf_spectacular.utils import extend_schema_serializer

from safers.core.models import SafersSettings

from safers.users.models import User, Organization, Role


def validate_password(validated_data):
    if "password_confirmation" in validated_data:
        if validated_data["password"] != validated_data["password_confirmation"]:
            raise ValidationError({
                "password_confirmation": "Passwords must match."
            })

    try:
        django_validate_password(
            validated_data["password"],
            user=User(email=validated_data.get("email")),
        )
    except DjangoValidationError as exception:
        raise ValidationError({"password": exception.messages}) from exception


@extend_schema_serializer(exclude_fields=["organization", "role"])
class RegisterViewSerializer(serializers.Serializer):

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(style={"input_type": "password"})

    first_name = serializers.CharField(required=False, source="firstName")

    last_name = serializers.CharField(required=False, source="lastName")

    organization = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Organization.objects.all(),
        required=False,
        allow_null=True,
    )

    role = serializers.SlugRelatedField(
        slug_field="name",
        queryset=Role.objects.all(),
        required=True,
    )

    accepted_terms = serializers.BooleanField()

    def validate_accepted_terms(self, value):
        safers_settings = SafersSettings.load()
        if safers_settings.require_terms_acceptance and not value:
            raise ValidationError("Terms must be accepted.")
        return value

    def validate(self, data):
        validated_data = super().validate(data)

        # make sure password conforms to the rules specified in AUTH_PASSWORD_VALIDATORS
        validate_password(validated_data)

        # make sure organization & role are compatible
        organization = validated_data.get("organization")
        role = validated_data.get("role")
        if organization and role.is_citizen:
            raise ValidationError(
                "A citizen must not belong to an organization."
            )

        return validated_data
