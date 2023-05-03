# Generated by Django 4.2 on 2023-05-03 02:13

from django.db import migrations


def create_site_profiles(apps, schema_editor):

    SiteModel = apps.get_model("sites", "Site")
    SiteProfileModel = apps.get_model("core", "SiteProfile")

    for site in SiteModel.objects.all():
        SiteProfileModel.objects.get_or_create(site=site)


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_siteprofile'),
    ]

    operations = [
        migrations.RunPython(
            create_site_profiles, reverse_code=migrations.RunPython.noop
        )
    ]