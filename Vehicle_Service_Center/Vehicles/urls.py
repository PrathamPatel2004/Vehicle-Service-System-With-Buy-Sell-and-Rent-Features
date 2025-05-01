from django.urls import path
from .views import rent_vehicle, rent_vehicle_form

urlpatterns = [
    path('rent_vehicle/', rent_vehicle , name='rent_vehicle'),
    path('rent_request/<int:vehicle_id>/', rent_vehicle_form, name='rent_request'),
]