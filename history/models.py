from django.db import models

# Create your models here.


class User_log(models.Model):

    user = models.ForeignKey(
        "user.UserProfile",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    ip_address = models.CharField(
        max_length=100,
    )

    browser = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    os = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    device = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    for_admin = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )

    date = models.DateTimeField(
        auto_now_add=True
    )

    log_kind_choices = (
        (0, "ورود کاربر"),
        (1, "رمز اشتباه"),
        (2, "خروج کاربر"),
        (3, "توکن اشتباه"),

    )
    log_kind = models.SmallIntegerField(default=0,
                                        choices=log_kind_choices,
                                        help_text="نوع لاگ",)

    def __str__(self) -> str:
        return self.for_admin
