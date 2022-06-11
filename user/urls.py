# from user.views.contract_views import ImportContractUser
from django.urls import path, include
from user import models
from user.views import *


urlpatterns = [
    path("login/", UserLoginApiView.as_view()),
    # path('logout/', UserLogoutView.as_view()),
    path("change_token/", ChangeToken.as_view()),
    path("forgotpass/", ForgotPassView.as_view()),
    path("available_forgotpass/", ForgotPassByEmailAvailability.as_view()),
    path("signup/", SignupView.as_view()),
    path("profile/", ProfileView.as_view()),
    path("verify/", VerifyPhoneNumber.as_view()),
    path("changepass/", PasswordChange.as_view()),
    path("corporate_login/", CorporateLogin.as_view()),
    path("captcha/", CaptchaView.as_view()),
    path("verify_email/", VerifyEmailView.as_view()),
    path("verify_email_back/", VerifyEmailCallBack.as_view()),
    path("forgot_pass_back/", ForgotPassEmailCallBack.as_view()),
    # path("contracts/", UserContractView.as_view()),
    path("forgot_pass_sms_back/", ForgotPassSMSCallBack.as_view()),
    # path("import_contract_user/", ImportContractUser.as_view()),
    path("corporate_user_created_by/", CorportateUsers.as_view()),
    path("operator_update_user_profile/", OperatorUpdatesUser.as_view()),
    path("user_file_manger/", UserFileManager.as_view()),
    path("users_birthdays/", UsersBirthdays.as_view()),
    path('all_staff/',StaffListView.as_view()),
    # path("co_users_performance/", CoUsersPerformance.as_view()),
    # path("normal_users_performance/", NormalUsersPerformance.as_view()),
    path('user_birthday_by_link/', UserBirthdayByLink.as_view()),
    # path('normal_user_activity/',NormalUsersActivity.as_view()),
    # path('advance_user_search/', UserAdvanceSearch.as_view()),
    path('user_normal_search/', UserNormalSearch.as_view(),),
]
