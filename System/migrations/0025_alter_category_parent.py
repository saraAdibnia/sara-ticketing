# Generated by Django 4.0.2 on 2022-02-22 12:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0024_alter_category_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='System.category'),
        ),
    ]
