from rest_framework.views import APIView
from rest_framework.response import Response
from System.models import Ticket
from System.serializers import TicketSerializer
from user.serializer import UserProfileSerializer
from user.models import UserProfile
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from utilities.pagination import CustomPagination
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

# 
 

   
        
      
        
        
            
           

class Filter(APIView):
    pagination_class = CustomPagination()
    def post(self, request ,**kwargs):
        print(type(request.query_params))
        key_list= ['user__is_staff ', 'title__icontains' , 'operator', 'user__date_joined', 'department' , 'user__first_name__contains' , 'is_answered']
        validated_filters ={}
        f_dict=request.query_params.dict()
        for key,value in f_dict.items():
            if key in key_list:
                validated_filters[key]=value
        print(validated_filters)        
        tickets =Ticket.objects.filter(**validated_filters)
        page = self.pagination_class.paginate_queryset(queryset = tickets ,request =request)
        serializer = TicketSerializer(page, many = True)
    
        return self.pagination_class.get_paginated_response(serializer.data)


# class Filter(generics.ListAPIView):       
#     queryset = UserProfile.objects.all()
#     serializer_class = UserProfileSerializer
#     filterset_fields = ['first_name']
# class TicketListView(FilteredListView):
#     model = Ticket
#     paginate_by = 10
#     form_class = TicketListForm
#     search_fields = ['creator__last_name', 'creator__first_name',
#                  'subject', 'body']
#     filter_fields = ['status', 'priority']
#     qs_filter_fields = {'category__last_name': 'category',
#                         'status': 'status',
#                         'priority': 'priority'
#                     }
#     default_order = 'last_updated_at'