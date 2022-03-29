from django.shortcuts import render
from utilities.pagination import CustomPagination
from department.serializers import DepartmentSerializer , ShowDepartmentSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from department.models import Department
from rest_framework import status

class DepartmentViewManagement(APIView):
    pagination_class = CustomPagination()
    def get(self, request ):  

        departements =  Department.objects.all()
        page = self.pagination_class.paginate_queryset(queryset = departements ,request =request)
        serializer = ShowDepartmentSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

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
