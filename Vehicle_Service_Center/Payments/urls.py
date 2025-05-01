from django.urls import path
from .views import payment_history, create_payment

urlpatterns = [
    path('payment_history/', payment_history, name='payment_history'),
    path('create-payment/<int:payment_id>', create_payment, name='create-payment'),
]