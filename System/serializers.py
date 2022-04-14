from dataclasses import fields
from unicodedata import category
from rest_framework import serializers
from user.serializers import UserSerializer
from .models import File ,Answer, Tag ,Ticket,Category
from user.models import UserProfile
from department.serializers import DepartmentSerializer , ShowDepartmentSerializer
from icecream import ic
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
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
    file_fields = serializers.SerializerMethodField()
    
    def get_file_fields(self, obj):
        
        if self.context['with_files']: # add files if user has requested it 
            ic('adding files to the tickets')
            files = File.objects.filter(ticket = obj)
            serializer = FileSerializer(files , many = True)
            return serializer.data
        else:
            return None

        
    class Meta:
        model = Ticket
        fields = "__all__" 
        

    


class ShowAnswerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    ticket = ShowTicketSerializer()
    class Meta:
        model = Answer
        fields = ['ticket', 'sender', 'text']       

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
        extra_kwargs = {'e_name': {'required': True} , 'f_name': {'required': True}}

class TicketSerializer(serializers.ModelSerializer):
        model = Ticket
        fields = ['id','title','department','user','operator','created_by','text' ,'tags', 'is_answered','status','kind','priority','sub_category' , 'category', 'deleted', 'file_fields' , ]
        extra_kwargs = {'title': {'required': True} , 'text': {'required': True} , 'user': {'required': True} , 'sub_category': {'required': True} , 'category': {'required': True} , 'kind': {'required': True} , 'created_by':  { 'required': True}}
        

class AnswerSerializer(serializers.ModelSerializer):
    file_fields = serializers.SerializerMethodField()
    class Meta:
        model = Answer
        fields = ['id' ,'ticket', 'sender', 'text' , 'reciever' ,'to_department' , 'file_fields']       
        extra_kwargs= {'sender': {'required': True} , 'reciever': {'required': True}}

    def get_file_fields(self, obj):
        files = File.objects.filter(answer = obj)
        serializer = FileSerializer(files , many = True)
        return serializer.data

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id' , 'name', 'file_field' , 'ticket' , 'answer']
        extra_kwargs = {'file_field': {'required': True} ,'ticket': {'required': True} , 'answer': {'required': True}}
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ='__all__'
        extra_kwargs = {'name': {'required': True}} 

class SerachTicketSerializer(DepartmentSerializer):
    class Meta:
        model = Ticket
        fields = [ 'id',
            'title',
            'text',
            'is_answered',
            'kind',
            'status',
            'priority']
