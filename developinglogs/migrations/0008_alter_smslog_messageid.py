# Generated by Django 3.2.5 on 2021-07-06 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('developinglogs', '0007_alter_smslog_created_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='smslog',
            name='messageid',
            field=models.BigIntegerField(null=True),
        ),
    ]
