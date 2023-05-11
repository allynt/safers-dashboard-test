import logging
import requests
from urllib.parse import urljoin, urlencode

from django.conf import settings
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema, OpenApiExample

from safers.core.authentication import TokenAuthentication
from safers.core.clients import GATEWAY_CLIENT

from safers.users.models import User, UserProfile, UserStatus
from safers.users.serializers import UserSerializer, UserCreateSerializer
from safers.users.utils import reshape_profile_data, ProfileDirection

from safers.auth.clients import AUTH_CLIENT
from safers.auth.permissions import AllowRegistrationPermission, AllowLoginPermission
from safers.auth.serializers import (
    RegisterViewSerializer,
    AuthenticateViewSerializer,
)
from safers.auth.signals import user_registered_signal
from safers.auth.utils import reshape_auth_errors

logger = logging.getLogger(__name__)


class RegisterView(GenericAPIView):
    """
    Registers a user w/ FusionAuth.  Creates a corresponding local
    dashboard user.  Updates the corresponding remote gateway user.
    """
    permission_classes = [AllowRegistrationPermission]
    serializer_class = RegisterViewSerializer

    @transaction.atomic
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

        # validate request parameters...
        serializer = self.get_serializer(
            data=request.data,
            context={
                # copy email to username
                "username": request.data.get("email"),
            }
        )
        serializer.is_valid(raise_exception=True)

        organization = serializer.validated_data.pop("organization")
        team = None
        role = serializer.validated_data.pop("role")
        accepted_terms = serializer.validated_data.pop("accepted_terms")

        # register w/ FusionAuth...
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
        auth_token = auth_response.success_response["token"]

        # create local user...
        user = User.objects.create(
            auth_id=auth_user_data["id"],
            organization_name=organization.name if organization else None,
            role_name=role.name if role else None,
            email=auth_user_data["email"],
            username=auth_user_data["username"],
            accepted_terms=accepted_terms,
        )
        user.save()
        # (using get_or_create instead of just user.profile in case of race conditions w/ User PostSaveSignal)
        user_profile, _ = UserProfile.objects.get_or_create(user=user)
        user_profile.first_name = auth_user_data["firstName"]
        user_profile.last_name = auth_user_data["lastName"]
        user_profile.save()

        # user_serializer = UserCreateSerializer(
        #     data=dict(
        #         accepted_terms=accepted_terms,
        #         **(
        #             reshape_profile_data(
        #                 remote_profile_data,
        #                 direction=ProfileDirection.REMOTE_TO_LOCAL,
        #             )
        #         )
        #     )
        # )
        # user_serializer.is_valid(raise_exception=True)
        # user = user_serializer.save()

        # update remote user...
        # TODO: I WOULD PREFER TO DO THIS IN AuthenticateView BELOW,
        # TODO: BUT I'M THINKING EDGE CASES WHERE AFTER RegisterView
        # TODO: THE USER LOGS INTO SOME OTHER SAFERS CLIENT (LIKE THE
        # TODO: CHATBOT) BEFORE ACTUALLY LOGGING INTO THE DASHBOARD.
        try:
            auth = TokenAuthentication(auth_token)
            remote_profile_data = {
                k: v
                for k, v in GATEWAY_CLIENT.get_profile(auth=auth)["profile"].items()
                if k in [
                    "user",
                    "organizationId",
                    "teamId",
                    "personId",
                    "isFirstLogin",
                    "isNewUser",
                    "taxCode",
                ]
            }  # yapf: disable
            remote_profile_data = GATEWAY_CLIENT.update_profile(
                auth=auth,
                data=dict(
                    organizationId=organization.id if organization else None,
                    teamId=team.id if team else None,
                    **remote_profile_data
                )
            )
        except Exception as e:
            raise APIException(e) from e

        # signal the registration...
        user_registered_signal.send(
            None,
            instance=user,
            request=request,
        )

        return Response(status=status.HTTP_201_CREATED)


class AuthenticateView(GenericAPIView):
    """
    The 2nd part of the "authorization code grant".  Takes an authorization
    code from FusionAuth and returns an access_token for safers-dashboard.
    Creates/updates a local user as needed.
    """
    authentication_classes = []
    permission_classes = [AllowLoginPermission]
    serializer_class = AuthenticateViewSerializer

    @extend_schema(
        request=AuthenticateViewSerializer,
        responses={status.HTTP_200_OK: None},  # TODO: REPLACE W/ REAL CONTENT
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # TODO: MODIFY THIS TO COPE W/ SWAGGER ?
        redirect_uri = settings.FUSIONAUTH_REDIRECT_URL

        # get token...
        auth_token_response = AUTH_CLIENT.exchange_o_auth_code_for_access_token(
            code=serializer.validated_data["code"],
            redirect_uri=redirect_uri,
            client_id=settings.FUSIONAUTH_CLIENT_ID,
            client_secret=settings.FUSIONAUTH_CLIENT_SECRET,
        )
        if not auth_token_response.was_successful():
            errors = reshape_auth_errors(auth_token_response.error_response)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        auth_token_data = auth_token_response.success_response

        # use token to get user details...
        auth_user_response = AUTH_CLIENT.retrieve_user(
            auth_token_data["userId"]
        )
        if not auth_user_response.was_successful():
            errors = reshape_auth_errors(auth_user_response.error_response)
            return Response(errors, status=status.HTTP_400_BAD_REQUEST)
        auth_user_data = auth_user_response.success_response["user"]

        # get/create the corresponding local user...
        user, created = User.objects.get_or_create(
            auth_id=auth_token_data["userId"],
            defaults={
                "email": auth_user_data["email"],
                "username": auth_user_data["username"],
            }
        )

        # update user as needed...
        if user.status == UserStatus.PENDING:
            auth = TokenAuthentication(auth_token_data["access_token"])
            if created:
                # user was not yet created in the dashboard...
                # (therefore get remote details and save locally)
                remote_profile_data = GATEWAY_CLIENT.get_profile(auth=auth)
                UserCreateSerializer().update(
                    user,
                    reshape_profile_data(
                        remote_profile_data,
                        direction=ProfileDirection.REMOTE_TO_LOCAL,
                    )
                )
            else:
                # user was already created in the dashboard...
                # (therefore get local details and save remotely)
                logger.info(
                    "user already created - waiting to update remote user until PATCH is implemented"
                )
                # local_profile_data = UserSerializer(instance=user).data
                # GATEWAY_CLIENT.update_profile(
                #     auth=auth,
                #     data=reshape_profile_data(
                #         local_profile_data,
                #         direction=ProfileDirection.LOCAL_TO_REMOTE,
                #     )
                # )

            user.status = UserStatus.COMPLETED

        user.last_login = timezone.now()
        user.save()

        # check if the user satisfies all the login requirements...
        # (such as is_active)
        # TODO:

        data = {
            "access_token": auth_token_data["access_token"],
            # "refresh_token": auth_token_data["refresh_token"],
            "expires_in": auth_token_data["expires_in"],
            "user_id": user.id,
        }
        return Response(
            data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


# TODO: REFRESH

# TODO: LOGOUT

#################
# Django Views #
#################


def login_view(request):
    """"
    Login via FusionAuth. (This is a normal Django view as opposed to
    a DRF view.)
    """
    AUTHENTICATION_CODE_GRANT_PATH = "oauth2/authorize"

    base_auth_url = urljoin(
        settings.FUSIONAUTH_EXTERNAL_URL, AUTHENTICATION_CODE_GRANT_PATH
    )
    auth_url_params = urlencode({
        "client_id": settings.FUSIONAUTH_CLIENT_ID,
        "redirect_uri": settings.FUSIONAUTH_REDIRECT_URL,
        "tenant_id": settings.FUSIONAUTH_TENANT_ID,
        "response_type": "code",
        "scope": "offline_access",
    })
    auth_url = f"{base_auth_url}?{auth_url_params}"

    response = redirect(auth_url)
    return response


def callback_view(request):
    """
    This simple callback acts as a pretend callback.  It is used for
    development only.  It just passes on the code (or the error) returned
    by FusionAuth login ot the AuthenticateView above.  Manually copying
    the code into the AuthenticateView via swagger cannot be done before
    the code expires.
    """
    data = request.GET
    logger.info(data)

    authenticate_response = requests.post(
        request.build_absolute_uri(reverse("auth-authenticate")),
        data=data,
        timeout=4,
    )
    return JsonResponse(
        authenticate_response.json(), authenticate_response.status
    )
