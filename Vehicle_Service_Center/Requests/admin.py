from django.contrib import admin

from .models import Service_Requests, Sell_Requests, Buy_Requests, Rent_Requests

admin.site.register(Service_Requests)
admin.site.register(Sell_Requests)
admin.site.register(Buy_Requests)
admin.site.register(Rent_Requests)