from re import A
from rest_framework import serializers
from user.serializer import show_UserProfileSerializer
from .models import Department ,File ,Answer, Tag ,Ticket,Category
from user.models import UserProfile

###### serializer to show ######
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [ 'id','name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [ 'id','e_name' , 'f_name']

class TicketSerializer(serializers.ModelSerializer):
    user = show_UserProfileSerializer()
    department = DepartmentSerializer()
    tags = TagSerializer()
    operator = show_UserProfileSerializer()
    created_by = show_UserProfileSerializer()
    class Meta:
        model = Ticket
        fields = '__all__' 

class AnswerSerializer(serializers.ModelSerializer):
    user = show_UserProfileSerializer()
    ticket = TicketSerializer()
    class Meta:
        model = Answer
        fields = ['id' ,'ticket', 'user', 'text']       

class FileSerializer(serializers.ModelSerializer):
    ticket = TicketSerializer()
    answer = AnswerSerializer()
    class Meta:
        model = File
        fields = ['id' , 'name', 'file_field' , 'ticket']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name' ,'parent']

###### serializer to create ######

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [ 'id','name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [ 'id','e_name' , 'f_name']

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__' 

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id' ,'ticket', 'user', 'text']       

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id' , 'name', 'file_field' , 'ticket']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name' ,'parent']