from department.models import Department
from rest_framework import serializers

class ShowDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [ 'id','name']
        extra_kwargs ={'name' : {'required' : True}}