from rest_framework import permissions
from icecream import ic
from user.models import User
from System.models import Ticket
from django.db.models import Q
class EditTickets(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

class IsOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role ==3






