# Generated by Django 4.0.2 on 2022-06-11 08:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0003_answer_to_department'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='e_name',
            new_name='ename',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='f_name',
            new_name='fname',
        ),
    ]
