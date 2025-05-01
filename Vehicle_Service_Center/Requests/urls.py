from django.urls import path
from .views import Requests, buy_sell_vehicle

urlpatterns = [
    path('requests/', Requests, name='requests'),
    path('buy_vehicle_list/', buy_sell_vehicle, name='buy_vehicle_list'),
]