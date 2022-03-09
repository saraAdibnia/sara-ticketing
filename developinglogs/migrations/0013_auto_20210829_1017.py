# Generated by Django 3.2.5 on 2021-08-29 05:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('developinglogs', '0012_smssend'),
    ]

    operations = [
        migrations.CreateModel(
            name='SmsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(help_text='کد دسته بندی پیامک')),
                ('title', models.CharField(help_text='عنوان دسته بندی پیامک', max_length=128)),
                ('description', models.CharField(blank=True, help_text='توضیحات دسته بندی پیامک', max_length=512, null=True)),
                ('smsText', models.TextField(blank=True, help_text='متن پیامک', null=True)),
                ('isActive', models.BooleanField(default=True, help_text='آیا دسته بندی پیامک فعال است؟')),
                ('sendByNumber', models.SmallIntegerField(choices=[(1, '100045312'), (2, '0018018949161'), (3, '10008663'), (4, '2000500666')], default=1, help_text='شماره خط جهت ارسال پیامک')),
            ],
        ),
        migrations.AddField(
            model_name='smslog',
            name='smsCat',
            field=models.ForeignKey(blank=True, help_text='دسته بندی پیامک', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sms_smsCategory', to='developinglogs.smscategory'),
        ),
    ]
