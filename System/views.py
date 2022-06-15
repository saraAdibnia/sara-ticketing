from re import T
from System.documents import TicketDocument
from System.permissions import EditTickets, IsOperator
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from System.serializers import SerachTicketSerializer, TicketSerializer, ShowAnswerSerializer,AnswerSerializer , FileSerializer , TagSerializer , CategorySerializer , ShowSubCategorySerializer , ShowTicketSerializer
from System.serializers import TicketSerializer, ShowAnswerSerializer,AnswerSerializer , FileSerializer , TagSerializer , CategorySerializer , ShowSubCategorySerializer , ShowTicketSerializer
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics , filters
import json
from utilities.pagination import CustomPagination
import datetime
from icecream import ic

class ListTickets(APIView):
    """
    a compelete list of tickets with file (if file requested) and a filtered list of tickets .  

    """
    # permission_classes = [IsAuthenticated & IsOperator] #TODO: uncomment this line 
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination()
    
    def get(self, request):
        filter_keys = ['is_answered' , 'user_id' ,'created_dated__date__range' , 'title__icontains',
        'text__icontains' , 'department_id' , 'id' , 'tag' ]
        
        context = {'with_files': request.query_params.get('with_files', False),} # check to whether shows the file or not

        validated_filters = dict()
        for key , value in request.query_params.dict().items():
            if key in filter_keys:
                validated_filters[key] = value
                
        tickets= Ticket.objects.filter(**validated_filters)
        
        page = self.pagination_class.paginate_queryset(queryset = tickets ,request =request, )

        serializer = ShowTicketSerializer(page, many=True, context = context)
        # if serializer.modified > datetime.datetime.now() + datetime.timedelta(days=30) & serializer.is_answered == False:
        #     serializer.is_suspended = True
        #     serializer.save()
       
        return self.pagination_class.get_paginated_response(serializer.data)
    
class CreateTickets(APIView):
    """
    create tickets by getting title, text, user, sub_category, category, kind and tags.
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            request.data._mutable=True
        except:
            pass
        
        # #1 create a list of tags from comming data (form-data/ json)
        # #2 remove the tags string or list from request.data 
        tags = request.data.get("tags", [] )
        try:# if data comming from a formddata
            tags = json.loads(tags)

        except:
            pass
        
        try:
            request.data.pop('tags')
        except:
            pass

        #3 saving data and create a new ticket 
        if not request.data.get("user"):
            request.data['user']= request.user.id

        request.data['created_by']  = request.user.id

        print(request.data)
        serializer = TicketSerializer(data=request.data, many = False)
        ic(request.data)
        if serializer.is_valid():
            ticket =serializer.save()
            ic(tags)
            # add tags list to the created ticket.

            ticket.tags.add(*tags) 
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   

class DeleteTickets(generics.UpdateAPIView):
    """
    suspend tickets by getting their id.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    def get_object(self):
        return Ticket.objects.get(id = self.request.query_params.get('id'))
    
    def update(self, request, *args, **kwargs):
        ticket = self.get_object()
        ticket.deleted = True
        ticket.save()
        return Response({'success':True}, status=200)

class ListAnswers(generics.ListAPIView):
    """
     list of all answers of a ticket to corporate user by getting the id of ticket.
     And to normal user shows just answers that the reciever is the user themselves.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = AnswerSerializer
    def get_queryset(self):
        queryset = Ticket.objects.get(id = self.request.data['id'])
        if self.request.user.role == 0 :
            answers =  Answer.objects.filter(receiver = self.request.user , ticket = queryset)
        else:
            answers =  Answer.objects.filter(ticket = queryset)
        return answers

class CreateAnswers(APIView):
    """
     create answers for specific ticket(requests the id of tickets) by getting sender and reciever and then the status of the ticket become jari(1).

    """
    permission_classes = [IsAuthenticated & IsOperator ]
    def post(self, request):
        request.data._mutable=True
        request.data['sender']= request.user.id
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            ticket =Ticket.objects.get(id = request.data['ticket'])
            ticket.status = 1
            ticket.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DeleteAnswers(generics.UpdateAPIView):
    """
    suspend answers by getting their id.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    def get_object(self):
        return Answer.objects.get(id = self.request.query_params.get('id'))
    
    def update(self, request, *args, **kwargs):
        answer = self.get_object
        answer.deleted = True
        answer.save()
        return Response({'success':True}, status=200)

class ListFiles(generics.ListAPIView):
    """
    a compelete list of files for spcefic ticket or specific answer.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = FileSerializer
    def get_queryset(self):
        if self.request.query_params.get('ticket_id',None):
            queryset =  File.objects.filter(ticket= self.request.query_params.get('ticket_id'))
        elif self.request.query_params.get('answer_id'):
            queryset =  File.objects.filter(answer= self.request.query_params.get('answer_id'))
        return queryset

class CreateFiles(generics.CreateAPIView):
    """
    upload files by getting file, ticket id and answer id.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = FileSerializer


class ListTags(APIView):
    """
    a compelete list of tags.

    """
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination()
    def get(self, request , format=None):  
        tags =  Tag.objects.all()
        page = self.pagination_class.paginate_queryset(queryset = tags ,request =request)
        serializer = TagSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

class CreateTags(generics.CreateAPIView ):
    """
    create tags by getting their fname and ename.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = TagSerializer

class UpdateTags(APIView):
    """
    update name of tags by their id.

    """
    permission_classes = [IsAuthenticated]
    def patch(self , request ):
            Tag_id = request.query_params.get("id")
            tag_updateing = Tag.objects.get(id = Tag_id)
            serializer = TagSerializer(tag_updateing , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTags(generics.DestroyAPIView):
    """
    delete tags by getting their id.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = TagSerializer
    def get_object(self):
        return Tag.objects.get(id = self.request.query_params.get('id'))

class CreateCategories(generics.CreateAPIView):
    """
    create categories by getting their name and create sub categories by getting name and parent id.

    """
    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = CategorySerializer

class UpdateCategories(APIView):
    """
    update category by their id.

    """
    permission_classes = [IsAuthenticated]
    def patch(self , request ):
            category_id = request.query_params.get("id")
            category =Category.objects.get(id = category_id)
            serializer = CategorySerializer(instance = category , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteCategories(APIView):
    """
    delete categories by getting their id.

    """
    permission_classes = [IsAuthenticated]
    def delete(self , request):
            category_id = request.query_params.get("id")
            category = Category.objects.get(id = category_id)
            category.delete()
            return Response({'success':True}, status=200)

class ListOfCategories(APIView):
    """
    category of a sub category or list of sub categories of s a category.

    """
    permission_classes = [IsAuthenticated]
    #pagination_class = CustomPagination()
    def get(self , request):
        if request.query_params.get("parent") != None:
            categories = Category.objects.filter(parent = request.query_params.get("parent"))
        else:
            categories = Category.objects.filter(parent__isnull = True)
        page = self.pagination_class.paginate_queryset(queryset = categories ,request =request)
        serializer = ShowSubCategorySerializer(page , many=True)
        return self.pagination_class.get_paginated_response(serializer.data)


class PaginatedElasticSearch(APIView):
    """
    search in title of tickets.

    """
    permission_classes = [IsAuthenticated]
    serializer_class = SerachTicketSerializer
    document_class = TicketDocument
    def get(self, request):
        search = self.document_class.search().query("match" , title = self.request.query_params.get("search"))
        response = search.execute()
        serializer = self.serializer_class(response, many=True)
        return Response(serializer.data)

class ListMyTicket(generics.ListAPIView):
    permission_classes = [EditTickets , IsAuthenticated]
    serializer_class = TicketSerializer
    def get_queryset(self):
        if self.request.user.role == 0 :
            tickets =  Ticket.objects.filter(Q (user = self.request.user) | Q (operator = self.request.user))
        else:
            tickets =  Ticket.objects.all()
        return tickets

class TagNormalSerach(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["id","fname", "ename"]
