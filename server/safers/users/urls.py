from django.urls import include, path

from rest_framework import routers

from safers.users.views import (
    UserView,
    OrganizationView,
    RoleView,
)

api_router = routers.DefaultRouter()
api_urlpatterns = [
    path("", include(api_router.urls)),
    path("users/<slug:user_id>", UserView.as_view(), name="users"),
    path("organizations", OrganizationView.as_view(), name="organizations"),
    path("roles", RoleView.as_view(), name="roles"),
]

urlpatterns = []
