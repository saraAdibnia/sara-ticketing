# authentication
## captcha
It generates the code and checks either the entered code is correct or not.
## login
There is two login APIViews one for **normal** user other one for **coporate** user.
### normal user login
checking that user exists matching credentials provided and get token and checks the token to login. After all either the login was successful or unsuccessfull user log will be set. 
### coporate user login
If coporate user give wrong passowrd we generate a for digit int random number to send it via sms as temp password and after user can login successfully they should change their password. Corporate user can also login by direct_login method and get token like normal user.
# signup
if a user want's to signup in this web service there are two mandatory fields **(password, mobile phone number)** and one optional(email).
user must verify the mobile phone is theirs. this would be specified by offering 4 digit int code that has been sent to them
this view does the logic of signing up afterwards.
after that the verify code is sent by this view, front-end should take the mentioned code and send it to verifyphonenumber view in this file.
as long as the user has not provided the code to that view, his account would be inactive (handled by is_active field in user model)
in this view if the front-end get succeeded parmater as true, he should ask for the code and send the code to mobile verification view.

