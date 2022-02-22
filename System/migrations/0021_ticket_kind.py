# Generated by Django 4.0.2 on 2022-02-22 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0020_remove_ticket_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='Kind',
            field=models.IntegerField(blank=True, choices=[(1, 'DARUN SAZMANI'), (2, 'BIRUN SAZMANI')], default=1, null=True),
        ),
    ]
