# Generated by Django 4.2 on 2023-05-02 07:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SafersSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('_singleton_id', models.IntegerField(default=1, editable=False, help_text='An ID to use for this mixin, in case the model uses some non-standard PK.')),
                ('allow_signin', models.BooleanField(default=True, help_text='Allow users to signin w/ Safers-Dashboard.')),
                ('allow_signup', models.BooleanField(default=True, help_text='Allow users to register w/ Safers-Dashboard.')),
                ('allow_password_change', models.BooleanField(default=False, help_text='Allow users to change their password via the dashboard.')),
                ('require_terms_acceptance', models.BooleanField(default=True, help_text='Require a user to accept the terms & conditions during the sign up process.')),
                ('request_timeout', models.FloatField(default=6000, help_text='The time (in milliseconds) for the frontend to wait for a response from the backend. Set to 0 to have no timeout.', validators=[django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'Settings',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]
