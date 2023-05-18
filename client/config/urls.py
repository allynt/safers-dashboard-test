from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView

from auth.urls import urlpatterns as auth_urlpatterns

urlpatterns = [
    # django admin...
    path(settings.ADMIN_URL, admin.site.urls),

    # index...
    path("", TemplateView.as_view(template_name="index.html"), name="index"),

    # app-specific patterns...
    path("auth/", include(auth_urlpatterns)),
]
