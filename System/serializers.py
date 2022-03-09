from unicodedata import category
from rest_framework import serializers
from user.serializers import UserSerializer
from .models import File ,Answer, Tag ,Ticket,Category
from user.models import UserProfile
from department.serializers import DepartmentSerializer , ShowDepartmentSerializer

###### serializer to show ######
        

class ShowTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['e_name' , 'f_name']


class ShowCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [ 'name' ,'parent']

class ShowSubCategorySerializer(serializers.ModelSerializer):
    parent = ShowCategorySerializer()
    class Meta:
        model = Category
        fields = ['name', 'parent']

class ShowTicketSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department = ShowDepartmentSerializer()
    tags = ShowTagSerializer()
    operator = UserSerializer()
    created_by = UserSerializer()
    sub_category  = ShowSubCategorySerializer()
    category = ShowCategorySerializer()
    class Meta:
        model = Ticket
        fields = ['title' , 'text' , 'department' , 'tags' ,'kind' , 'status'] 

class ShowAnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    ticket = ShowTicketSerializer()
    class Meta:
        model = Answer
        fields = ['ticket', 'user', 'text']       

class ShowFileSerializer(serializers.ModelSerializer):
    ticket = ShowTicketSerializer()
    answer = ShowAnswerSerializer()
    class Meta:
        model = File
        fields = [ 'name', 'file_field' , 'ticket']



###### serializer to create ######


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = [ 'id','e_name' , 'f_name']

class TicketSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    class Meta:
        model = Ticket
        fields = ['id','title','department','user','operator','created_by','text' ,'tags', 'is_answered','status','kind','priority','sub_category']
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id' ,'ticket', 'user', 'text' , 'to_operator' ,'to_department']       

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id' , 'name', 'file_field' , 'ticket']

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ='__all__'
