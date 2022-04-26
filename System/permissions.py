from rest_framework import permissions
from System.serializers import AnswerSerializer, TicketSerializer
from .models import Ticket
from icecream import ic
class UpdateOwnProfile(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user.id == request.user.id

class EditTickets(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

class IsOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role ==1

