from django.urls import URLPattern, path,include
from . import views
from rest_framework import routers
#URLConf
urlpatterns = [
    # path('api-auth/',views.HelloView.as_view()),
    path('tickets/', views.my_tickets_view, name='my_tickets_view'),
    path('tickets/', views.department_tickets_view, name='.department_tickets_view'),
    path('tickets/', views.operator_tickets_view, name='operator_tickets_view'),
    # path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
