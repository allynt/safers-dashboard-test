from django.urls import include, path

from rest_framework import routers

from .views import (
    settings_view,
)

api_router = routers.DefaultRouter()
api_urlpatterns = [
    path("", include(api_router.urls)),
    path("settings", settings_view, name="settings"),
]

urlpatterns = []


