# Generated by Django 4.0.2 on 2022-06-26 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FAQ', '0002_frequentlyaskedquestion_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequentlyaskedquestion',
            name='description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
