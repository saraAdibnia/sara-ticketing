# Generated by Django 3.2.5 on 2021-09-08 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('history', '0004_auto_20210908_0902'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_log',
            name='log_kind',
            field=models.SmallIntegerField(choices=[(0, 'ورود کاربر'), (1, 'رمز اشتباه'), (2, 'خروج کاربر'), (3, 'توکن اشتباه')], default=0, help_text='نوع لاگ'),
        ),
    ]
