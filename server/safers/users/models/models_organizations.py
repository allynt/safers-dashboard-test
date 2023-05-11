import requests
from urllib.parse import urljoin

from django.conf import settings
from django.db import models

from safers.core.managers import CachedTransientModelManager, TransientModelQuerySet

from safers.users.tests.mocks import MOCK_ORGANIZATIONS_DATA


class OrganizationQuerySet(TransientModelQuerySet):
    pass


class OrganizationManager(CachedTransientModelManager):

    queryset_class = OrganizationQuerySet

    cache_key = "organizations"

    def get_transient_queryset_data(self):
        # TODO: USE GATEWAY_CLIENT
        GET_ORGANIZATIONS_PATH = "/api/services/app/Profile/GetOrganizations"
        response = requests.get(
            urljoin(settings.SAFERS_GATEWAY_URL, GET_ORGANIZATIONS_PATH),
            params={"MaxResultCount": 1000},
            timeout=4,
        )
        response.raise_for_status()
        organizations_data = response.json()["data"]

        # organizations_data = MOCK_ORGANIZATIONS_DATA

        return organizations_data


class Organization(models.Model):
    class Meta:
        managed = False

    objects = OrganizationManager.from_queryset(OrganizationQuerySet)()

    id = models.IntegerField(primary_key=True)
    shortName = models.CharField(max_length=32)
    name = models.CharField(max_length=128)
    description = models.TextField(null=True)
    webSite = models.URLField(null=True)
    logoUrl = models.URLField(null=True)
    parentId = models.IntegerField(null=True)
    parentName = models.CharField(max_length=128, null=True)
    membersHaveTaxCode = models.BooleanField(null=True)
    hasChildren = models.BooleanField(null=True)

    def __str__(self) -> str:
        return str(self.name)

    @property
    def title(self) -> str:
        """
        Return a pretty name for the organization
        """
        return str(self).title()