from django.urls import path, include
from department.views import *

urlpatterns = [
    path('DepartmentViewManagement/',DepartmentViewManagement.as_view()),
    path('department_normal_search/',DepartmentNormalSearch.as_view()),
]