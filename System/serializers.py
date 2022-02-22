from rest_framework import serializers
from .models import Department ,File ,Answer, Tag ,Ticket,User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'mobile', 'department']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id' ,'title', 'user', 'department' ,'text', 'status' ,'tags' , 'is_answered']

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