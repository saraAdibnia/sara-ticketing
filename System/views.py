from django.shortcuts import render
from .models import *
from django.shortcuts import render
from django.template import RequestContext
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import DepartmentSerializer ,FileSerializer ,AnswerSerializer ,TicketSerializer,UserSerializer


# class TestAuthView(APIView):
#     authentication_classes = (authentication.TokenAuthentication,)
#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request, format=None):
#         if (user && user.token)
#             Token.objects.create(user=instance)

#     def post(self, request, format=None):
#         setHeaders: {
#           Authorization: 
#           }




def department_tickets_view(request):
    tickets = Ticket.objects.filter(department = request.department)
    return render(request,'department-tickets.html',
                              {"department-tickets": tickets},
                              context_instance=RequestContext(request))

def operator_tickets_view(request):
    tickets = Ticket.objects.filter(operator=request.user) \
                                    .filter(is_answered = 1)
    return render(request,'operator-tickets.html',
                              {"operator-tickets": tickets},
                              
                              context_instance=RequestContext(request))

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
def my_tickets_view(request):
    tickets = Ticket.objects.filter(UserProfile = request.user)
    return render(request,'my-tickets.html',
                        {"my-tickets": tickets},
                        context_instance=RequestContext(request))
