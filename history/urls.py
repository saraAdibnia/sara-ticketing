# from operatorimport.views.pickup_delivery_manifset import (
#     ImportTransferManifestManagementView,
#     ImportTransferManifestView,
# )
# from operatorimport.views.hub_management import WaybillComingToHub
from django.urls import path

from .views import UserLogView

app_name = 'apps'

urlpatterns = [
    path("user_logs/", UserLogView.as_view()),
]
