from rest_framework import serializers
from user.serializer import show_UserProfileSerializer
from .models import Department ,File ,Answer, Tag ,Ticket,Category
from user.models import UserProfile

###### serializer to show ######
        
class show_departmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['name']


class show_tagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['e_name' , 'f_name']

class show_ticketSerializer(serializers.ModelSerializer):
    user = show_UserProfileSerializer()
    department = show_departmentSerializer()
    tags = show_tagSerializer()
    operator = show_UserProfileSerializer()
    created_by = show_UserProfileSerializer()
    class Meta:
        model = Ticket
        fields = ['title' , 'text' , 'department' , 'tags' ,'kind' , 'status'] 

class show_answerSerializer(serializers.ModelSerializer):
    user = show_UserProfileSerializer()
    ticket = show_ticketSerializer()
    class Meta:
        model = Answer
        fields = ['ticket', 'user', 'text']       

class show_fileSerializer(serializers.ModelSerializer):
    ticket = show_ticketSerializer()
    answer = show_answerSerializer()
    class Meta:
        model = File
        fields = [ 'name', 'file_field' , 'ticket']

class show_categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ 'name' ,'parent']

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

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name' )

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name' ,'sub_categories']
        
    @staticmethod
    def get_sub_categories(obj):
        return SubCategorySerializer(obj.categories, many=True, read_only=True).data