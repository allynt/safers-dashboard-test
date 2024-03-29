# Generated by Django 4.2 on 2023-05-11 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile',
            field=models.JSONField(default=dict, help_text='JSON representation of profile; used for synchronization w/ gateway.'),
        ),
    ]
