from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    first_name = models.CharField(
        _("first name"), max_length=150, blank=True, null=True
    )
    last_name = models.CharField(
        _("last name"), max_length=150, blank=True, null=True
    )

    # TODO: ADD MORE FIELDS
    # TODO: OR MAYBE I SHOULD JUST USE A JSONField ?

    def __str__(self) -> str:
        return str(self.user)
