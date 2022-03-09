from django.contrib import admin

# Register your models here.
from developinglogs.models import SMSLog, Mymodel, SmsSend, SmsCategory
from developinglogs.models import ReceivedSms

class SmsCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "title",
        "isActive",
        "sendByNumber",
        "kind"
    )
    empty_value_display = "-empty-"
    search_fields = ("title", "isActive")
    list_filter = ("sendByNumber",)


class SMSLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "params_receptor",
        "params_sender",
        "status",
        "smsCat",
    )
    empty_value_display = "-empty-"
    search_fields = ("params_receptor", "params_sender")
    list_filter = ("smsCat",)


admin.site.register(SMSLog, SMSLogAdmin)
admin.site.register(Mymodel)
admin.site.register(SmsSend)
admin.site.register(SmsCategory, SmsCategoryAdmin)
admin.site.register(ReceivedSms)
