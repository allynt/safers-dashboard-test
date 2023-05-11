"""
Custom Authentication Extensions to ensure DRF Authentication is correctly
configured in swagger.  drf-spectacular intropects "DEFAULT_AUTHENTICATION_CLASSES"
to try and automatically populate the "Available Authorizations" Dialog Box.  
But if any of those classes are not recognized, or if safers' implementation 
of them is non-standard, then _these_ schemes can be used instead (as long as 
the "target_class" matches and "priority" is <= any other matching schemes).
"""
from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.plumbing import build_bearer_security_scheme_object

from safers.auth.authentication import OAuth2Authentication


class SwaggerOAuth2Authentication(OpenApiAuthenticationExtension):

    # TODO: FOUND A BUG IN drf-spectacular (`target_class` requires Class object instead of path) ?
    # taget_class = "safers.auth.authentication.OAuth2Authentication"
    target_class = OAuth2Authentication
    name = "access_token Authentication"
    match_subclasses = False
    priority = -1

    token_prefix = "Bearer"
    description = f"Token-based authentication with required prefix: {token_prefix}"

    def get_security_definition(self, auto_schema):
        scheme = build_bearer_security_scheme_object(
            header_name="Authorization", token_prefix=self.token_prefix
        )
        scheme["description"] = self.description
        return scheme
