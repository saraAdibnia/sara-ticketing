from FAQ.serializers import QuestionSerializer , ShowQuestionSerializer , ShowAnswerSerializer , AnswerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from FAQ.models import Question , Answer
from rest_framework import status

from utilities.pagination import CustomPagination



class QuestionViewManagement(APIView):
    pagination_class = CustomPagination
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


class AnswerViewManagement(APIView):
    pagination_class = CustomPagination()
    def get(self, request ):  

        questions =  Answer.objects.all()
        page = self.pagination_class.paginate_queryset(queryset = questions ,request =request)
        serializer = ShowQuestionSerializer(page, many=True)
        return self.pagination_class.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self , request ):
            answerId = request.query_params.get("id")
            answer = Answer.objects.get(id = answerId)
            serializer = AnswerSerializer(instance = answer , data=request.data , partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self , request ):
            answerId = request.query_params.get("id")
            answer = Answer.objects.get(id = answerId)
            answer.delete()
            return Response({'success':True}, status=200)
