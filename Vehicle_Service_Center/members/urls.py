from django.urls import path
from . import views
from User_Details.views import sign_up, verify_otp, resend_otp, login, dashboard, Mechanic_Data_Form
from Requests.views import Requests, New_Request, buy_sell_vehicle, Rent_Vehicle_Requests
from Payments.views import payment_history, create_payment
from Vehicles.views import rent_vehicle, rent_vehicle_form, add_vehicle, add_rent_vehicle

urlpatterns = [
    path('', views.members, name='members'),
    path('login/', login, name='login'),
    path('sign_up/', sign_up, name='sign_up'),
    path('Mechanic_Data_Form/', Mechanic_Data_Form, name='Mechanic_Data_Form'),  # Add this line
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('resend_otp/', resend_otp, name='resend_otp'),
    path('dashboard/', dashboard, name='dashboard'),
    path('requests/', Requests, name='requests'),
    path('new_request/', New_Request, name='new_request'),
    path('requests/new_request/', New_Request, name='new_request'),
    path('payment_history/', payment_history, name='payment_history'),
    path('rent_vehicle/', rent_vehicle, name='rent_vehicle'), 
    path('rent_request/<int:vehicle_id>/', rent_vehicle_form, name="rent_request"),
    path('buy_vehicle_list/', buy_sell_vehicle, name='buy_vehicle_list'),
    path('create-payment/<int:payment_id>', create_payment, name='create-payment'),
    path('add_vehicle/', add_vehicle, name='add_vehicle'),
    path('buy_vehicle_list/add_vehicle/', add_vehicle, name='add_vehicle'),
    path('add_rent_vehicle/', add_rent_vehicle, name='add_rent_vehicle'),
    path('rent_vehicle/add_rent_vehicle/', rent_vehicle_form, name="rent_request"),
    path('rent_vehicle_requests/', Rent_Vehicle_Requests, name='rent_vehicle_requests'),

]
