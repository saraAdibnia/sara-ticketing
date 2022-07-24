from django.urls import path
from django.conf.urls import include
from places.views import DialCodeView , CityView , CountryView

urlpatterns = [
    path('dialcode/', DialCodeView.as_view(),),
    path('city/', CityView.as_view(),),
    path('country/', CountryView.as_view(),),
]