from user.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation

###### serializer to show ######
class show_UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','is_active' ,'last_name' , 'department' , 'role' , 'created_by']



###### serializer to create ######
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','is_active' ,'last_name' ,'mobile' , 'department' , 'role' , 'password' , 'created_by']
        extra_kwargs = {'password': {'write_only': True} , 'created_by': {'write_only': True} }

    def create(self, validated_data):
        if "password" in validated_data:
            
            validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)

