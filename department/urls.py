from django.urls import path, include
from department.views import *

urlpatterns = [
    path('DepartmentViewManagement/',DepartmentViewManagement.as_view()),
]