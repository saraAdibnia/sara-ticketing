# Generated by Django 4.0.2 on 2022-08-16 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0047_rename_rated_one_review_rated_operator_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_format',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
