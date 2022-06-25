from django.urls import path
from FAQ.views import *

urlpatterns = [
    path('faq_view_management/',FAQViewManagement.as_view()),
]