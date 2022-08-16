# Generated by Django 4.0.2 on 2022-08-16 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0009_alter_state_country'),
        ('user', '0015_alter_user_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.ForeignKey(blank=True, default=1112, help_text='کشور محل سکونت', null=True, on_delete=django.db.models.deletion.SET_NULL, to='places.country'),
        ),
    ]
