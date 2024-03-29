# Generated by Django 4.0.2 on 2022-08-23 09:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import user.models.user


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0009_alter_state_country'),
        # ('accesslevel', '0008_rename_name_commonaccesslevel_fname'),
        ('department', '0004_rename_created_date_department_created_and_more'),
        ('user', '0017_alter_user_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('temp_password', models.CharField(blank=True, max_length=128, null=True, verbose_name='temp_password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(blank=True, db_index=True, max_length=25, null=True)),
                ('mobile', models.CharField(db_index=True, help_text='شماره موبایل (فیلد اصلی یوزرنیم)', max_length=20)),
                ('fname', models.CharField(help_text='اسم کوچک فارسی', max_length=100, null=True)),
                ('ename', models.CharField(blank=True, help_text='اسم کوچک انگلیسی', max_length=100, null=True)),
                ('flname', models.CharField(help_text='نام خانوادگی فارسی', max_length=100, null=True)),
                ('elname', models.CharField(blank=True, help_text='نام خانوادگی انگلیسی', max_length=100, null=True)),
                ('economic_code', models.CharField(blank=True, help_text='کد اقتصادی (حقوقی)', max_length=30, null=True)),
                ('national_id', models.CharField(blank=True, help_text='شناسه ملی (حقوقی)', max_length=30, null=True)),
                ('registration_id', models.CharField(blank=True, help_text='شناسه ثبت (حقوقی)', max_length=30, null=True)),
                ('register_date', models.DateField(blank=True, help_text='تاریخ ثبت (حقوقی)', null=True)),
                ('postal_code', models.CharField(blank=True, help_text='کد پستی (حقوقی)', max_length=100, null=True)),
                ('address_text', models.CharField(blank=True, help_text='آدرس شرکت (حقوقی)', max_length=1500, null=True)),
                ('phone', models.CharField(blank=True, help_text='شماره تلفن ثابت', max_length=30, null=True)),
                ('field_of_work', models.CharField(blank=True, help_text='حوزه\u200cی کاری (حقوقی)', max_length=30, null=True)),
                ('uni_code', models.CharField(blank=True, help_text='کد ملی', max_length=100, null=True)),
                ('email', models.EmailField(help_text='ایمیل', max_length=254, null=True)),
                ('email_verified', models.BooleanField(default=False, help_text='ایا ایمیل اعتبارسنجی شده یا خیر')),
                ('birthday', models.DateField(blank=True, help_text='تاریخ تولد (حقیقی)', null=True)),
                ('profile_image', models.TextField(blank=True, help_text='عکس پروفایل', max_length=100, null=True, validators=[user.models.user.Validate_Image])),
                ('needs_to_change_pass', models.BooleanField(default=False, help_text='آیا یوزر از فراموشی رمز عبور استفاده کرده و مجبور است رمز خود را عوض کند؟')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('banned', models.BooleanField(default=False, help_text='یوزر از سایت بن شده')),
                ('ban_cause', models.TextField(blank=True, help_text='علت بن شدن یوزر از سایت', null=True)),
                ('is_real', models.BooleanField(default=True, help_text='یوزر حقیقی\u200c است یا حقوقی')),
                ('role', models.SmallIntegerField(choices=[(0, 'کاربر عادی'), (1, 'کاربر داشبورد سازمانی'), (2, 'تحصیل\u200cدار')], default=0, help_text='handling the user kind, role')),
                ('signiture', models.CharField(blank=True, help_text='امضا', max_length=100, null=True)),
                ('gender', models.BooleanField(blank=True, help_text='male = True, female = False', null=True)),
                ('created_time', models.DateTimeField(blank=True, editable=False)),
                ('modified', models.DateTimeField(blank=True, editable=False)),
                ('direct_login', models.BooleanField(blank=True, default=False, null=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('access_granted_by', models.ForeignKey(blank=True, db_constraint=False, help_text='دسترسی به این کاربر آخرین بار توسط چه کسی داده شده است.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('banned_by', models.ForeignKey(blank=True, db_constraint=False, help_text='یوزر توسط چه کسی بن شده', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('common_access_level', models.ForeignKey(blank=True, db_constraint=False, help_text='سطح دسترسی متداولی که کاربر به آن دسترسی دارد', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='accesslevel.commonaccesslevel')),
                ('country', models.ForeignKey(blank=True, db_constraint=False, default=1112, help_text='کشور محل سکونت', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='places.country')),
                ('created_by', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('department', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='department.department')),
                ('dial_code', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='places.dialcode')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(blank=True, db_constraint=False, default=19395, help_text='استان محل سکونت', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='places.state')),
            ],
            options={
                'verbose_name': 'historical user',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
