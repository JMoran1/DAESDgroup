# Generated by Django 4.1.6 on 2023-04-24 16:52

from django.db import migrations
from django.utils.text import slugify


def populate_ticket_uids(apps, schema_editor):
    Ticket = apps.get_model('UWEFlixApp', 'Ticket')
    for ticket in Ticket.objects.all():
        ticket.uid = slugify(ticket.type)

class Migration(migrations.Migration):

    dependencies = [
        ('UWEFlixApp', '0017_remove_screening_seats_remaining_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ticket',
            old_name='ticket_type',
            new_name='type',
        ),
        migrations.AlterField(
            model_name='ticket',
            name='type',
            field=models.CharField(max_length=50, unique=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='uid',
            field=models.SlugField(null=True),
        ),
        migrations.RunPython(populate_ticket_uids, lambda a, s: None), # no action required for backwards migrate
        migrations.AlterField(
            model_name='ticket',
            name='uid',
            field=models.SlugField(unique=True),
        ),
    ]