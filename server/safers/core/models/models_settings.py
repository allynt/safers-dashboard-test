from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from safers.core.mixins import SingletonMixin


class SafersSettings(SingletonMixin, models.Model):
    class Meta:
        verbose_name = "Settings"
        verbose_name_plural = "Settings"

    allow_signin = models.BooleanField(
        default=True,
        help_text=_("Allow users to signin w/ Safers-Dashboard."),
    )

    allow_signup = models.BooleanField(
        default=True,
        help_text=_("Allow users to register w/ Safers-Dashboard."),
    )

    allow_password_change = models.BooleanField(
        default=False,
        help_text=_("Allow users to change their password via the dashboard.")
    )

    require_terms_acceptance = models.BooleanField(
        default=True,
        help_text=_(
            "Require a user to accept the terms & conditions during the sign up process."
        ),
    )

    request_timeout = models.FloatField(
        default=6000,
        validators=[MinValueValidator(0)],
        help_text=_(
            "The time (in milliseconds) for the frontend to wait for a response from the backend. "
            "Set to 0 to have no timeout."
        )
    )

    def __str__(self) -> str:
        return "Safers Settings"
