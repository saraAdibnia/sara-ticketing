from django.db import models
from extra_scripts.timestampmodel import TimeStampedModel
from extra_scripts.validate_image import validate_image
from django.core.validators import FileExtensionValidator


def access_level_subject_icon_path(instance, filename):
    return "access_level_subjects/{}/icon/{}".format(instance.name, filename)


def access_level_subject_icon_hovered_path(instance, filename):
    return "access_level_subjects/{}/hovered_icon/{}".format(instance.name, filename)


def access_level_subject_large_icon_path(instance, filename):
    return "access_level_subjects/{}/large_icon/{}".format(instance.name, filename)


def access_level_subject_large_icon_hovered_path(instance, filename):
    return "access_level_subjects/{}/large_hovered_icon/{}".format(
        instance.name, filename
    )


class AccessLevelSubject(TimeStampedModel):
    """موضوعات سطح دسترسی"""

    name = models.CharField(
        blank=True, null=True, max_length=200, unique=True, help_text="نام موضوع"
    )

    icon = models.FileField(
        upload_to=access_level_subject_icon_path,
        validators=[
            validate_image,
            FileExtensionValidator(["png", "jpg", "svg", "jpeg"]),
        ],
        blank=True,
        null=True,
        help_text="آیکن هاور نشده",
    )

    hovered_icon = models.FileField(
        upload_to=access_level_subject_icon_hovered_path,
        validators=[
            validate_image,
            FileExtensionValidator(["png", "jpg", "svg", "jpeg"]),
        ],
        blank=True,
        null=True,
        help_text="آیکن هاور شده موضوع",
    )

    large_icon = models.FileField(
        upload_to=access_level_subject_large_icon_path,
        validators=[
            validate_image,
            FileExtensionValidator(["png", "jpg", "svg", "jpeg"]),
        ],
        blank=True,
        null=True,
        help_text="آیکن بزرگ هاور شده موضوع",
    )

    large_hovered_icon = models.FileField(
        upload_to=access_level_subject_large_icon_hovered_path,
        validators=[
            validate_image,
            FileExtensionValidator(["png", "jpg", "svg", "jpeg"]),
        ],
        blank=True,
        null=True,
        help_text="آیکن بزرگ هاور شده موضوع",
    )

    display_name = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text="اسمی که نمایش داده میشه",
    )
    display_name_eng = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text="english name for show",
    )

    importance = models.IntegerField(
        blank=True,
        null=True,
        help_text="میزان اهمیت موضوع. برای sort کردن موضوعات در ساید بار",
    )

    description = models.TextField(
        blank=True,
        null=True,
        help_text="توضیحات راجع به این موضوع",
    )

    index = models.FloatField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.display_name

    class Meta:
        ordering = ("index",)


class AccessLevelGroup(TimeStampedModel):
    """گروه ها همان منوهایی هستند که در هر موضوع وجود دارند"""

    access_level_subject = models.ForeignKey(
        AccessLevelSubject,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="موضوعی که منو در آن وجود دارد",
    )

    name = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        unique=True,
        help_text="اسم منو که به عنوان url استفاده می‌شه",
    )

    display_name = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text="اسم منو جهت نمایش",
    )
    display_name_eng = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text="name to show , in english",
    )
    
    description = models.TextField(
        blank=True,
        null=True,
        help_text="توضیحات درباره منو",
    )

    index = models.FloatField(
        blank=True,
        null=True,
    )
    hide = models.BooleanField(
        blank=False, default=False, help_text="جهت عدم نمایش باید مقدار true شود"
    )

    def __str__(self):
        return self.display_name


class AccessLevelAction(TimeStampedModel):
    """
    وقتی که لازمه یک دکمه یا یک جزئیات در منو سطح دسترسی داشته باشه یک عدد اکشن می‌سازیم و با فرانت هماهنگ می‌کنیم.
    """

    access_level_group = models.ForeignKey(
        AccessLevelGroup,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        help_text="این اکشن مربوط به کدام منو است",
    )

    name = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        unique=True,
        help_text="اسم انگلیسی اکشن",
    )

    display_name = models.CharField(
        blank=True, null=True, max_length=200, help_text="اسم فارسی اکشن"
    )

    description = models.TextField(blank=True, null=True, help_text="توضیحات")

    def __str__(self):
        return self.display_name
