from .profilemanagement import ProfileView, OperatorUpdatesUser
from .passwordchange import PasswordChange
from .captcha import CaptchaView
from .forgot import (
    ForgotPassByEmailAvailability,
    ForgotPassView,
    ForgotPassEmailCallBack,
    ForgotPassSMSCallBack,
)

from .signup import SignupView, VerifyPhoneNumber
from .login import (
    UserLoginApiView,
    CorporateLogin,
    # UserLogoutView,
    ChangeToken,
)
from .verifyemail import VerifyEmailView, VerifyEmailCallBack
from .operator_users import *
from .user_files import *
from .users_birthdays import *
