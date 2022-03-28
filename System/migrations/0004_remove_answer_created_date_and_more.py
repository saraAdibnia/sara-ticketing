# Generated by Django 4.0.2 on 2022-03-28 06:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0003_rename_to_operator_answer_reciever_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='answer',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='file',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='file',
            name='modified_date',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='modified_date',
        ),
        migrations.AddField(
            model_name='answer',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='ticket',
            name='modified',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
