from django.urls import path
from django.conf.urls import include
from places.views import DialCodeView , CityView , CountryView , StateView , CreateStateView

urlpatterns = [
    path('dialcode/', DialCodeView.as_view(),),
    path('city/', CityView.as_view(),),
    path('country/', CountryView.as_view(),),
    path('state/', StateView.as_view()),
    path('create_state/', CreateStateView.as_view()),

]