from django.urls import URLPattern, path,include
from . import views
from rest_framework import routers
from rest_framework.routers import DefaultRouter
from .views import PostViewSet ,UserLoginApiView





#URLConf
urlpatterns = [
     path('all_ticket/',views.ListTickets.as_view()),
     path('create_ticket/',views.CreateTickets.as_view()),
     path('update_ticket/',views.UpdateTickets.as_view()),
     path('delete_ticket/',views.DeleteTickets.as_view()),
     path('DepartmentViewManagement/',views.DepartmentViewManagement.as_view()),
     path('all_answer/',views.ListAnswers.as_view()),
     path('create_answer/',views.CreateAnswers.as_view()),
     path('update_answer/',views.UpdateAnswers.as_view()),
     path('delete_answer/',views.DeleteAnswers.as_view()),
     path('all_file/',views.ListFiles.as_view()),
     path('create_file/',views.CreateFiles.as_view()),
     path('update_file/',views.UpdateFiles.as_view()),
     path('delete_file/',views.DeleteFiles.as_view()),
    # path('tickets/', views.my_tickets_view, name='my_tickets_view'),
    # path('tickets/', views.department_tickets_view, name='.department_tickets_view'),
    # path('tickets/', views.operator_tickets_view, name='operator_tickets_view'),
    # path('', include(router.urls)),
    # path('all_ticket/', views.ticket_list),
    # path('all_ticket/<int:pk>/', views.ticket_detail),
    path('', include(router.urls)),
    path('login/', UserLoginApiView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]


router = DefaultRouter()
router.register('posts', PostViewSet)

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
