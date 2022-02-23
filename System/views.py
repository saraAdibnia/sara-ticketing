from ast import keyword
from importlib.abc import ExecutionLoader
from logging import exception

from django.test import tag
from .models import *
from datetime import timedelta , datetime
from django.utils import timezone
from django.shortcuts import render
from django.template import RequestContext
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from django.http import Http404
from rest_framework import status
from System.serializers import TicketSerializer , DepartmentSerializer , AnswerSerializer , FileSerializer , TagSerializer , CategorySerializer, UserProfileSerializer
# from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
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
    permission_classes = (IsAuthenticated,)
    def get(self, request):  
            tickets =  Ticket.objects.all()
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data)

    
class CreateTickets(APIView):

    def post(self, request):
        serializer = TicketSerializer( data=request.data)
        tag = Tag.objects.first()
        # tag = Tag.objects.filter(id__in = tag_ids)
        
        if serializer.is_valid():
            ticket = serializer.save()
            ticket.tags.add(tag)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateTickets(APIView):
    def patch(self , request ):
            TicketId = request.query_params.get("id")
            ticket = Ticket.objects.get(id = TicketId)
            serializer = TicketSerializer(instance = ticket , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
          
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class DeleteTickets(APIView):
    def delete(self , request ):
            TicketId = request.query_params.get("id")
            ticket = Ticket.objects.get(id = TicketId)
            ticket.delete()
            return Response({'success':True}, status=200)

class DepartmentViewManagement(APIView):

    def get(self, request ):  

        departements =  Department.objects.all()
        serializer = DepartmentSerializer(departements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self , request ):
            DepartmentId = request.query_params.get("id")
            department = Department.objects.get(id = DepartmentId)
            serializer = DepartmentSerializer(instance = department , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self , request ):
            DepartmentId = request.query_params.get("id")
            department = Department.objects.get(id = DepartmentId)
            department.delete()
            return Response({'success':True}, status=200)


class ListAnswers(APIView):

    def get(self, request ):  

        answers =  Answer.objects.all()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)

class CreateAnswers(APIView):

     def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateAnswers(APIView):
    def patch(self , request ):
        # print(request.query_params)
        # print(request.data)
            AnswerId = request.query_params.get("id")
            answer =Answer.objects.get(id = AnswerId)
            serializer = AnswerSerializer(instance = answer , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteAnswers(APIView):
    def delete(self , request):
            AnswerId = request.query_params.get("id")
            answer = Answer.objects.get(id = AnswerId)
            answer.delete()
            return Response({'success':True}, status=200)

class ListFiles(APIView):

    def get(self, request ):  

        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

class CreateFiles(APIView):
    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateFiles(APIView):
    def patch(self , request ):
            FileId = request.query_params.get("id")
            file = File.objects.get(id = FileId)
            serializer = FileSerializer(instance = file , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteFiles(APIView):
    def delete(self , request ):
            FileId = request.query_params.get("id")
            file = File.objects.get(id =FileId)
            file.delete()
            return Response({'success':True}, status=200)

class ListTags(APIView):

    def get(self, request , format=None):  
        
        tags =  Tag.objects.all()
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data)

class CreateTags(APIView):

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
    def get( self , request):  
            categories =  Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)

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

class NoAnswer(APIView):
    def get(self , request):
       NoAnswerTicket = Ticket.objects.exclude(is_answered = True)
       serializer = TicketSerializer(NoAnswerTicket, many=True)
       return Response(serializer.data)

class SpeceficUserTicket(APIView):
    def get(self , request):
            user_id = request.query_params.get("id") 
            SpeceficUser = Ticket.objects.filter(user = user_id )
        # get > one object  
        # all >   
        # filter > 
        # exclude > list 
            serializer = TicketSerializer(SpeceficUser, many=True)
            return Response(serializer.data)

class LastDayTickets(APIView):
    def get(self , request):
       startdate = datetime.today() - timedelta(days=1)
       enddate = datetime.today()
       LastdayTickets =Ticket.objects.filter(created_date__date__range=[startdate, enddate])
       serializer = TicketSerializer(LastdayTickets , many=True)
       return Response(serializer.data)

class LastWeekTickets(APIView):
    def get(self , request):
       startdate = datetime.today() - timedelta(days=6)
       enddate = datetime.today()
       LastweekTickets =Ticket.objects.filter(created_date__date__range=[startdate, enddate])
       serializer = TicketSerializer(LastweekTickets , many=True)
       return Response(serializer.data)
class LastYearTickets(APIView):
    def get(self , request):
       startdate = datetime.today() - timedelta(days = 365)
       enddate = datetime.today()
       LastyearTickets =Ticket.objects.filter(created_date__date__range=[startdate, enddate])
       serializer = TicketSerializer(LastyearTickets , many=True)
       return Response(serializer.data)
    
class SpeceficKeywordTicket(APIView):
    def get(self , request):
            key = request.query_params.get("keyword")
            print(key)
            tickets = Ticket.objects.filter(Q(title__contains = key) | Q(text__contains =key ))
            serializer = TicketSerializer(tickets, many=True)
            return Response(serializer.data)

class SpeceficDepartmentTicket(APIView):
    def get(self , request):
       Department_id = request.query_params.get("id")
       SpeceficDepartment = Ticket.objects.filter(department = Department_id)
       serializer = TicketSerializer(SpeceficDepartment, many=True)
       return Response(serializer.data)

class SpeceficDepartmentAndNoAnsTicket(APIView):
    def get(self , request):
       Department_id = request.query_params.get("id")
       SpeceficDepartmentNoAnswerd = Ticket.objects.filter(department = Department_id , is_answered = 0)
       serializer = TicketSerializer(SpeceficDepartmentNoAnswerd , many=True)
       return Response(serializer.data)

class SpeceficTagsTicket(APIView):
    def get(self , request):
            tag_id = request.query_params.get("id")
            SpeceficTag = Ticket.objects.filter(tags = tag_id)
            serializer = TicketSerializer(SpeceficTag, many=True)
            return Response(serializer.data)

class TagsForSpeceficTicket(APIView):
    def get(self , request):
       Ticket_id = request.query_params.get("id")
       SpeceficTicket = Tag.objects.filter(ticket = Ticket_id)
       serializer = TagSerializer(SpeceficTicket , many=True)
       return Response(serializer.data)

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

# class UserList(generics.ListAPIView):
#     f_dict={'is_staff': True }#, 'title__icontains' : key
#     serializer_class = UserSerializer
#     queryset =UserProfile.objects.filter(**f_dict)

class ListUser(APIView):
    def get( self , request):  
            users =  UserProfile.objects.all()
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data)

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

