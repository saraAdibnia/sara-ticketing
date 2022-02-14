from rest_framework import serializers
from .models import Department ,File ,Answer ,Ticket,User
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'mobile', 'department']


class TicketSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ticket
        fields = ['url', 'subject', 'user', 'department', 'operator', 'is_answered' ,'created_date' ,'modified_date','text']

class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Answer
        fields = ['url', 'ticket', 'user', 'text', 'operator','created_date' ,'modified_date']

class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['url', 'name', 'user', 'patch', 'ticket' ,'created_date' ,'modified_date']
        
class DepartmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Department
        fields = ['url', 'name', 'user','created_date' ,'modified_date']