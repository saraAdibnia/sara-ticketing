# Generated by Django 4.0.2 on 2022-07-26 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0033_alter_answer_reaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='ticket',
        ),
        migrations.AlterField(
            model_name='answer',
            name='reaction',
            field=models.IntegerField(choices=[(0, 'Thumbs Down'), (1, 'Thmbs Up ')], null=True),
        ),
    ]