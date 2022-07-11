from multiprocessing.sharedctypes import Value
from re import T
from tkinter.tix import FileSelectBox
from elasticsearch import serializer
from isort import file
from System.documents import TicketDocument
from System.permissions import EditTickets, IsOperator
from user import serializers
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from System.serializers import SerachTicketSerializer, TicketSerializer, ShowAnswerSerializer,AnswerSerializer , FileSerializer , TagSerializer , CategorySerializer , ShowSubCategorySerializer , ShowTicketSerializer
from System.serializers import TicketSerializer, ShowAnswerSerializer,AnswerSerializer , FileSerializer , TagSerializer , CategorySerializer , ShowSubCategorySerializer , ShowTicketSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics , filters
import json
from utilities.pagination import CustomPagination
import datetime
from icecream import ic
from user.serializers import UserSimpleSerializer
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView ,OpenApiParameter
from drf_spectacular.utils import extend_schema, extend_schema_view
from drf_spectacular.openapi import AutoSchema
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse
import os
class ListTickets(APIView):
    """
    a compelete list of tickets with file (if with_files is True) and a filtered list of tickets . The filter is on 'is_answered' , 'user_id' ,'created_dated__date__range' , 'title__icontains','text__icontains' , 'department_id' , 'id' , 'tag' fields. 
    This api is just for operator user.
    """
    permission_classes = [IsOperator , IsAuthenticated]
    pagination_class = CustomPagination()
    
    def get(self, request):
        filter_keys = ['is_answered' , 'user_id' ,'created__date__range' , 'title__icontains',
        'text__icontains' , 'department_id' , 'id' , 'tag' , 'status'  , 'operator']
        context = {'with_files': request.query_params.get('with_files', False), }
        sort = request.query_params.get('sort' , 'created') # check to whether shows the file or not
        validated_filters = dict()
        for key , value in request.query_params.dict().items():
            if key in filter_keys:
                validated_filters[key] = value
                    
        tickets= Ticket.objects.filter(**validated_filters ).order_by(sort)
        ic(type(tickets))
        page = self.pagination_class.paginate_queryset(queryset = tickets ,request =request, )            
        serializer = ShowTicketSerializer(page, many=True, context = context)
            # if serializer.modified > datetime.datetime.now() + datetime.timedelta(days=30) & serializer.is_answered == False:
            #     serializer.is_suspended = True
            #     serializer.save()
        return self.pagination_class.get_paginated_response(serializer.data)
class CreateTickets(APIView):
    """
    create tickets by getting title, text, user, sub_category, category, kind and tags in form body.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            request.data._mutable=True
        except:
            pass
        
        # #1 create a list of tags from comming data (form-data/ json)
        # #2 remove the tags string or list from request.data 
        tags = request.data.get("tags", [] )
        try:# if data comming from a formddata
            tags = json.loads(tags)

        except:
            pass
        
        try:
            request.data.pop('tags')
        except:
            pass

        #3 saving data and create a new ticket 
        if not request.data.get("user"):
            request.data['user']= request.user.id

        request.data['created_by']  = request.user.id

        print(request.data)
        serializer = TicketSerializer(data=request.data, many = False)
        ic(request.data)
        if serializer.is_valid():
            ticket =serializer.save()
            ic(tags)
            # add tags list to the created ticket.

            ticket.tags.add(*tags)
            return Response({"succeeded":True}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class DeleteTickets(generics.UpdateAPIView):
    """
    suspend tickets by getting their id in params and only if a user is the owner of the ticket has access to it.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    def get_object(self):
        return Ticket.objects.get(id = self.request.query_params.get('id'))
    
    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket.deleted = True
        ticket.status = 0
        ticket.save()
        return Response({'succeeded':True}, status=200)

class ListAnswers(generics.ListAPIView):
    """
     list of all answers of a ticket to corporate user by getting the id of ticket in params.
     And to normal user shows just answers that the reciever is the user themselves.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = ShowAnswerSerializer
    def get_queryset(self):
        queryset = Ticket.objects.get(id = self.request.query_params.get('id'))
        if self.request.user.role == 0 :
            answers =  Answer.objects.filter(receiver = self.request.user , ticket = queryset ) 
        else:
            answers =  Answer.objects.filter(ticket = queryset )
        return answers

class CreateAnswers(APIView):
    """
     create answers for specific ticket(requests the id of tickets in body form) by getting sender(in form body) and reciever, then the status of the ticket become jari(1).

    """
    permission_classes = [IsAuthenticated & IsOperator ]
    def post(self, request):
        try:
            request.data._mutable=True
        except:
            pass
        # request.data['sender']= request.user.id
        serializer = AnswerSerializer(data=request.data)
        request.data['sender'] = request.user.id
        ticket =Ticket.objects.get(id = request.data['ticket'])
        # file = File.objects.get("files" ,[])
        if not request.data.get("reciever"):
            request.data['reciever'] = ticket.user.id
        if request.data['to_department']:
                department = Department.objects.get(id = request.data['to_department'])
                ticket.department = department.id
        if serializer.is_valid():
            if not (request.data['sender'] == ticket.user.id or request.data['sender'] == ticket.created_by.id) and ticket.status == 2:
                ticket.status = 1
            else:
                pass
            ticket.deleted = False
            ticket.save()
    
            serializer.save()
            return Response({'succeeded' : True}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteAnswers(generics.UpdateAPIView):
    """
    suspend answers by getting their id in params.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    def get_object(self):
        return Answer.objects.get(id = self.request.query_params.get('id'))
    
    def update(self, request, *args, **kwargs):
        answer = self.get_object()
        answer.deleted = True
        answer.save()
        return Response({'succeeded':True}, status=200)

class ListFiles(generics.ListAPIView):
    """
    a compelete list of files for spcefic ticket or specific answer.(by getting ticket_id or answer_id in params)

    """
    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = FileSerializer
    def get_queryset(self):
        if self.request.query_params.get('ticket_id',None):
            queryset =  File.objects.filter(ticket= self.request.query_params.get('ticket_id'))
        elif self.request.query_params.get('answer_id'):
            queryset =  File.objects.filter(answer= self.request.query_params.get('answer_id'))
        return queryset

class CreateFiles(APIView):
    """
    upload files by getting file, ticket id and answer id in form body.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    def post(self ,request):
        file_data = list()
        for file in  request.FILES:
            ic(type(file))
            file_data.append({
                'ticket' : request.data.get('ticket') ,
                'answer' : request.data.get('answer') ,
                'file' : request.data[file],
                'name' : request.FILES[file].name,
                'url' :request.data.get('url')
            })
            
        # by this you avoiding saving files if any of them has a problem and just return the error of the incorrect file
        serializer = FileSerializer(data = file_data, many = True)
        if serializer.is_valid():
            serializer.save()
        else:
                return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
        return Response({'succeed':'ok'}, status = status.HTTP_201_CREATED)



class ListTags(APIView):
    """
    a compelete list of tags.

    """
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination()
    def get(self, request , format=None):
        sort = request.query_params.get('sort' , 'created')
        tags =  Tag.objects.all().order_by('-'+sort)
        page = self.pagination_class.paginate_queryset(queryset = tags ,request =request)
        serializer = TagSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

class CreateTags(generics.CreateAPIView ):
    """
    create tags by getting their fname and ename in form body.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = TagSerializer
    pagination_class = CustomPagination()

class UpdateTags(APIView):
    """
    update fname and ename of tags(in form body) by getting their id (in params).

    """
    pagination_class = CustomPagination()
    permission_classes = [IsAuthenticated]
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
    delete tags by getting their id in params and only operators has access to it.

    """
    pagination_class = CustomPagination()
    permission_classes = [IsOperator , IsAuthenticated]
    serializer_class = TagSerializer
    def get_object(self):
        return Tag.objects.get(id = self.request.query_params.get('id'))

class ListOfCategories(APIView):
    """
    List of sub categories of a category or the category of some sub categories.(if in params give the parent it responses the childes(subs))

    """
    pagination_class = CustomPagination()
    permission_classes = [IsAuthenticated]

    def get(self  ,request):

        try:
            sort= request.query_params.get('sort' , 'created')
            if request.query_params.get("parent"): #get children
                parent = Category.objects.get(id=  request.query_params.get("parent"))
                categories = Category.objects.filter(parent =parent ).order_by('-'+sort)

            elif request.query_params.get("sub"):#get parent
                child = Category.objects.get(id = request.query_params.get("sub"))
                categories = Category.objects.filter( parent   = child.parent.id).order_by('-'+sort)

            else: #get all parents
                categories = Category.objects.filter(parent__isnull = True).order_by('-'+sort)


            page = self.pagination_class.paginate_queryset(queryset = categories ,request =request)
            serializer = ShowSubCategorySerializer(page , many=True)
            return self.pagination_class.get_paginated_response(serializer.data)

        except ObjectDoesNotExist:
            return Response({'error': 'existance error', }, status= 404)

class CreateCategories(generics.CreateAPIView):
    """
    create categories by getting their fname and ename in form body and create sub categories by getting fname and ename and also parent id in form body.

    """
    permission_classes = [IsOperator  , IsAuthenticated]
    serializer_class = CategorySerializer
    pagination_class = CustomPagination()

class UpdateCategories(APIView):
    """
    update category by getting their id in params and and only operator has access to it and can update fname and ename of category in form body  .

    """
    pagination_class = CustomPagination()
    permission_classes = [ IsOperator,IsAuthenticated]
    def patch(self , request ):
            category_id = request.query_params.get("id")
            category =Category.objects.get(id = category_id)
            serializer = CategorySerializer(instance = category , data=request.data , partial=True)
            self.check_object_permissions(request, serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCategories(generics.DestroyAPIView):
    """
    delete tags by getting their id.

    """
    pagination_class = CustomPagination()
    permission_classes = [IsOperator , IsAuthenticated]
    serializer_class = CategorySerializer
    def get_object(self):
        return Category.objects.get(id = self.request.query_params.get('id'))


class PaginatedElasticSearch(APIView):
    """
    search in title of tickets. by elastic serach and serach the title in params.

    """
    permission_classes = [IsAuthenticated]
    serializer_class = SerachTicketSerializer
    document_class = TicketDocument
    def get(self, request):
        search = self.document_class.search().query("match" , title = self.request.query_params.get("search"))
        response = search.execute()
        serializer = self.serializer_class(response, many=True)
        return Response(serializer.data)

class ListMyTicket(generics.ListAPIView):
    """
    List of tickets for normal user and customer(user with role =2)
    """
    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = TicketSerializer
    def get_queryset(self):
        if self.request.user.role == 0 :
            tickets =  Ticket.objects.filter(Q (user = self.request.user) | Q (operator = self.request.user))
        else:
            tickets =  Ticket.objects.all()
        return tickets

class TagNormalSerach(generics.ListAPIView):
    """
    search in tags of tickets. by word 'serach' in params.

    """
    permission_classes = [IsAuthenticated]
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["id","fname", "ename"]

class TicketNormalSearch(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    filter_backends  = [filters.SearchFilter]
    search_fields = ['title' ,'text' ,'department' ,'status' ,'kind' ,'priority', 'category' ,'sub_category']