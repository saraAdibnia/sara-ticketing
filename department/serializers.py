from department.models import Department
from rest_framework import serializers

class ShowDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['e_name' , 'f_name']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [ 'id','e_name' , 'f_name']
        extra_kwargs ={'e_name' : {'required' : True} , 'f_name' : {'required' : True}}