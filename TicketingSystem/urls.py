"""TicketingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin 
from django.urls import path , re_path
from django.conf.urls import include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_swagger.views import get_swagger_view



# WAGTAIL
from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
# from TicketingSystem.settings import WAGTAIL_SITE_NAME # TODO : edit this import
from .api import api_router



# schema_view = get_schema_view(
#    openapi.Info(
#       title="Snippets API",
#       default_version='v1',
#       description="Test description",
#       terms_of_service="https://www.google.com/policies/terms/",
#       contact=openapi.Contact(email="contact@snippets.local"),
#       license=openapi.License(name="BSD License"),
#    ),
#    public=True,
#    permission_classes=[permissions.AllowAny],
# )




schema_view = get_swagger_view(title='Pastebin API')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('system/', include ('System.urls')),
    path('user/', include ('user.urls')) ,
    path('department/', include ('department.urls')) ,
    path('history/', include ('history.urls')) ,
    path('accesslevel/', include ('accesslevel.urls')) ,
    path('swagger/', schema_view),
    # WAGTAIL
    # path('cms/', include(wagtailadmin_urls)),
    # path('documents/', include(wagtaildocs_urls)),
    # path('pages/', include(wagtail_urls)),
    # path('api/v2/', api_router.urls),
    # re_path(r'^', include(wagtail_urls)),
]+static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# urlpatterns += [
#    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
#    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
# ]

