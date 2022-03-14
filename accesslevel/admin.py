from django.contrib import admin

from accesslevel.models import (
    AccessLevelRequest,
    AccessLevelSubject,
    AccessLevelGroup,
    AccessLevelAction,
    CommonAccessLevelGroup,
    CommonAccessLevel,
    UserRowCountAccess
)


class AccessLevelGroupInLine(admin.TabularInline):
    model = AccessLevelGroup


class AccessLevelSubjectAdmin(admin.ModelAdmin):
    inlines = [AccessLevelGroupInLine]
    list_display = ("id", "name", "display_name", "description", "index")


class AccessLevelActionInLine(admin.TabularInline):
    model = AccessLevelAction


class AccessLevelGroupAdmin(admin.ModelAdmin):
    inlines = [AccessLevelActionInLine]
    list_display = (
        "id",
        "access_level_subject",
        "name",
        "display_name",
        "display_name_eng",
        "description",
        "index",
        "hide",
    )
    list_filter = ("access_level_subject",)


class CommonAccessLevelInLine(admin.TabularInline):
    model = CommonAccessLevel


class CommonAccessLevelGroupAdmin(admin.ModelAdmin):
    inlines = [CommonAccessLevelInLine]


admin.site.register(AccessLevelSubject, AccessLevelSubjectAdmin)
admin.site.register(AccessLevelGroup, AccessLevelGroupAdmin)
admin.site.register(CommonAccessLevelGroup, CommonAccessLevelGroupAdmin)
admin.site.register(AccessLevelRequest)
admin.site.register(CommonAccessLevel)
admin.site.register(UserRowCountAccess)
