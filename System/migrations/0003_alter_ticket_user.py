# Generated by Django 4.0.2 on 2022-02-27 08:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('System', '0002_answer_user_ticket_created_by_ticket_department_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='user',
            field=models.ForeignKey(blank=True, help_text='The owner of ticket either for themself or customers or co-workers', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_id', to=settings.AUTH_USER_MODEL, verbose_name='user_id'),
        ),
    ]