from user import views
from django.urls import path

urlpatterns = [
path('all_user/',views.ListUser.as_view()),
path('create_user/',views.CreateUser.as_view()),
path('update_user/',views.UpdateUser.as_view()),
path('delete_user/',views.DeleteUser.as_view()),
]