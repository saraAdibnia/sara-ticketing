# Generated by Django 4.0.2 on 2022-10-11 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0023_rename_created_time_historicaluser_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaluser',
            name='birthday',
            field=models.CharField(blank=True, help_text='تاریخ تولد (حقیقی)', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.CharField(blank=True, help_text='تاریخ تولد (حقیقی)', max_length=100, null=True),
        ),
    ]