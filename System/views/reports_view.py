from rest_framework import generics
from System.models import *
from ..serializers import ShowTicketSerializer
from System.serializers import (ShowTicketSerializer)
from rest_framework.permissions import IsAuthenticated
from System.permissions import EditTickets, IsOperator

class ListOfBadOperators(generics.ListAPIView):

    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = ShowTicketSerializer
    def get_object(self):
        ticket =  Ticket.objects.filter(status = 3) 
        operator = User.objects.filter(id = self.ticket.operator.id )
        return operator
class ListAnswers(generics.ListAPIView):

    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = ShowTicketSerializer
    def get_queryset(self):
        queryset = Ticket.objects.get(id = self.request.query_params.get('id'))
        if self.request.user.role == 0 :
            answers =  Answer.objects.filter(receiver = self.request.user , ticket = queryset ) 
        else:
            answers =  Answer.objects.filter(ticket = queryset )
        return answers
class ListAnswers(generics.ListAPIView):

    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = ShowTicketSerializer
    def get_queryset(self):
        queryset = Ticket.objects.get(id = self.request.query_params.get('id'))
        if self.request.user.role == 0 :
            answers =  Answer.objects.filter(receiver = self.request.user , ticket = queryset ) 
        else:
            answers =  Answer.objects.filter(ticket = queryset )
        return answers