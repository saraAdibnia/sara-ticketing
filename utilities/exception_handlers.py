from tkinter.messagebox import RETRY
from turtle import st
from django.http import response
from rest_framework.response import Response


def validation_error(serializer):
    return Response({
        'error':serializer.errors,
        'succeed':False
    })

def existence_error(object:str):
    return Response({
        'error':f'object {object} does not exists',
        'succeed':False
    })