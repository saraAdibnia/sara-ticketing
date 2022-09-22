from FAQ.serializers import FrequentlyAskedQuestionSerializer , ShowFrequentlyAskedQuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from FAQ.models import FrequentlyAskedQuestion
from rest_framework import status
from utilities.pagination import CustomPagination
from rest_framework import generics , filters
from rest_framework.permissions import IsAuthenticated

class FAQViewManagement(APIView):
    pagination_class = CustomPagination()
    def get(self, request ):
        sort = request.query_params.get('sort' , '-id')
        if request.query_params.get('id'):
            questions = FrequentlyAskedQuestion.objects.filter(id = request.query_params.get('id')).order_by(sort)
        else:
            questions = FrequentlyAskedQuestion.objects.all().order_by(sort)
        page = self.pagination_class.paginate_queryset(queryset = questions ,request =request)
        serializer = ShowFrequentlyAskedQuestionSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = FrequentlyAskedQuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self , request ):
            faq_Id = request.query_params.get("id")
            question = FrequentlyAskedQuestion.objects.get(id = faq_Id)
            serializer = FrequentlyAskedQuestionSerializer(instance = question , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self , request ):
            faq_Id = request.query_params.get("id")
            question = FrequentlyAskedQuestion.objects.get(id = faq_Id)
            question.delete()
            return Response({'succeeded':True}, status=200)

class FAQNormalSearch(generics.ListAPIView):
    queryset = FrequentlyAskedQuestion.objects.all()
    serializer_class = ShowFrequentlyAskedQuestionSerializer
    filter_backends  = [filters.SearchFilter]
    search_fields = ['title' ,'text' ,'description']
