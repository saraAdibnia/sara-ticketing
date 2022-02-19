from rest_framework import serializers
from .models import Department ,File ,Answer ,Ticket,User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'mobile', 'department']


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id' ,'title', 'user', 'department' ,'text', 'is_answered' ,'tag' ]

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['ticket', 'user', 'text', 'operator']

class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = ['name', 'user', 'patch', 'ticket' ,'file_filed']
        
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = [ 'id','name']