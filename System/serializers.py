from rest_framework import serializers
from .models import Department ,File ,Answer, Tag ,Ticket,Category, UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['department','mobile']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id' ,'title', 'user', 'department' ,'text', 'status' ,'tags' , 'is_answered' ,'kind', 'priority' , 'created_by']

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id' ,'ticket', 'user', 'text']

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['id' , 'name', 'file_field' , 'ticket']
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [ 'id','name']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [ 'id','e_name' , 'f_name']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name' ,'parent']

