from rest_framework.serializers import ModelSerializer, SerializerMethodField

from department.serializers import DepartmentSerializer
from user.models import UserProfile
from accesslevel.models import (
    AccessLevelRequest,
    AccessLevelSubject,
    AccessLevelGroup,
    AccessLevelAction,
    CommonAccessLevel,
    CommonAccessLevelGroup,
    UserRowCountAccess

)


class AccessLevelSubjectSerializer(ModelSerializer):
    class Meta:
        model = AccessLevelSubject
        fields = "__all__"


class AccessLevelGroupSerializer(ModelSerializer):
    class Meta:
        model = AccessLevelGroup
        fields = "__all__"


class AccessLevelActionSerializer(ModelSerializer):
    class Meta:
        model = AccessLevelAction
        fields = "__all__"


class CommonAccessLevelGroupSerializer(ModelSerializer):
    class Meta:
        model = CommonAccessLevelGroup
        fields = "__all__"


class CommonAccessLevelSerializer(ModelSerializer):
    class Meta:
        model = CommonAccessLevel
        fields = "__all__"


class CommonAccessLevelSerializer(ModelSerializer):
    class Meta:
        model = CommonAccessLevel
        fields = "__all__"


class simpleCommonAccessLevelSerializer(ModelSerializer):
    class Meta:
        model = CommonAccessLevel
        exclude = ("subjects", "actions", "groups")


class CommonAccessLevelShowSerializer(ModelSerializer):
    def get_group(self, obj):
        query = obj.groups.all().order_by("index")
        access = AccessLevelGroupSerializer(query, read_only=True, many=True)
        return access.data

    subjects = AccessLevelSubjectSerializer(read_only=True, many=True)
    groups = SerializerMethodField(
        "get_group",
    )
    actions = AccessLevelActionSerializer(read_only=True, many=True)
    common_access_level_group = CommonAccessLevelGroupSerializer(
        read_only=True)

    class Meta:
        model = CommonAccessLevel
        fields = "__all__"


class UserInfoSerializer(ModelSerializer):

    department = DepartmentSerializer(read_only=True)
    common_access_level = CommonAccessLevelShowSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "mobile",
            "fname",
            "flname",
            "ename",
            "elname",
            "email",
            "profile_image",
            "role",
            "common_access_level",
            "department",
        ]


class AccessLevelRequestSerializer(ModelSerializer):
    class Meta:
        model = AccessLevelRequest
        fields = "__all__"


class AccessLevelRequestSubmitSerializer(ModelSerializer):
    class Meta:
        model = AccessLevelRequest
        fields = ("user", "negative", "office",
                  "common_access_level", "created_by")


class AccessLevelRequestProceedSerializer(ModelSerializer):
    class Meta:
        model = AccessLevelRequest
        fields = ("granted", "not_granted_desc", "granted_by", "office")


class AccessLevelRequestListSerializer(ModelSerializer):
    user = UserInfoSerializer()
    created_by = UserInfoSerializer()
    common_access_level = CommonAccessLevelShowSerializer()

    class Meta:
        model = AccessLevelRequest
        fields = (
            "id",
            "user",
            "created_by",
            "created",
            "negative",
            "granted",
            "common_access_level",
        )


class AccessLevelRequestShowSerializer(ModelSerializer):
    user = UserInfoSerializer()
    department = DepartmentSerializer()
    created_by = UserInfoSerializer()
    common_access_level = CommonAccessLevelSerializer()

    class Meta:
        model = AccessLevelRequest
        fields = "__all__"


class UserRowCountAccessSerializer(ModelSerializer):
    role = CommonAccessLevelSerializer()

    class Meta:
        model = UserRowCountAccess
        fields = "__all__"


class UserRowCountAccessCreateSerializer(ModelSerializer):
    class Meta:
        model = UserRowCountAccess
        fields = "__all__"
