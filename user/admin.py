from django.contrib import admin
from user.models import (
    UserProfile,
    Captcha,
    EVFP,
    UserFiles
)
from user.my_authentication.aseman_token_auth import MyToken

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'mobile', 'fname', 'flname', 'is_active',
                    'is_superuser', 'email', 'role', 'is_real', 'direct_login')
    list_filter = ('is_active', 'is_superuser', 'role', 'is_real','direct_login')
    search_fields = ("mobile", "fname__contains", "flname__contains")

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserFiles)
admin.site.register(MyToken)
