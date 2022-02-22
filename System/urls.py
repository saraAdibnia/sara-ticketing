from django.forms import Media
from django.urls import URLPattern, path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework import routers
# from rest_framework.routers import DefaultRouter
# from .views import PostViewSet ,UserLoginApiView





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
     path('all_tag/',views.ListTags.as_view()),
     path('create_tag/',views.CreateTags.as_view()),
     path('update_tag/',views.UpdateTags.as_view()),
     path('delete_tag/',views.DeleteTags.as_view()),
     path('all_category/',views.ListCategories.as_view()),
     path('create_category/',views.CreateCategories.as_view()),
     path('update_category/',views.UpdateCategories.as_view()),
     path('delete_category/',views.DeleteCategories.as_view()),
     path('NoAnswerTicket/',views.NoAnswer.as_view()),
     path('speceficUser/',views.SpeceficUserTicket.as_view()),
     path('last_day_ticket/',views.LastDayTickets.as_view()),
     path('last_week_ticket/',views.LastWeekTickets.as_view()),
     path('last_year_ticket/',views.LastYearTickets.as_view()),
     path('specefic_keyword/',views.SpeceficKeywordTicket.as_view()),
     path('specefic_department/',views.SpeceficDepartmentTicket.as_view()),
     path('specefic_dep_No_Ans_department/',views.SpeceficDepartmentAndNoAnsTicket.as_view()),
     path('specefic_tag/',views.SpeceficTagsTicket.as_view()),
     path('Ticket_tag/',views.TagsForSpeceficTicket.as_view()),
     path('api-token-auth/',obtain_auth_token, name='api_token_auth'),
     #  path('update_title_of_ticket/',views.UpdateTitleOfTicket.as_view()),
    # path('tickets/', views.my_tickets_view, name='my_tickets_view'),
    # path('tickets/', views.department_tickets_view, name='.department_tickets_view'),
    # path('tickets/', views.operator_tickets_view, name='operator_tickets_view'),
    # path('', include(router.urls)),
    # path('all_ticket/', views.ticket_list),
    # path('all_ticket/<int:pk>/', views.ticket_detail),
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# router = DefaultRouter()
# router.register('posts', PostViewSet)

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
