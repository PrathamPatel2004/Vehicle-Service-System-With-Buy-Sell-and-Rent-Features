from django.db import models
from User_Details.models import User_Details
from Vehicles.models import Rent_Vehicles

# Create your models here.
class Service_Requests(models.Model):
    user = models.ForeignKey(User_Details, on_delete=models.CASCADE)
    service_request_type = models.CharField(choices=[('Full Vehicle Diagnostic', 'Full Vehicle Diagnostic'), ('Routine Maintenance Service', 'Routine Maintenance Service'), ('Car Wash & Vacuuming', 'Car Wash & Vacuuming'), ('Paint Protection & Polishing', 'Paint Protection & Polishing'), ('Tyre Replacement & Oil Change', 'Tyre Replacement & Oil Change')], max_length=50)
    vehicle_type = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    vehicle_color = models.CharField(max_length=50, null=True, blank=True)
    vehicle_number = models.CharField(max_length=10)
    branch = models.CharField(choices=[('Surat', 'Surat'), ('Vadodara', 'Vadodara'), ('Ranip, Ahmedabad', 'Ranip, Ahmedabad'), ('Thaltej, Ahmedabad', 'Thaltej, Ahmedabad'), ('Mahesana', 'Mahesana')], max_length=50)
    vehicle_proof_image = models.ImageField(upload_to='members/static/images/vehicle_proof_images/', null=True, blank=True)
    status = models.CharField(choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], max_length=20)
    assigned_to = models.ForeignKey(User_Details, on_delete=models.CASCADE, related_name='assigned_to', null=True, blank=True)
    payment_status = models.CharField(choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid')], null=True, blank=True, max_length=50)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    service_date = models.DateField(null=True, blank=True)
    problem_description = models.TextField()

    def __str__(self):
        return self.user.username + ' - ' + self.service_request_type + ' - ' + self.vehicle_number
    
class Sell_Requests(models.Model):
    user = models.ForeignKey(User_Details, on_delete=models.CASCADE)
    vehicle_type = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    vehicle_model_year = models.IntegerField()
    vehicle_color = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=10)
    vehicle_used_condition = models.CharField(choices=[('New', 'New'), ('Used', 'Used')], max_length=10)
    vehicle_price = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_proof_image = models.ImageField(upload_to='members/static/images/vehicle_proof_images/')
    status = models.CharField(choices=[('Available', 'Available'), ('Sold', 'Sold'), ('Cancelled', 'Cancelled')], max_length=20)
    seller_details = models.ForeignKey(User_Details, on_delete=models.CASCADE, related_name='buyers_details', null=True, blank=True)
    seller_identification_proof = models.ImageField(upload_to='members/static/images/seller_identification_proofs/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    additional_details = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.user.username + ' - ' + self.vehicle_number + ' - '  + str(self.vehicle_price)
    
class Buy_Requests(models.Model):
    user = models.ForeignKey(User_Details, on_delete=models.CASCADE)
    vehicle_details = models.ForeignKey(Sell_Requests, on_delete=models.CASCADE)
    buyer_details = models.ForeignKey(User_Details, on_delete=models.CASCADE, related_name='sellers_details')
    buyer_payment_status = models.CharField(choices=[('Unpaid', 'Unpaid'), ('Partially Paid', 'Partially Paid'), ('Paid', 'Paid')], max_length=50)
    buyer_payment_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.user.username + ' - ' + self.vehicle_details.vehicle_number + ' - ' + self.buyer_details.username
    
class Rent_Requests(models.Model):
    user = models.ForeignKey(User_Details, on_delete=models.CASCADE)
    vehicle_details = models.ForeignKey(Rent_Vehicles, on_delete=models.CASCADE)
    renter_details = models.ForeignKey(User_Details, on_delete=models.CASCADE, related_name='rented_to', null=True, blank=True)
    rent_start_date = models.DateField()
    rent_end_date = models.DateField()
    total_hours_rented = models.IntegerField(null=True, blank=True)
    rent_payment_status = models.CharField(choices=[('Unpaid', 'Unpaid'), ('Partially Paid', 'Partially Paid'), ('Paid', 'Paid')], max_length=50)
    rent_end_date_payment_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    