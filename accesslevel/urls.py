from django.urls import path, include

from accesslevel.views import *
from accesslevel.views.user_access_levels_show_views import UserAccessLevelShowView


urlpatterns = [
    path("my_access_level_requests/", MyAccessLevelRequestListView.as_view()),
    path("access_level_request_submit/", AccessLevelRequestSubmitView.as_view()),
    path("access_level_subject_tree/", AccessLevelAllSubjectsView.as_view()),
    path("access_level_group_tree/", AccessLevelAllGroupsView.as_view()),
    path("access_level_action_tree/", AccessLevelAllActionsView.as_view()),
    path("common_users_show/", CommonAccessLevelShowView.as_view()),
    path(
        "common_users_group_management/", CommonAccessLevelGroupManagementView.as_view()
    ),
    path("common_users_management/", CommonAccessLevelManagementView.as_view()),
    path("user_access_level/", UserAccessLevelShowView.as_view()),
    path("all_access_level_requests/", AccessLevelRequestList.as_view()),
    path("access_level_request_proceed/", AccessLevelRequestProceed.as_view()),
    path("change_user_access_level/", UserAccessLevelManagementView.as_view()),
    # path("corporate_users/", CorporateUsers.as_view()),
    # path("corporate_users_activity/", CorporateUsersActivity.as_view(),),
    path("user_row_count_access_manager/",
         UserRowCountAccessViews.as_view()),
]
