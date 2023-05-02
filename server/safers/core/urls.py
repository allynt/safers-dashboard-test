from django.urls import include, path

from rest_framework import routers

from .views import (
    SettingsView,
)

api_router = routers.DefaultRouter()
api_urlpatterns = [
    path("", include(api_router.urls)),
]

urlpatterns = []
