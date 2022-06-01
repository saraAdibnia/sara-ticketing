from FAQ.serializers import QuestionSerializer , ShowQuestionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from FAQ.models import Question
from rest_framework import status



class QuestionViewManagement(APIView):
    pagination_class = CustomPagination()
    def get(self, request ):  

        questions =  Question.objects.all()
        page = self.pagination_class.paginate_queryset(queryset = questions ,request =request)
        serializer = ShowQuestionSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self , request ):
            DepartmentId = request.query_params.get("id")
            question = Question.objects.get(id = DepartmentId)
            serializer = QuestionSerializer(instance = question , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self , request ):
            QuestionId = request.query_params.get("id")
            question = Question.objects.get(id = QuestionId)
            question.status = 3
            question.save()
            return Response({'success':True}, status=200)
