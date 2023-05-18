from django.apps import AppConfig


class AuthConfig(AppConfig):
    name = 'auth'
    label = "client_auth"  # unique label so as not to conflict w/ "django.contrib.auth"
