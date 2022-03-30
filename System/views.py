from ast import keyword
from importlib.abc import ExecutionLoader
from logging import exception
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
from rest_framework import viewsets
from rest_framework import permissions
from django.http import Http404
from rest_framework import status
from System.serializers import TicketSerializer , AnswerSerializer , FileSerializer , TagSerializer , CategorySerializer , ShowSubCategorySerializer , ShowTicketSerializer 
from department.serializers import DepartmentSerializer , ShowDepartmentSerializer
# from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
import json
from utilities.pagination import CustomPagination
# from django.conf import settings
# from rest_framework.authtoken.views import ObtainAuthToken 
# from rest_framework.settings import api_settings
# from rest_framework import viewsets
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from .models import Post
# from .serializers import PostSerializer
# from .permissions import UpdateOwnProfile
# 


# class UserLoginApiView(ObtainAuthToken):
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
# class TokenAuthentication(APIView):
#       def post(self, request):
#         token = Token.objects.get_or_create()
#         users =  UserProfile.objects.all()
#         serializer = UserSerializer(users = request.user , many=True)
#         if serializer.is_valid():
#             token.save()
#             return Response(token.key)

class ListTickets(APIView):
    # permission_classes = (IsAuthenticated ,)
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
    permission_classes = (EditTickets)
    # permission_classes = (IsAuthenticated ,)
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
    

# class UpdateTickets(APIView):
#     def patch(self , request ):
#             TicketId = request.query_params.get("id")
#             ticket = Ticket.objects.get(id = TicketId)
#             serializer = TicketSerializer(instance = ticket , data=request.data , partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
          
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteTickets(APIView):
    permission_classes = (EditTickets)
    def delete(self , request ):
            TicketId = request.query_params.get("id")
            ticket = Ticket.objects.get(id = TicketId)
            ticket.delete()
            return Response({'success':True}, status=200)


class ListAnswers(APIView):
    pagination_class = CustomPagination()
    permission_classes = [IsAuthenticated]
    def post(self, request ):
        ticket_id =Ticket.objects.get(id = request.data['id'])
        if request.user.role == 0 :
            answers =  Answer.objects.filter(receiver = request.user , ticket = ticket_id)
        else:
            answers =  Answer.objects.filter(ticket = ticket_id)
        page = self.pagination_class.paginate_queryset(queryset = answers ,request =request)
        serializer = AnswerSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

class CreateAnswers(APIView):
    permission_classes = (EditTickets)
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
    
# class UpdateAnswers(APIView):
#     def patch(self , request ):
#         # print(request.query_params)
#         # print(request.data)
#             AnswerId = request.query_params.get("id")
#             answer =Answer.objects.get(id = AnswerId)
#             serializer = AnswerSerializer(instance = answer , data=request.data , partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAnswers(APIView):
    permission_classes = (EditTickets)
    def delete(self , request):
            AnswerId = request.query_params.get("id")
            answer = Answer.objects.get(id = AnswerId)
            answer.status = 3
            answer.save()
            return Response({'success':True}, status=200)

class ListFiles(APIView):
    pagination_class = CustomPagination()   
    def get(self, request ):  
        files = File.objects.all()
        page = self.pagination_class.paginate_queryset(queryset = files ,request =request)
        serializer = FileSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

class CreateFiles(APIView):
    permission_classes = (EditTickets)
    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UpdateFiles(APIView):
#     def patch(self , request ):
#             FileId = request.query_params.get("id")
#             file = File.objects.get(id = FileId)
#             serializer = FileSerializer(instance = file , data=request.data , partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DeleteFiles(APIView):
#     def delete(self , request ):
#             FileId = request.query_params.get("id")
#             file = File.objects.get(id =FileId)
#             file.delete()
#             return Response({'success':True}, status=200)

class ListTags(APIView):
    pagination_class = CustomPagination()
    def get(self, request , format=None):  
        tags =  Tag.objects.all()
        page = self.pagination_class.paginate_queryset(queryset = tags ,request =request)
        serializer = TagSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

class CreateTags(APIView):
    permission_classes = (EditTickets)
    def post(self, request):
        # print(request.data)
        serializer = TagSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateTags(APIView):
    def patch(self , request ):
            Tag_id = request.query_params.get("id")
            tag_updateing = Tag.objects.get(id = Tag_id)
            serializer = TagSerializer(tag_updateing , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTags(APIView):
    def delete(self , request ):
            Tag_id = request.query_params.get("id")
            tag = Tag.objects.get(id = Tag_id)
            tag.delete()
            return Response({'success':True}, status=200)

class ListCategories(APIView):
    pagination_class = CustomPagination()
    def get( self , request):  
            categories =  Category.objects.all()
            page = self.pagination_class.paginate_queryset(queryset = categories ,request =request)
            serializer = CategorySerializer(page, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)

class CreateCategories(APIView):
     def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateCategories(APIView):
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
    def delete(self , request):
            category_id = request.query_params.get("id")
            category = Category.objects.get(id = category_id)
            category.delete()
            return Response({'success':True}, status=200)

# class NoAnswer(APIView):
#     pagination_class = CustomPagination()
#     def get(self , request):
#        NoAnswerTicket = Ticket.objects.exclude(is_answered = True)
#        page = self.pagination_class.paginate_queryset(queryset = NoAnswerTicket ,request =request)
#        serializer = TicketSerializer(page, many=True)
#        return self.pagination_class.get_paginated_response(serializer.data)

# class SpeceficUserTicket(APIView):
#     pagination_class = CustomPagination()
#     def get(self , request):
#             user_id = request.query_params.get("id") 
#             SpeceficUser = Ticket.objects.filter(user = user_id )
#             page = self.pagination_class.paginate_queryset(queryset = SpeceficUser ,request =request)
#         # get > one object  
#         # all >   
#         # filter > 
#         # exclude > list 
#             serializer = TicketSerializer(page, many=True)
#             return self.pagination_class.get_paginated_response(serializer.data)
# class LastDayTickets(APIView):
#     pagination_class = CustomPagination()
#     def get(self , request):
#        startdate = datetime.today() - timedelta(days=1)
#        enddate = datetime.today()
#        LastdayTickets =Ticket.objects.filter(created_date__date__range=[startdate, enddate])
#        page = self.pagination_class.paginate_queryset(queryset = LastdayTickets ,request =request)
#        serializer = TicketSerializer(page , many=True)
#        return self.pagination_class.get_paginated_response(serializer.data)

# class LastWeekTickets(APIView):
#     pagination_class = CustomPagination()
#     def get(self , request):
#        startdate = datetime.today() - timedelta(days=6)
#        enddate = datetime.today()
#        LastweekTickets =Ticket.objects.filter(created_date__date__range=[startdate, enddate])
#        page = self.pagination_class.paginate_queryset(queryset = LastweekTickets ,request =request)
#        serializer = TicketSerializer(page , many=True)
#        return self.pagination_class.get_paginated_response(serializer.data)
# class LastYearTickets(APIView):
#     pagination_class = CustomPagination()
#     def get(self , request):
#        startdate = datetime.today() - timedelta(days = 365)
#        enddate = datetime.today()
#        LastyearTickets =Ticket.objects.filter(created_date__date__range=[startdate, enddate])
#        page = self.pagination_class.paginate_queryset(queryset = LastyearTickets ,request =request)
#        serializer = TicketSerializer(page , many=True)
#        return self.pagination_class.get_paginated_response(serializer.data)
    
# class SpeceficKeywordTicket(APIView):
#     pagination_class = CustomPagination()
#     def get(self , request):
#             key = request.query_params.get("keyword")
#             print(key)
#             tickets = Ticket.objects.filter(Q(title__contains = key) | Q(text__contains =key ))
#             page = self.pagination_class.paginate_queryset(queryset = tickets ,request =request)
#             serializer = TicketSerializer(page, many=True)
#             return self.pagination_class.get_paginated_response(serializer.data)

# class SpeceficDepartmentTicket(APIView):
#     pagination_class = CustomPagination()
#     def get(self , request):
#        Department_id = request.query_params.get("id")
#        SpeceficDepartment = Ticket.objects.filter(department = Department_id)
#        page = self.pagination_class.paginate_queryset(queryset = SpeceficDepartment ,request =request)
#        serializer = TicketSerializer(page, many=True)
#        return self.pagination_class.get_paginated_response(serializer.data)

# class SpeceficDepartmentAndNoAnsTicket(APIView):
#     pagination_class = CustomPagination()
#     def get(self , request):
#        Department_id = request.query_params.get("id")
#        SpeceficDepartmentNoAnswerd = Ticket.objects.filter(department = Department_id , is_answered = 0)
#        page = self.pagination_class.paginate_queryset(queryset = SpeceficDepartmentNoAnswerd ,request =request)
#        serializer = TicketSerializer(page , many=True)
#        return self.pagination_class.get_paginated_response(serializer.data)

# class SpeceficTagsTicket(APIView):
#     pagination_class = CustomPagination()
#     def get(self , request):
#             tag_id = request.query_params.get("id")
#             SpeceficTag = Ticket.objects.filter(tags = tag_id)
#             page = self.pagination_class.paginate_queryset(queryset = SpeceficTag ,request =request)
#             serializer = TicketSerializer(page, many=True)
#             return self.pagination_class.get_paginated_response(serializer.data)

# class TagsForSpeceficTicket(APIView):
#     pagination_class = CustomPagination()
#     def get(self , request):
#        Ticket_id = request.query_params.get("id")
#        SpeceficTicket = Tag.objects.filter(ticket = Ticket_id)
#        page = self.pagination_class.paginate_queryset(queryset = SpeceficTicket ,request =request)
#        serializer = TagSerializer(page , many=True)
#        return self.pagination_class.get_paginated_response(serializer.data)

class TicketList(generics.ListAPIView):
	queryset = Ticket.objects.all()
	serializer_class = TicketSerializer
	name = 'Ticket-list'
	
	filter_fields = (
		'department',
		'user',
		'title',
        'is_answered',
		'tags'
	)


class ListOfCategories(APIView):
    pagination_class = CustomPagination()
    def get(self , request):
        if request.query_params.get("parent") != None:
            categories = Category.objects.filter(parent = request.query_params.get("parent"))
        else:
            categories = Category.objects.filter(parent__isnull = True)
        page = self.pagination_class.paginate_queryset(queryset = categories ,request =request)
        serializer = ShowSubCategorySerializer(page , many=True)
        return self.pagination_class.get_paginated_response(serializer.data)



#         categories =  Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.name)
# #

#

# class UpdateTitleOfTicket(APIView):
#     def patch(self , request):
#         try:
#             TicketId = request.query_params.get("id")
#             new_title = request.query_params.get("new title")
#             SpeceficTicket = Ticket.objects.filter( id = TicketId ).update(title = new_title)
#             serializer = TicketSerializer(instance = SpeceficTicket , title=request.data , partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except ObjectDoesNotExist:  
#             print("The keyword doesn't exist.")
        
# @csrf_exempt
# def ticket_list(request):
   
#     if request.method == 'GET':
#         tickets = Ticket.objects.all()
#         serializer = TicketSerializer(tickets, many=True)
#         return JsonResponse(serializer.data, safe=False)

#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = TicketSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, status=400)

# @csrf_exempt
# def ticket_detail(request, pk):
  
#     try:
#         ticket = Ticket.objects.get(pk=pk)
#     except Ticket.DoesNotExist:
#         return HttpResponse(status=404)

#     if request.method == 'GET':
#         serializer = TicketSerializer(snippet)
#         return JsonResponse(serializer.data)

#     elif request.method == 'PUT':
#         data = JSONParser().parse(request)
#         serializer = TicketSerializer(snippet, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == 'DELETE':
#         ticket.delete()
#         return HttpResponse(status=204)


# def department_tickets_view(request):
#     tickets = Ticket.objects.filter(department = request.department)
#     return render(request,'department-tickets.html',
#                               {"department-tickets": tickets},
#                               context_instance=RequestContext(request))

# def operator_tickets_view(request):
#     tickets = Ticket.objects.filter(operator=request.user) \
#                                     .filter(is_answered = 1)
#     return render(request,'operator-tickets.html',
#                               {"operator-tickets": tickets},
                              
#                               context_instance=RequestContext(request))

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class TicketViewSet(viewsets.ModelViewSet):
   
#     queryset = Ticket.objects.all()
#     serializer_class = TicketSerializer
#     permission_classes = [permissions.IsAuthenticated]

# def my_tickets_view(request):
#     tickets = Ticket.objects.filter(UserProfile = request.user)
#     return render(request,'my-tickets.html',
#                         {"my-tickets": tickets},
#                         context_instance=RequestContext(request))

