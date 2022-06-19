from rest_framework import permissions
from icecream import ic

class EditTickets(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user.id == request.user.id                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                

class IsOperator(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role ==1 


