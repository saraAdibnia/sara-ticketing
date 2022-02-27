from user import views
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
path('all_user/',views.ListUser.as_view()),
path('create_user/',views.CreateUser.as_view()),
path('update_user/',views.UpdateUser.as_view()),
path('delete_user/',views.DeleteUser.as_view()),
path('token-auth/',obtain_auth_token, name='token_auth'),
path('user_filters/',views.Filter.as_view()),
]