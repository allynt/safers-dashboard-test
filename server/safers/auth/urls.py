from django.urls import path

from .views import (
    RegisterView,
    AuthenticateView,
    login_view,
    callback_view,
)

api_urlpatterns = [
    path(
        "auth/register",
        RegisterView.as_view(),
        name="auth-register",
    ),
    path(
        "auth/authenticate",
        AuthenticateView.as_view(),
        name="auth-authenticate",
    ),
]

urlpatterns = [
    path("auth/login", login_view, name="auth-login"),
    path("auth/callback", callback_view, name="auth-callback"),
]
