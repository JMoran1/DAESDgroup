# Generated by Django 4.1.7 on 2023-04-19 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "UWEFlixApp",
            "0010_remove_user_members_have_club_user_requested_club_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="booking",
            name="cancel_requested",
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
    ]
