from user.models import UserProfile
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import password_validation

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name','is_active' ,'last_name' ,'mobile' , 'department' , 'role' , 'password']

    def create(self, validated_data):
        print("adibnia is very very  "  )
        if "password" in validated_data:
            
            validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)