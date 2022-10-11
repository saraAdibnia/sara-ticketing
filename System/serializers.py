from ast import operator
from rest_framework import serializers
from user.models.user import User
from user.serializers import UserProfileSerializer ,  UserProSerializer , UserSerializer , ShowSignitureSerializer
from .models import File ,Answer, Review, Tag ,Ticket,Category
from department.serializers import DepartmentSerializer , ShowDepartmentSerializer 
from icecream import ic
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from System.documents import TicketDocument
from rest_framework.serializers import ValidationError
from rest_framework import filters
###### serializer to show ######
        

class ShowTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['ename' , 'fname' , 'created' , 'modified']


class ShowCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields =  '__all__'

class ShowSubCategorySerializer(serializers.ModelSerializer):
    parent = ShowCategorySerializer()
    class Meta:
        model = Category
        fields = '__all__'


    def create(self, validated_data):
        parent = Category.objects.filter(**validated_data)
        return parent


class ShowTicketSerializer(serializers.ModelSerializer):
    user = UserProSerializer()
    department = ShowDepartmentSerializer()
    tags = ShowTagSerializer()
    operator = UserProSerializer()
    created_by = UserProSerializer()
    sub_category  = ShowSubCategorySerializer()
    category = ShowCategorySerializer()
    file_fields = serializers.SerializerMethodField()
    def get_file_fields(self, obj):
        
        if self.context.get('with_files'): # add files if user has requested it 
            ic('adding files to the tickets')
            files = File.objects.filter(ticket = obj)
            serializer = FileSerializer(files , many = True)
            return serializer.data
        else :
            return None
    class Meta:
        model = Ticket
        fields = "__all__" 
    

class ShowAnswerSerializer(serializers.ModelSerializer):
    file_fields = serializers.SerializerMethodField()
    ticket = ShowTicketSerializer()
    to_department = ShowDepartmentSerializer()
    sender = UserProSerializer()
    reciever = UserProSerializer()
    
    class Meta:
        model = Answer
        fields = ['id' , 'ticket', 'sender', 'text' , 'created' , 'modified' , 'reciever' ,  'file_fields' ,'deleted' ,'to_department' ]       
    def get_file_fields(self, obj):
        files = File.objects.filter(answer = obj)
        serializer = FileSerializer(files , many = True)
        return serializer.data
class ShowFileSerializer(serializers.ModelSerializer):
    ticket = ShowTicketSerializer()
    answer = ShowAnswerSerializer()
    class Meta:
        model = File
        fields = '__all__'
class ShowReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ShowReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['reaction']
###### serializer to create ######


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"
        extra_kwargs = {'fname': {'required': True}}

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"
        extra_kwargs = {'title': {'required': True} , 'text': {'required': True} , 'user': {'required': True} , 'sub_category': {'required': True} , 'category': {'required': True} , 'kind': {'required': True} , 'created_by':  { 'required': True}}
        

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id' ,'ticket', 'sender', 'text' , 'reciever' ,'to_department' , 'created' , 'modified' ,'deleted']       
        extra_kwargs= {'text': {'required': True}}

    

class FileSerializer(serializers.ModelSerializer):
    # file_count = serializers.SerializerMethodField()
    class Meta:
        model = File
        fields = '__all__'
        extra_kwargs= {'file': {'required': True}}
    def validate(self , data):
        ic()
        empty_list = [0 , None , '' , ' ']
        if data.get('ticket' , None) in empty_list  and data.get('answer' , None) in empty_list :
           raise ValidationError("ticket either answer must not be null ")
        return super().validate(data)

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields ="__all__"
        extra_kwargs = {'fname': {'required': True}} 

class SerachTicketSerializer(DocumentSerializer):
    class Meta:
        document = TicketDocument
        fields = [ 'id',
            'title',
            'text',
            'is_answered',
            'kind',
            'status',
            'priority']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {'user' : {'required' : True} } 
        
class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id' , 'reaction']
        extra_kwargs = {'reaction' : {'required' : True}}
