from django.db import models 

from extra_scripts.timestampmodel import TimeStampedModel



class CommonAccessLevelGroup(TimeStampedModel):
    '''گروه‌های اصلی کاربران مثل دسته مالی، اداری، انبارداری و غیره'''

    fname = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text='نام دسته',
    )

    ename = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text='نام انگلیسی دسته',
    )

    def __str__(self):
        return self.fname
    

class CommonAccessLevel(TimeStampedModel):
    '''
    سطح دسترسی متداول:
    دسترسی در این سامانه تحت این مدل به افراد داده می‌شود.
    ما از روی موضوعات، گروه‌ها و اکشن‌ها یک دسترسی متداول می‌سازیم و به افراد مختلف این دسترسی را می‌دهیم
    
    '''
    common_access_level_group = models.ForeignKey(
        CommonAccessLevelGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text='این کاربر متداول به کدام دسته متعلق است؟',
    )

    fname = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text='اسم دسترسی متداول (مثلا کاربر مالی ارشد)',
    )

    ename = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text='اسم انگلیسی دسترسی متداول',
    )

    subjects = models.ManyToManyField(
        'accesslevel.AccessLevelSubject',
        help_text='موضوعاتی که این کاربر متداول به آنها دسترسی دارد',
    )

    groups = models.ManyToManyField(
        'accesslevel.AccessLevelGroup',
        help_text='گروه‌ها (منو) که این کاربر متداول به آن‌ها دسترسی دارد'
    )

    actions = models.ManyToManyField(
        'accesslevel.AccessLevelAction',
        blank=True,
        help_text='اکشن‌هایی که این کاربر متداول دارد',
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text='توضیحات بیشتر راجع به این دسترسی متداول',
    )

    def __str__(self):
        return self.fname
    