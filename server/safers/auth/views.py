import requests
from urllib.parse import urljoin

from django.conf import settings

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiExample

from safers.users.models import User, UserStatus

from safers.auth.clients import AUTH_CLIENT
from safers.auth.permissions import AllowRegistrationPermission, AllowLoginPermission
from safers.auth.serializers import (
    RegisterViewSerializer,
)
from safers.auth.signals import user_registered_signal
from safers.auth.utils import reshape_auth_errors


class RegisterView(GenericAPIView):
    """
    creates a remote user; creates a local user, triggers signal
    """
    permission_classes = [AllowRegistrationPermission]
    serializer_class = RegisterViewSerializer

    @extend_schema(
        request=RegisterViewSerializer,
        responses={status.HTTP_201_CREATED: None},
        examples=[
            OpenApiExample(
                "valid request",
                {
                    "email": "user@example.com",
                    "password": "RandomPassword123",
                    "first_name": "Test",
                    "last_name": "User",
                    "organization": "Test Organization",
                    "role": "organization_manager",
                    "accepted_terms": True,
                }
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        organization = serializer.validated_data.pop("organization")
        role = serializer.validated_data.pop("role")
        accepted_terms = serializer.validated_data.pop("accepted_terms")

        auth_response = AUTH_CLIENT.register({
            "registration": {
                "applicationId": settings.FUSIONAUTH_APPLICATION_ID,
                "roles": [role.name],
            },
            "user": serializer.validated_data,
        })
        if not auth_response.was_successful():
            errors = reshape_auth_errors(auth_response.error_response)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)

        auth_user_data = auth_response.success_response["user"]
        user = User.objects.create(
            auth_id=auth_user_data["id"],
            email=auth_user_data["email"],
            username=auth_user_data.get("username", auth_user_data["email"]),
            role_name=role.name,
            organization_name=organization.name,
            accepted_terms=accepted_terms,
        )

        user_registered_signal.send(
            None,
            instance=user,
            request=request,
        )

        return Response(status=status.HTTP_201_CREATED)
