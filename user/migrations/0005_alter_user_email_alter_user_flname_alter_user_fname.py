# Generated by Django 4.0.2 on 2022-07-25 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_user_city_user_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(help_text='ایمیل', max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='flname',
            field=models.CharField(help_text='نام خانوادگی فارسی', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='fname',
            field=models.CharField(help_text='اسم کوچک فارسی', max_length=100, null=True),
        ),
    ]