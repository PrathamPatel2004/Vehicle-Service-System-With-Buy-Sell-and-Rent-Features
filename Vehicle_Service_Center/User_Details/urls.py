from django.urls import path
from User_Details.views import sign_up, login

urlpatterns = [
    path('Sign Up/', sign_up, name='Sign Up'),
    path('Login/', login, name='Login'),
    
]