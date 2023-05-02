from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.urls import include, path

from rest_framework import routers

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from config.types import EnvironmentTypes

# from safers.core.urls import (
#     urlpatterns as core_urlpatterns,
#     api_urlpatterns as core_api_urlpatterns,
# )

# from safers.auth.urls import (
#     urlpatterns as auth_urlpatterns,
#     api_urlpatterns as auth_api_urlpatterns,
# )

from safers.users.urls import (
    urlpatterns as users_urlpatterns,
    api_urlpatterns as users_api_urlpatterns,
)

################
# admin config #
################

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE

#################
# swagger stuff #
#################

swagger_restriction = user_passes_test(
    # prevent ordinary users from accessing swagger unless DEBUG is True
    lambda user: (settings.DEBUG or user.is_admin),
    login_url="admin:login",
)

api_schema_views = [
    path(
        "swagger/",
        swagger_restriction(
            SpectacularSwaggerView.as_view(url_name="api-schema")
        ),
        name="api-docs",
    ),
    path(
        "schema/",
        swagger_restriction(SpectacularAPIView.as_view()),
        name="api-schema"
    ),
]

##############
# API routes #
##############

api_router = routers.DefaultRouter()
api_urlpatterns = [
    path("", include(api_schema_views)),
    path("", include(api_router.urls)),
]

# api_urlpatterns += core_api_urlpatterns
# api_urlpatterns += auth_api_urlpatterns
api_urlpatterns += users_api_urlpatterns

#################
# normal routes #
#################

urlpatterns = [
    # django admin...
    path(settings.ADMIN_URL, admin.site.urls),

    # API...
    path("api/", include(api_urlpatterns)),

    # app-specific patterns (just in case)...
    # path("", include(core_urlpatterns)),
    # path("auth", include(auth_urlpatterns)),
    path("users", include(users_urlpatterns)),
]

# local static & media files...
if settings.ENVIRONMENT == EnvironmentTypes.DEVELOPMENT:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT,
    )
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

if settings.DEBUG:

    # TODO: error pages
    # TODO: profiling pages

    pass