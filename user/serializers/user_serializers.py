from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.contrib.auth.hashers import make_password
# from drf_extra_fields import geo_fields
from user.models import UserProfile, Captcha, EVFP, UserFiles


# class UserProfileInfoSerializer(ModelSerializer):

#     office = OfficeSerializer(read_only=True)
#     common_access_level = simpleCommonAccessLevelSerializer(read_only=True)
#     country = CountryNameSerializer()
#     city = CityShowSerializerForUser()
#     state = StateShowSerialzerForUser()

#     class Meta:
#         model = UserProfile
#         fields = ['id', 'mobile', 'fname', 'flname', 'ename', 'elname', 'email',
#                   'profile_image', 'role', 'common_access_level', 'office', 'is_active', 'is_real', 'state', 'country', 'city', ]


class UserProfileSimpleSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['id', 'mobile', 'fname', 'flname', 'ename', 'elname', 'email',
                  'profile_image', 'role',  'is_active', 'is_real']


class UserSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {
            'password': {
                'write_only': True,
            },
            'temp_password': {
                'write_only': True,
            }
        }


class QuickUserSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        # fields = '__all__'
        exclude = ['is_superuser',
                   'password', 'temp_password', 'needs_to_change_pass']


class UserEditSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ['mobile', 'is_superuser', 'password', 'temp_password',
                   'is_staff', 'groups', 'user_permissions', 'last_login',  'role', 'needs_to_change_pass', ]


class UserPermSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        exclude = ['is_superuser', 'password', 'temp_password', 'is_active', 'is_staff', 'groups',
                   'user_permissions', 'last_login',  'role', 'needs_to_change_pass', 'source_code', 'created_by', ]


# class UserShowSerializer(ModelSerializer):
#     city = CityShowSerializerForUser(read_only=True)
#     state = StateShowSerialzerForUser(read_only=True)
#     country = CountryShowSerializerForUser(read_only=True)
#     common_access_level = simpleCommonAccessLevelSerializer(read_only=True)
#     office = OfficeShowSerializer()
#     marketer = UserProfileInfoSerializer()

#     class Meta:
#         model = UserProfile
#         exclude = ['is_superuser', 'password', 'temp_password',
#                    'is_staff', 'groups', 'user_permissions', ]


class UserProfileQuickSerilaizer(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = "__all__"


class UserProfileSerializer(ModelSerializer):
    """serializes a user profile object """

    class Meta:
        model = UserProfile
        fields = ('__all__')
        # extra_kwargs = {
        #     'password': {
        #         'write_only': True,
        #         'style': {'input_type': 'password'}
        #     },
        #     'temp_password': {
        #         'write_only': True,
        #         'style': {'input_type': 'password'}
        #     }
        # }

    def create(self, validated_data, format=None):
        """"creates and returns a new user"""

        user = UserProfile.objects.create_user(
            password=make_password(validated_data.get('password')),
            mobile=validated_data.get('mobile', ""),
            email=validated_data.get('email', ""),
            role="0"
        )
        user.save()

        return user

    def update(self, instance, validated_data):

        instance.password = make_password(
            validated_data.get('password'), instance.password)
        instance.temp_password = make_password(
            validated_data.get('temp_password'), instance.temp_password)

        instance.save()

        return instance


# class UserAccessLevelSerializer(ModelSerializer):

#     class Meta:
#         model = UserProfile
#         fields = (
#             'id',
#             'offices',
#         )


class UserPerNameFNameSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("id", "fname", "flname")


class UserEngNameFNameSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("ename", "elname")


class UserEngPerNameFNameSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("ename", "elname", "fname", "flname")


class UserSimpleSerializer(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ("id", "mobile", "fname", "flname", "ename")


class UserFilesSerialzier(ModelSerializer):
    class Meta:
        model = UserFiles
        fields = "__all__"


class UserBirthdaysSerialzier(ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ['fname', 'ename', 'flname',
                  'elname', 'birthday', 'role', 'mobile']
