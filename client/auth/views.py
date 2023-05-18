import logging
import requests
from urllib.parse import urljoin, urlencode

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = None  # don't close request connections during development


def login_view(request):

    CODE_GRANT_PATH = "oauth2/authorize"

    redirect_uri = request.build_absolute_uri(reverse("callback"))

    base_auth_url = urljoin(settings.FUSIONAUTH_URL, CODE_GRANT_PATH)
    auth_url_params = urlencode({
        "client_id": settings.FUSIONAUTH_CLIENT_ID,
        "redirect_uri": redirect_uri,
        "tenant_id": settings.FUSIONAUTH_TENANT_ID,
        "response_type": "code",
        "scope": "offline_access",  # (ensures "refresh_token" is returned)
        "locale": "en",
    })
    auth_url = f"{base_auth_url}?{auth_url_params}"

    response = redirect(auth_url)
    return response


def callback_view(request):

    AUTHENTICATE_PATH = "api/auth/authenticate"

    data = request.GET
    logger.info(data)

    authenticate_response = requests.post(
        urljoin(settings.DASHBOARD_API_URL, AUTHENTICATE_PATH),
        data=data,
        timeout=REQUEST_TIMEOUT,
    )

    return JsonResponse(
        authenticate_response.json(),
        status=authenticate_response.status_code,
    )
