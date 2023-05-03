# Generated by Django 4.2 on 2023-05-03 02:33

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_siteprofile_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('admin_code', models.CharField(max_length=3, unique=True)),
                ('admin_name', models.CharField(max_length=128)),
                ('sovereign_name', models.CharField(max_length=128)),
                ('sovereign_code', models.CharField(max_length=3)),
                ('geometry', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
    ]