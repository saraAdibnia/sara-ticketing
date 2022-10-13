from django.db import models

from extra_scripts.timestampmodel import TimeStampedModel
from user.models import User\
# Create your models here.


class SmsSend(models.Model):

    kind = models.SmallIntegerField(
        blank=True,
        null=True,
    )

    is_send = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f"{self.kind}"


class SmsCategory(TimeStampedModel):
    code = models.IntegerField(
        blank=False,
        help_text="کد دسته بندی پیامک",
        null=False,
    )
    title = models.CharField(
        max_length=128,
        blank=True,
        null=True,
        help_text="عنوان دسته بندی پیامک",
    )
    description = models.CharField(
        max_length=512,
        blank=True,
        null=True,
        help_text="توضیحات دسته بندی پیامک",
    )
    smsText = models.TextField(
        blank=True,
        null=True,
        help_text="متن پیامک",
    )
    KIND_CHOICES = ((1, "واردات"),
                    (2, "صادرات"),
                    (3, "داخلی"),
                    (4, "اپراتور"),
                    (5, "ادمین"),
                    (6, "بازاریابی"),
                    (7, "متفرقه"))
    kind = models.SmallIntegerField(
        choices=KIND_CHOICES, blank=True, null=True,)

    isActive = models.BooleanField(
        blank=False,
        default=True,
        help_text="آیا دسته بندی پیامک فعال است؟",
    )
    activeBy = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    number_choices = (
        (1, "100045312"),
        (2, "0018018949161"),
        (3, "10008663"),
        (4, "2000500666"),
    )
    sendByNumber = models.SmallIntegerField(
        default=1,
        blank=False,
        null=False,
        choices=number_choices,
        help_text="شماره خط جهت ارسال پیامک",
    )
# TODO add modified_by field

    def __str__(self):
        return f"{self.code} : {self.title}"


class SMSLog(models.Model):

    params_receptor = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="",
    )

    params_message = models.TextField(
        blank=True,
        null=True,
    )

    params_sender = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="",
    )

    params_template = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="",
    )

    params_token = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="",
    )

    params_type = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="",
    )

    validation = models.BooleanField(
        blank=True,
        null=True,
        help_text="",
    )

    status_choices = (
        (1, "در صف ارسال قرار دارد"),
        (2, "زمان بندی شده (ارسال در تاریخ معین)"),
        (4, "ارسال شده به مخابرات"),
        (5, "ارسال شده به مخابرات (همانند وضعیت 4)"),
        (
            6,
            "خطا در ارسال پیام که توسط سر شماره پیش می آید و به معنی عدم رسیدن پیامک می‌باشد (Failed)",
        ),
        (10, "رسیده به گیرنده (Delivered)"),
        (
            11,
            "نرسیده به گیرنده ، این وضعیت به دلایلی از جمله خاموش یا خارج از دسترس بودن گیرنده اتفاق می افتد (Undelivered)",
        ),
        (
            13,
            "ارسال پیام از سمت کاربر لغو شده یا در ارسال آن مشکلی پیش آمده که هزینه آن به حساب برگشت داده می‌شود",
        ),
        (
            14,
            "بلاک شده است، عدم تمایل گیرنده به دریافت پیامک از خطوط تبلیغاتی که هزینه آن به حساب برگشت داده می‌شود",
        ),
        (
            100,
            "شناسه پیامک نامعتبر است ( به این معنی که شناسه پیام در پایگاه داده کاوه نگار ثبت نشده است یا متعلق به شما نمی‌باشد)",
        ),
    )

    status = models.SmallIntegerField(
        null=True,
        choices=status_choices,
        help_text="",
    )

    messageid = models.BigIntegerField(
        null=True,
        help_text="",
    )

    message = models.TextField(
        blank=True,
        null=True,
    )

    sender = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="",
    )

    receptor = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="",
    )
    smsCat = models.ForeignKey(
        SmsCategory,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        help_text="دسته بندی پیامک",
        related_name="sms_smsCategory",
    )
    send_by = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    date = models.DateTimeField(
        blank=True,
        null=True,
    )

    cost = models.IntegerField(
        blank=True,
        null=True,
        help_text="",
    )

    created_date = models.DateTimeField(auto_now_add=True)

    is_sending = models.BooleanField(default=True)  # send or recieved types

    def __str__(self):
        return f"{self.params_receptor} - {self.params_sender} -  {self.smsCat}"


class ReceivedSms(TimeStampedModel):
    messageid = models.BigIntegerField(
        null=True,
        help_text="شناسه پیامک دریافتی که به شما کمک می کند پیامک های تکراری را دریافت نکنید",
        blank= True, 
    )
    message = models.TextField(
        blank=True,
        null=True,
        help_text="متن پیامک دریافت شده"
    )

    sender = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="شماره فرستنده پیامک",
    )
    receptor = models.CharField(
        max_length=32,
        blank=True,
        null=True,
        help_text="شماره گیرنده پیامک",
    )
    sender_user = models.ForeignKey(User, on_delete= models.SET_NULL, blank= True, null= True)
    time = models.DateTimeField(
        blank=True,
        null=True,
    )

