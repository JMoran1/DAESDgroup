# Generated by Django 4.1.2 on 2023-03-06 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlixApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='num_total',
        ),
    ]
