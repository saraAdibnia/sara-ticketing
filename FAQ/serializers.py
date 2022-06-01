from FAQ.models import Question, Answer
from rest_framework import serializers

class ShowQuestionSerializer(serializers.ModelSerializer):
    class Meta:
            model = Question
            fields = ['id' , 'text']

class ShowAnswerSerializer(serializers.ModelSerializer):
    class Meta:
            model = Answer
            fields = ['id' , 'text']
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
            model = Question
            fields = ['id' , 'text']
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
            model = Answer
            fieldns= ['id' , 'text']