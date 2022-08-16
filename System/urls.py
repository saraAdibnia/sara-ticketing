from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from System.views import views , reports_view


urlpatterns = [
     path('all_ticket/',views.ListTickets.as_view()),
     path('create_ticket/',views.CreateTickets.as_view()),
     path('delete_ticket/',views.DeleteTickets.as_view()),
     path('all_answer/',views.ListAnswers.as_view()),
     path('create_answer/',views.CreateAnswers.as_view()),
     path('delete_answer/',views.DeleteAnswers.as_view()),
     path('all_file/',views.ListFiles.as_view()),
     path('create_file/',views.CreateFiles.as_view()),
     path('all_tag/',views.ListTags.as_view()),
     path('create_tag/',views.CreateTags.as_view()),
     path('update_tag/',views.UpdateTags.as_view()),
     path('delete_tag/',views.DeleteTags.as_view()),
     path('create_category/',views.CreateCategories.as_view()),
     path('update_category/',views.UpdateCategories.as_view()),
     path('delete_category/',views.DeleteCategories.as_view()),
     path('categories/',views.ListOfCategories.as_view()),
     path('all_my_ticket/',views.ListMyTicket.as_view()),
     path('search/',views.PaginatedElasticSearch.as_view()),
     path('tags_normal_search/',views.TagNormalSerach.as_view()),
     path('tickets_normal_search/',views.TicketNormalSearch.as_view()),
     path('all_reviews/',views.ReviewsListAPI.as_view()),
     path('create_reviews/',views.ReviewsCreateAPI.as_view()),
     path('all_reactions/',views.ReactionListApi.as_view()),
     path('create_reactions/',views.ReactionCreateAPI.as_view()),
     path('delete_reactions/',views.ReactionDeleteAPI.as_view()),
     path('Bad_operators/',reports_view.ListOfBadOperators.as_view()),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
