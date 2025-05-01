from datetime import timezone
from django.db import models
from User_Details.models import User_Details

# Create your models here.
class Rent_Vehicles(models.Model):
    vehicle_id = models.AutoField(primary_key=True)
    vehicle_type = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    vehicle_milage = models.IntegerField(default=0)
    vehicle_capacity = models.IntegerField(default=1)
    vehicle_fuel_type = models.CharField(max_length=50)
    vehicle_model_year = models.IntegerField()
    vehicle_color = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=10)
    vehicle_price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_image = models.ImageField(upload_to='members/static/images/vehicle_images/')
    vehicle_proof_image = models.ImageField(upload_to='members/static/images/vehicle_proof_images/')
    status = models.CharField(choices=[('Available', 'Available'), ('Rented_currently','Rented_currently'), ('In_Service', 'In_Service') ], max_length=20)
 
    def __str__(self):
        return self.vehicle_number
    
class Vehicles_For_Sell(models.Model):
    CONDITION_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Fair', 'Fair'),
        ('Poor', 'Poor'),
    ]

    FUEL_TYPE_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Sold', 'Sold'),
    ]

    user = models.ForeignKey(User_Details, on_delete=models.CASCADE)
    vehicle_model = models.CharField(max_length=100)
    vehicle_mileage = models.PositiveIntegerField(help_text="Enter mileage in kilometers")
    used_years = models.PositiveIntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    vehicle_image = models.ImageField(upload_to='vehicles_for_sale/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    date_listed = models.DateTimeField(default=timezone)

    def __str__(self):
        return f"{self.vehicle_model} - {self.user.username}"
