# Generated by Django 4.0.2 on 2022-08-09 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0039_review_opertor'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='rated',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]