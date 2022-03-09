from accesslevel.serializers import (
    CommonAccessLevelSerializer,
    CommonAccessLevelShowSerializer,
    simpleCommonAccessLevelSerializer,
)
from accesslevel.models.common_users import CommonAccessLevel

### kind = 1 -> full accessLevelReport  kind =2 -> simple - only accessLevel info
def userAccessLevel(user, kind):
    userAccessLevel_obj = CommonAccessLevel.objects.filter(
        id=user.common_access_level.id
    ).last()

    if kind == 1:
        userAccessSerialized = CommonAccessLevelShowSerializer(
            userAccessLevel_obj, many=False
        )

    else:
        userAccessSerialized = simpleCommonAccessLevelSerializer(
            userAccessLevel_obj, many=False
        )

    return userAccessSerialized.data


def userAccessGroup(user):
    pass
