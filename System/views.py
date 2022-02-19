from importlib.abc import ExecutionLoader
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
from System.serializers import TicketSerializer , DepartmentSerializer , AnswerSerializer , FileSerializer
# from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist


# from django.conf import settings
# from rest_framework.authtoken.views import ObtainAuthToken 
# from rest_framework.settings import api_settings
# from rest_framework import viewsets
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from .models import Post
# from .serializers import PostSerializer
# from .permissions import UpdateOwnProfile
# class PostViewSet(viewsets.ModelViewSet):
#     serializer_class = PostSerializer
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (
#         UpdateOwnProfile,
#         IsAuthenticatedOrReadOnly,
#     )
#     queryset = Post.objects.all()


# class UserLoginApiView(ObtainAuthToken):
#     renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ListTickets(APIView):

    def get(self, request , format=None):  

        tickets =  Ticket.objects.all()
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)
    




class CreateTickets(APIView):

    def post(self, request, format=None):
        # print(request.data)
        serializer = TicketSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateTickets(APIView):
    def patch(self , request ):
        try:
            TicketId = request.query_params.get("id")
            ticket = Ticket.objects.get(id = TicketId)
            serializer = TicketSerializer(instance = ticket , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:  
            print("The ticket doesn't exist.")
        

class DeleteTickets(APIView):
    def delete(self , request , format = None):
        try:
            TicketId = request.query_params.get("id")
            ticket = Ticket.objects.get(id = TicketId)
            ticket.delete()
            return Response({'success':True}, status=200)
        except ObjectDoesNotExist:  
            print("Either the department or ticket doesn't exist.")
class DepartmentViewManagement(APIView):

    def get(self, request , format=None):  

        departements =  Department.objects.all()
        serializer = DepartmentSerializer(departements, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self , request ):
        try:
        # print(request.query_params)
        # print(request.data)
            DepartmentId = request.query_params.get("id")
            department = Department.objects.get(id = DepartmentId)
            serializer = DepartmentSerializer(instance = department , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:  
            print("Either the department or ticket doesn't exist.")
        

    def delete(self , request , format = None):
        try:
            DepartmentId = request.query_params.get("id")
            department = Department.objects.get(id = DepartmentId)
            department.delete()
            return Response({'success':True}, status=200)
        except ObjectDoesNotExist:  
            print("Either the department or ticket doesn't exist.")

    

class ListAnswers(APIView):

    def get(self, request , format=None):  

        answers =  Answer.objects.all()
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)





class CreateAnswers(APIView):

     def post(self, request, format=None):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateAnswers(APIView):
    def patch(self , request ):
        try:
        # print(request.query_params)
        # print(request.data)
            AnswerId = request.query_params.get("id")
            answer =Answer.objects.get(id = AnswerId)
            serializer = AnswerSerializer(instance = answer , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:  
            print("Either the answer or ticket doesn't exist.")

class DeleteAnswers(APIView):
    def delete(self , request , format = None):
        try:
            AnswerId = request.query_params.get("id")
            answer = Answer.objects.get(id = AnswerId)
            answer.delete()
            return Response({'success':True}, status=200)
        except ObjectDoesNotExist:  
            print("Either the answer or ticket doesn't exist.")

class ListFiles(APIView):

    def get(self, request , format=None):  

        files = File.objects.all()
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)





class CreateFiles(APIView):

    def post(self, request):
        try:
            FileId = request.query_params.get("id")
            file = File.objects.get(id = FileId)
            fs = FileSystemStorage()
            serializer = fs.url(FileSerializer(request.FILES)) 
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        except ObjectDoesNotExist:  
            print("Either the file or ticket doesn't exist.")

class UpdateFiles(APIView):
    def patch(self , request ):
        try:
        # print(request.query_params)
        # print(request.data)
            FileId = request.query_params.get("id")
            file = File.objects.get(id = FileId)
            serializer = FileSerializer(instance = file , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:  
             print("Either the file or ticket doesn't exist.")

class DeleteFiles(APIView):
    def delete(self , request , format = None):
        try:
            FileId = request.query_params.get("id")
            file = File.objects.get(id =FileId)
            file.delete()
            return Response({'success':True}, status=200)
        except ObjectDoesNotExist:  
            print("The ticket doesn't exist.")

class NoAnswer(APIView):
    def get(self , request):
       NoAnswerTicket = Ticket.objects.exclude(is_answered = True)
       serializer = TicketSerializer(NoAnswerTicket, many=True)
       return Response(serializer.data)

class SpeceficUserTicket(APIView):
    def get(self , request):
        try:
            user_id = request.query_params.get("id") 
            SpeceficUser = Ticket.objects.filter(user = user_id )
        # get > one object  
        # all >   
        # filter > 
        # exclude > list 
            serializer = TicketSerializer(SpeceficUser, many=True)
            return Response(serializer.data)
        except ObjectDoesNotExist:  
            print("The ticket doesn't exist.")


class LastDayTickets(APIView):
    def get(self , request):
       startdate = datetime.today() - timedelta(days=1)
       enddate = timezone.now().date()
       LastdayTickets =Ticket.objects.filter(created_date__date__range=[startdate, enddate])
       serializer = TicketSerializer(LastdayTickets , many=True)
       return Response(serializer.data)
class LastWeekTickets(APIView):
    def get(self , request):
       startdate = datetime.today() - timedelta(days=6)
       enddate = timezone.now().date()
       LastweekTickets =Ticket.objects.filter(created_date__range=[startdate, enddate])
       serializer = TicketSerializer(LastweekTickets , many=True)
       return Response(serializer.data)
class LastYearTickets(APIView):
    def get(self , request):
       startdate = datetime.today() - timedelta(days = 365)
       enddate = timezone.now().date()
       LastyearTickets =Ticket.objects.filter(created_date__range=[startdate, enddate])
       serializer = TicketSerializer(LastyearTickets , many=True)
       return Response(serializer.data)
    
class SpeceficKeywordTicket(APIView):
    def get(self , request):
       key= request.query_params.get("id")
       SpeceficKeyword = Ticket.objects.filter(data__contains = key)
       serializer = TicketSerializer(SpeceficKeyword, many=True)
       return Response(serializer.data)

class SpeceficDepartmentTicket(APIView):
    def get(self , request):
       key= request.query_params.get("Department")
       SpeceficDepartmentword = Ticket.objects.filter(key)
       serializer = TicketSerializer(SpeceficDepartmentword, many=True)
       return Response(serializer.data)

class SpeceficDepartmentAndNoAnsTicket(APIView):
    def get(self , request):
       key= request.query_params.get("Department")
       SpeceficDepartmentNoAnswerd = Ticket.objects.filter(department = key) \
                                     .filter(is_answered = 0)
       serializer = TicketSerializer(SpeceficDepartmentNoAnswerd , many=True)
       return Response(serializer.data)

class SpeceficTagsTicket(APIView):
    def get(self , request):
       Tag = request.query_params.get("Tag")
       SpeceficTag = Ticket.objects.filter(Tag)
       serializer = TicketSerializer(SpeceficTag , many=True)
       return Response(serializer.data)

class TagsList(APIView):
    def get(self , request):
       TicketID = request.query_params.get("ID")
       SpeceficTicket = Ticket.objects.filter(TicketID)
       serializer = TicketSerializer(SpeceficTicket , many=True)
       return Response(serializer.data)

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

