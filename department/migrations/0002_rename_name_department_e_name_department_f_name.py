# Generated by Django 4.0.2 on 2022-05-30 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='name',
            new_name='e_name',
        ),
        migrations.AddField(
            model_name='department',
            name='f_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
