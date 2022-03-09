# Generated by Django 4.0.2 on 2022-03-07 07:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0005_alter_ticket_kind'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='is_suspended',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_categories', to='System.category'),
        ),
    ]
