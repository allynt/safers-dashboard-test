from django.urls import path

from .views import (
    RegisterView,
)

api_urlpatterns = [
    path("auth/register", RegisterView.as_view(), name="auth-register"),
]

urlpatterns = []
