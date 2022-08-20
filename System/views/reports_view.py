from rest_framework import generics
from System.models import *
from ..serializers import ShowTicketSerializer
from System.serializers import (ShowTicketSerializer)
from rest_framework.permissions import IsAuthenticated
from System.permissions import EditTickets, IsOperator
from user.serializers import UserShowSerializer

class ListOfBadOperators(generics.ListAPIView):

    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = UserShowSerializer
    def get_queryset(self):
        ticket =  Ticket.objects.filter(status = 3).first()
        operator = ticket.operator
        operator = User.objects.filter(id = operator.id )
        return operator
  