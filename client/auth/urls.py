from django.urls import path

from .views import (
    login_view,
    callback_view,
)

urlpatterns = [
    path("login", login_view, name="login"),
    path("sign-in", callback_view, name="callback"),
]
