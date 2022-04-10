from ast import keyword
from importlib.abc import ExecutionLoader
from logging import exception
from webbrowser import get
from django.test import tag
from System.permissions import EditTickets
from accesslevel.permissions import MyAccessLevelViewSubmitPermission
from user.serializers.user_serializers import UserProfileSerializer , UserProfileSimpleSerializer
from .models import *
from datetime import timedelta , datetime
from django.shortcuts import render
from django.template import RequestContext
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from django.http import Http404
from rest_framework import status
from System.serializers import TicketSerializer , AnswerSerializer , FileSerializer , TagSerializer , CategorySerializer , ShowSubCategorySerializer , ShowTicketSerializer
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import json
from utilities.pagination import CustomPagination


class ListTickets(APIView):
    """
    a compelete list of tickets and a filtered list of tickets   

    """
    pagination_class = CustomPagination()
    def get(self, request):  
        tickets =  Ticket.objects.all()
        page = self.pagination_class.paginate_queryset(queryset = tickets ,request =request)
        serializer = TicketSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)
    
    def post(self , request):
        filter_keys = ['is_answered' , 'user_id' ,'created_dated__date__range' , 'title__icontains',
        'text__icontains' , 'department_id' , 'ticket_id' , 'tag_id' ]
        validated_filters =[]
        f_dict = request.query_params.dict()
        for key , value in f_dict.items():
            if key in filter_keys:
                validated_filters[key] = value
        ticket = Ticket.objects.filters(**validated_filters)
        page = self.pagination_class.paginate_queryset(queryset = ticket ,request =request)
        serializer = TicketSerializer(page , many = True)
        return self.pagination_class.get_paginated_response(serializer.data)
    
class CreateTickets(APIView):
    """
    create tickets by getting title, text, user, sub_category, category, kind and tags.

    """
    permission_classes = [EditTickets]
    def post(self, request):
        request.data._mutable=True
        #1 create a list of tags from comming data (form-data/ json)
        #2 remove the tags string or list from request.data 
        tags = request.data.get("tags")
        print(type(tags))
        try:# if data comming from a formddata
            tags = json.loads(tags)
        except:
            pass
        request.data.pop('tags')
        print('this is type :' , type(tags))
        print('this is the data  tags :' ,tags)
        #3 saving data and create a new ticket 
        if request.data.get("user") == None:
            request.data['user']= request.user.id
        serializer = TicketSerializer( data=request.data)
        if serializer.is_valid():
            ticket =serializer.save()
            # add tags list to the created ticket 
            ticket.tags.add(*tags)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class DeleteTickets(generics.UpdateAPIView):
    """
    suspend tickets by getting their id.

    """
    permission_classes = [EditTickets]
    def get_object(self):
        return Ticket.objects.get(id = self.request.query_params.get('id'))
    
    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket.deleted = True
        ticket.save()
        return Response({'success':True}, status=200)

class ListAnswers(generics.ListAPIView):
    """
     list of all answers of a ticket to corporate user by getting the id of ticket.
     And to normal user shows just ansewrs that the reciever is the user themselves.

    """
    permission_classes = [EditTickets]
    serializer_class = AnswerSerializer
    def get_queryset(self):
        queryset = Ticket.objects.get(id = self.request.data['id'])
        if self.request.user.role == 0 :
            answers =  Answer.objects.filter(receiver = self.request.user , ticket = queryset)
        else:
            answers =  Answer.objects.filter(ticket = queryset)
        return answers

class CreateAnswers(APIView):
    """
     create answers for specific ticket(by getting the id og tickets) by getting sender and reciever and then the status of the ticket become jari(1).

    """
    permission_classes = [EditTickets]
    def post(self, request):
        request.data._mutable=True
        request.data['sender']= request.user.id
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ticket =Ticket.objects.get(id = request.data['ticket'])
            ticket.status = 1
            ticket.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteAnswers(generics.UpdateAPIView):
    """
    suspend answers by getting their id.

    """
    permission_classes = [EditTickets]
    def get_object(self):
        return Answer.objects.get(id = self.request.query_params.get('id'))
    
    def update(self, request, *args, **kwargs):
        answer = self.get_object
        answer.deleted = True
        answer.save()
        return Response({'success':True}, status=200)

class ListFiles(generics.ListAPIView):
    """
    a compelete list of files.

    """
    permission_classes = [EditTickets]
    queryset  = File.objects.all()
    serializer_class = FileSerializer
    

class CreateFiles(APIView):
    """
    upload files by getting file_field, ticket id and answer id.

    """
    permission_classes = [EditTickets]
    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListTags(APIView):
    """
    a compelete list of tags.

    """
    pagination_class = CustomPagination()
    def get(self, request , format=None):  
        tags =  Tag.objects.all()
        page = self.pagination_class.paginate_queryset(queryset = tags ,request =request)
        serializer = TagSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

class CreateTags(generics.CreateAPIView ):
    """
    create tags by getting a f-name and e-name.

    """
    permission_classes = [EditTickets]
    serializer_class = TagSerializer


class UpdateTags(APIView):
    """
    update tag's name by their id.

    """
    def patch(self , request ):
            Tag_id = request.query_params.get("id")
            tag_updateing = Tag.objects.get(id = Tag_id)
            serializer = TagSerializer(tag_updateing , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTags(generics.DestroyAPIView):
    """
    delete tags by getting their id.

    """
    permission_classes = [EditTickets]
    serializer_class = TagSerializer
    def get_object(self):
        return Tag.objects.get(id = self.request.query_params.get('id'))

class ListCategories(generics.ListAPIView):
    """
    a compelete list of tags.

    """
    permission_classes = [EditTickets]
    queryset  = Category.objects.all()
    serializer_class = CategorySerializer

class CreateCategories(generics.CreateAPIView):
    """
    create categories by getting a name and create sub categories by getting name and parent id.

    """
    permission_classes = [EditTickets]
    serializer_class = CategorySerializer

class UpdateCategories(APIView):
    """
    update category by their id.

    """
    def patch(self , request ):
        # print(request.query_params)
        # print(request.data)
            category_id = request.query_params.get("id")
            category =Category.objects.get(id = category_id)
            serializer = CategorySerializer(instance = category , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCategories(APIView):
    """
    delete categories by getting their id.

    """
    def delete(self , request):
            category_id = request.query_params.get("id")
            category = Category.objects.get(id = category_id)
            category.delete()
            return Response({'success':True}, status=200)

class ListOfCategories(APIView):
    """
    category of a sub category or list of sub categories of s a category.

    """
    pagination_class = CustomPagination()
    def get(self , request):
        if request.query_params.get("parent") != None:
            categories = Category.objects.filter(parent = request.query_params.get("parent"))
        else:
            categories = Category.objects.filter(parent__isnull = True)
        page = self.pagination_class.paginate_queryset(queryset = categories ,request =request)
        serializer = ShowSubCategorySerializer(page , many=True)
        return self.pagination_class.get_paginated_response(serializer.data)
