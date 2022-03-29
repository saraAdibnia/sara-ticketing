# Generated by Django 4.0.2 on 2022-03-17 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Mymodel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('answer', models.JSONField(blank=True, help_text=",\n            contains jsons in a specific order in the list\n            each json's key shows a warehouse id as an integer\n            each json's value shows that the cargo has either reached there or not\n            so the json values are booleans        \n            ", null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SmsCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('code', models.IntegerField(help_text='کد دسته بندی پیامک')),
                ('title', models.CharField(help_text='عنوان دسته بندی پیامک', max_length=128)),
                ('description', models.CharField(blank=True, help_text='توضیحات دسته بندی پیامک', max_length=512, null=True)),
                ('smsText', models.TextField(blank=True, help_text='متن پیامک', null=True)),
                ('kind', models.SmallIntegerField(blank=True, choices=[(1, 'واردات'), (2, 'صادرات'), (3, 'داخلی'), (4, 'اپراتور'), (5, 'ادمین'), (6, 'بازاریابی'), (7, 'متفرقه')], null=True)),
                ('isActive', models.BooleanField(default=True, help_text='آیا دسته بندی پیامک فعال است؟')),
                ('sendByNumber', models.SmallIntegerField(choices=[(1, '100045312'), (2, '0018018949161'), (3, '10008663'), (4, '2000500666')], default=1, help_text='شماره خط جهت ارسال پیامک')),
                ('activeBy', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SmsSend',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.SmallIntegerField(blank=True, null=True)),
                ('is_send', models.BooleanField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SMSLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('params_receptor', models.CharField(blank=True, max_length=32, null=True)),
                ('params_message', models.TextField(blank=True, null=True)),
                ('params_sender', models.CharField(blank=True, max_length=32, null=True)),
                ('params_template', models.CharField(blank=True, max_length=32, null=True)),
                ('params_token', models.CharField(blank=True, max_length=32, null=True)),
                ('params_type', models.CharField(blank=True, max_length=32, null=True)),
                ('validation', models.BooleanField(blank=True, null=True)),
                ('status', models.SmallIntegerField(choices=[(1, 'در صف ارسال قرار دارد'), (2, 'زمان بندی شده (ارسال در تاریخ معین)'), (4, 'ارسال شده به مخابرات'), (5, 'ارسال شده به مخابرات (همانند وضعیت 4)'), (6, 'خطا در ارسال پیام که توسط سر شماره پیش می آید و به معنی عدم رسیدن پیامک می\u200cباشد (Failed)'), (10, 'رسیده به گیرنده (Delivered)'), (11, 'نرسیده به گیرنده ، این وضعیت به دلایلی از جمله خاموش یا خارج از دسترس بودن گیرنده اتفاق می افتد (Undelivered)'), (13, 'ارسال پیام از سمت کاربر لغو شده یا در ارسال آن مشکلی پیش آمده که هزینه آن به حساب برگشت داده می\u200cشود'), (14, 'بلاک شده است، عدم تمایل گیرنده به دریافت پیامک از خطوط تبلیغاتی که هزینه آن به حساب برگشت داده می\u200cشود'), (100, 'شناسه پیامک نامعتبر است ( به این معنی که شناسه پیام در پایگاه داده کاوه نگار ثبت نشده است یا متعلق به شما نمی\u200cباشد)')], null=True)),
                ('messageid', models.BigIntegerField(null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('sender', models.CharField(blank=True, max_length=32, null=True)),
                ('receptor', models.CharField(blank=True, max_length=32, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('cost', models.IntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_sending', models.BooleanField(default=True)),
                ('send_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('smsCat', models.ForeignKey(blank=True, help_text='دسته بندی پیامک', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sms_smsCategory', to='developinglogs.smscategory')),
            ],
        ),
        migrations.CreateModel(
            name='ReceivedSms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('messageid', models.BigIntegerField(blank=True, help_text='شناسه پیامک دریافتی که به شما کمک می کند پیامک های تکراری را دریافت نکنید', null=True)),
                ('message', models.TextField(blank=True, help_text='متن پیامک دریافت شده', null=True)),
                ('sender', models.CharField(blank=True, help_text='شماره فرستنده پیامک', max_length=32, null=True)),
                ('receptor', models.CharField(blank=True, help_text='شماره گیرنده پیامک', max_length=32, null=True)),
                ('time', models.DateTimeField(blank=True, null=True)),
                ('sender_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]