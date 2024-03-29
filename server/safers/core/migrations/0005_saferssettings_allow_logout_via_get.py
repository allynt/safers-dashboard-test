# Generated by Django 4.2 on 2023-05-11 02:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_country'),
    ]

    operations = [
        migrations.AddField(
            model_name='saferssettings',
            name='allow_logout_via_get',
            field=models.BooleanField(default=False, help_text='Allow users to logout via GET as well as POST.'),
        ),
    ]
