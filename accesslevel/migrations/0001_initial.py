# Generated by Django 4.0.2 on 2022-04-20 08:06

import accesslevel.models.access_level_models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import extra_scripts.validate_image


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLevelAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, help_text='اسم انگلیسی اکشن', max_length=200, null=True, unique=True)),
                ('display_name', models.CharField(blank=True, help_text='اسم فارسی اکشن', max_length=200, null=True)),
                ('description', models.TextField(blank=True, help_text='توضیحات', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccessLevelGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, help_text='اسم منو که به عنوان url استفاده می\u200cشه', max_length=200, null=True, unique=True)),
                ('display_name', models.CharField(blank=True, help_text='اسم منو جهت نمایش', max_length=200, null=True)),
                ('display_name_eng', models.CharField(blank=True, help_text='name to show , in english', max_length=200, null=True)),
                ('description', models.TextField(blank=True, help_text='توضیحات درباره منو', null=True)),
                ('index', models.FloatField(blank=True, null=True)),
                ('hide', models.BooleanField(default=False, help_text='جهت عدم نمایش باید مقدار true شود')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AccessLevelSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, help_text='نام موضوع', max_length=200, null=True, unique=True)),
                ('icon', models.FileField(blank=True, help_text='آیکن هاور نشده', null=True, upload_to=accesslevel.models.access_level_models.access_level_subject_icon_path, validators=[extra_scripts.validate_image.validate_image, django.core.validators.FileExtensionValidator(['png', 'jpg', 'svg', 'jpeg'])])),
                ('hovered_icon', models.FileField(blank=True, help_text='آیکن هاور شده موضوع', null=True, upload_to=accesslevel.models.access_level_models.access_level_subject_icon_hovered_path, validators=[extra_scripts.validate_image.validate_image, django.core.validators.FileExtensionValidator(['png', 'jpg', 'svg', 'jpeg'])])),
                ('large_icon', models.FileField(blank=True, help_text='آیکن بزرگ هاور شده موضوع', null=True, upload_to=accesslevel.models.access_level_models.access_level_subject_large_icon_path, validators=[extra_scripts.validate_image.validate_image, django.core.validators.FileExtensionValidator(['png', 'jpg', 'svg', 'jpeg'])])),
                ('large_hovered_icon', models.FileField(blank=True, help_text='آیکن بزرگ هاور شده موضوع', null=True, upload_to=accesslevel.models.access_level_models.access_level_subject_large_icon_hovered_path, validators=[extra_scripts.validate_image.validate_image, django.core.validators.FileExtensionValidator(['png', 'jpg', 'svg', 'jpeg'])])),
                ('display_name', models.CharField(blank=True, help_text='اسمی که نمایش داده میشه', max_length=200, null=True)),
                ('display_name_eng', models.CharField(blank=True, help_text='english name for show', max_length=200, null=True)),
                ('importance', models.IntegerField(blank=True, help_text='میزان اهمیت موضوع. برای sort کردن موضوعات در ساید بار', null=True)),
                ('description', models.TextField(blank=True, help_text='توضیحات راجع به این موضوع', null=True)),
                ('index', models.FloatField(blank=True, null=True)),
            ],
            options={
                'ordering': ('index',),
            },
        ),
        migrations.CreateModel(
            name='CommonAccessLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, help_text='اسم دسترسی متداول (مثلا کاربر مالی ارشد)', max_length=200, null=True)),
                ('ename', models.CharField(blank=True, help_text='اسم انگلیسی دسترسی متداول', max_length=200, null=True)),
                ('description', models.TextField(blank=True, help_text='توضیحات بیشتر راجع به این دسترسی متداول', null=True)),
                ('actions', models.ManyToManyField(blank=True, help_text='اکشن\u200cهایی که این کاربر متداول دارد', to='accesslevel.AccessLevelAction')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CommonAccessLevelGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(blank=True, help_text='نام دسته', max_length=200, null=True)),
                ('ename', models.CharField(blank=True, help_text='نام انگلیسی دسته', max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserRowCountAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('model_name', models.CharField(blank=True, help_text='name of the model we want limit for user', max_length=100, null=True)),
                ('count_of_row', models.IntegerField(blank=True, help_text='number of objects user can access in list', null=True)),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accesslevel.commonaccesslevel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='commonaccesslevel',
            name='common_access_level_group',
            field=models.ForeignKey(blank=True, help_text='این کاربر متداول به کدام دسته متعلق است؟', null=True, on_delete=django.db.models.deletion.SET_NULL, to='accesslevel.commonaccesslevelgroup'),
        ),
        migrations.AddField(
            model_name='commonaccesslevel',
            name='groups',
            field=models.ManyToManyField(help_text='گروه\u200cها (منو) که این کاربر متداول به آن\u200cها دسترسی دارد', to='accesslevel.AccessLevelGroup'),
        ),
        migrations.AddField(
            model_name='commonaccesslevel',
            name='subjects',
            field=models.ManyToManyField(help_text='موضوعاتی که این کاربر متداول به آنها دسترسی دارد', to='accesslevel.AccessLevelSubject'),
        ),
        migrations.CreateModel(
            name='AccessLevelRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
                ('negative', models.BooleanField(default=False, help_text='اگر ترو باشد یعنی درخواست سلب دسترسی و اگر فالس باشد یعنی درخواست اخذ دسترسی است')),
                ('granted', models.BooleanField(blank=True, help_text='آیا درخواست سطح دسترسی قبول شده یا رد شده.', null=True)),
                ('not_granted_desc', models.TextField(blank=True, help_text='اگر درخواست رد شده چه توضیحاتی داشته', null=True)),
                ('common_access_level', models.ForeignKey(blank=True, help_text='سطح دسترسی متداولی که درخواست شده', null=True, on_delete=django.db.models.deletion.SET_NULL, to='accesslevel.commonaccesslevel')),
            ],
            options={
                'ordering': ['-granted', '-id'],
            },
        ),
        migrations.AddField(
            model_name='accesslevelgroup',
            name='access_level_subject',
            field=models.ForeignKey(blank=True, help_text='موضوعی که منو در آن وجود دارد', null=True, on_delete=django.db.models.deletion.SET_NULL, to='accesslevel.accesslevelsubject'),
        ),
        migrations.AddField(
            model_name='accesslevelaction',
            name='access_level_group',
            field=models.ForeignKey(blank=True, help_text='این اکشن مربوط به کدام منو است', null=True, on_delete=django.db.models.deletion.SET_NULL, to='accesslevel.accesslevelgroup'),
        ),
    ]
