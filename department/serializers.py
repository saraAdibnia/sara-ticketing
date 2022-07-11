from department.models import Department
from rest_framework import serializers

class ShowDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'
        extra_kwargs ={'ename' : {'required' : True} , 'fname' : {'required' : True}}