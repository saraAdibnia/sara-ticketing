from django.urls import path
from FAQ.views import *

urlpatterns = [
    path('question_view_management/',QuestionViewManagement.as_view()),
    path('answer_view_management/',AnswerViewManagement.as_view()),
]