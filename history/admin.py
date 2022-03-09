from history.models import User_log
from django.contrib import admin

# Register your models here.


class userLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "ip_address",
        "browser",
        "os",
        "date",
        "log_kind"
    )
    empty_value_display = "-empty-"
    search_fields = ("user", "ip_address")


admin.site.register(User_log, userLogAdmin)
