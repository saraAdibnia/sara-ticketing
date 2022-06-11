from department.models import Department
from rest_framework import serializers

class ShowDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['ename' , 'fname']

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [ 'id','ename' , 'fname']
        extra_kwargs ={'ename' : {'required' : True} , 'fname' : {'required' : True}}