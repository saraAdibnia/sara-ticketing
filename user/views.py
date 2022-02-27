from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializer import UserProfileSerializer
from user.models import UserProfile
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

class ListUser(APIView):
    permission_classes = (IsAuthenticated,)
    def get( self , request):  
            users =  UserProfile.objects.all()
            serializer = UserProfileSerializer(users, many=True)
            return Response(serializer.data)

class CreateUser(APIView):

    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateUser(APIView):
    def patch(self , request ):
            user_id = request.query_params.get("id")
            user = UserProfile.objects.get(id = user_id)
            serializer = UserProfileSerializer(instance = user , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
          
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUser(APIView):
    def delete(self , request ):
            user_id = request.query_params.get("id")
            user = UserProfile.objects.get(id = user_id)
            user.is_active = False
            user.save()
            return Response({'success':True}, status=200)       

class Filter(generics.ListAPIView):
    def post(self, request):
        serializer = UserProfileSerializer(data=request.data)
        f_dict={'is_staff': True , 'first_name__icontains' : serializer.data }
        UserProfile.objects.filter(**f_dict)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)