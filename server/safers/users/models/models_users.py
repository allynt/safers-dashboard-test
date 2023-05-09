from typing import Iterable, Optional
import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import models
from django.db.models.expressions import ExpressionWrapper
from django.db.models.query_utils import Q
from django.utils.translation import gettext_lazy as _

from model_utils import FieldTracker

from safers.users.models import Organization, Role

###########
# helpers #
###########


class UserStatus(models.TextChoices):
    PENDING = "PENDING", _("Pending")
    COMPLETED = "COMPLETED", _("Completed")


########################
# managers & querysets #
########################


class UserManager(BaseUserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not email:
            raise ValueError('The given email must be set')

        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(
        self, username, email=None, password=None, **extra_fields
    ):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

    def get_queryset(self):
        """
        Add some calculated fields to the default queryset
        """
        qs = super().get_queryset()

        return qs.annotate(
            _is_local=ExpressionWrapper(
                Q(auth_id__isnull=True), output_field=models.BooleanField()
            ),
            _is_remote=ExpressionWrapper(
                Q(auth_id__isnull=False), output_field=models.BooleanField()
            )
        )


class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def local(self):
        return self.filter(_is_local=True)

    def remote(self):
        return self.filter(_is_remote=True)


##########
# models #
##########


class User(AbstractUser):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    objects = UserManager.from_queryset(UserQuerySet)()

    tracker = FieldTracker()

    # remove these fields, as they should form part of the UserProfile
    first_name = None
    last_name = None

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    email = models.EmailField(
        _('email address'),
        blank=False,
        unique=True,
    )

    change_password = models.BooleanField(
        default=False,
        help_text=_("Force user to change password at next login.")
    )

    accepted_terms = models.BooleanField(
        default=False,
        help_text=_("Has this user accepted the terms & conditions?")
    )

    auth_id = models.UUIDField(
        blank=True,
        editable=False,
        null=True,
        unique=True,
        help_text=_("The corresponding id of the FusionAuth User"),
    )

    status = models.CharField(
        max_length=64,
        choices=UserStatus.choices,
        default=UserStatus.PENDING,
        help_text=_("What stage of registration is this user at?"),
    )

    organization_name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )

    role_name = models.CharField(
        max_length=128,
        blank=True,
        null=True,
    )

    @property
    def is_local(self):
        return self.auth_id is None

    @property
    def is_remote(self):
        return self.auth_id is not None

    @property
    def is_citizen(self):
        role = self.role
        return role and role.is_citizen

    @property
    def organization(self):
        try:
            return Organization.objects.get(name=self.organization_name)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            pass

    @property
    def role(self):
        try:
            return Role.objects.get(name=self.role_name)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            pass

    def save(self, *args, **kwargs):
        if self.tracker.has_changed("status"):
            # TODO: DO SOMETHING WITH SIGNALS HERE ?
            old_status = self.tracker.previous("status")
            new_status = self.status
        return super().save(*args, **kwargs)
