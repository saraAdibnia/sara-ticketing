from rest_framework import permissions
from user.models import User
from accesslevel.models import AccessLevelGroup

class MyAccessLevelViewSubmitPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        
        needed_access_level_obj_id = AccessLevelGroup.objects.filter(name='accesslevel_request').first().id

        user_obj = User.objects.filter(
            id=request.user.id,
            common_access_level__groups=needed_access_level_obj_id
        ).first()

        return bool(request.user and request.user.is_authenticated and request.user.role==1) and bool(user_obj)



