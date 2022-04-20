from django.db import models

from extra_scripts.timestampmodel import TimeStampedModel

class AccessLevelRequest(TimeStampedModel):
    '''درخواست سطح دسترسی'''

    user = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='access_level_request_user',
        help_text='دسترسی برای چه کاربری درخواست شده؟',
    )
    
    negative = models.BooleanField(
        default=False,
        help_text='اگر ترو باشد یعنی درخواست سلب دسترسی و اگر فالس باشد یعنی درخواست اخذ دسترسی است',
    )

    department = models.ForeignKey(
        'department.Department',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='دفتری که برای دسترسی درخواست شده',
    )

    common_access_level = models.ForeignKey(
        'accesslevel.CommonAccessLevel',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='سطح دسترسی متداولی که درخواست شده',
    )

    granted = models.BooleanField(
        blank=True,
        null=True,
        help_text='آیا درخواست سطح دسترسی قبول شده یا رد شده.',
    )

    not_granted_desc = models.TextField(
        blank=True,
        null=True,
        help_text='اگر درخواست رد شده چه توضیحاتی داشته',
    )

    granted_by = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='access_level_request_granted_by',
        help_text='درخواست توسط چه کسی بررسی شده',
    )

    created_by = models.ForeignKey(
        'user.User',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='access_level_request_created_by',
        help_text='درخواست توسط چه کسی ثبت شده',
    )

    class Meta:
        ordering = ['-granted', '-id']