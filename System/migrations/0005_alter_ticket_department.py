# Generated by Django 4.0.2 on 2022-03-28 07:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
        ('System', '0004_remove_answer_created_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department_department', to='department.department'),
        ),
    ]