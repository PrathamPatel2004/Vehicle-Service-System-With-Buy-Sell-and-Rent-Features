from django.db import models
from User_Details.models import User_Details
from Requests.models import Service_Requests, Rent_Requests

# Create your models here.
class Payment_History(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User_Details, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service_Requests, on_delete=models.CASCADE, null=True, blank=True)
    payment_amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(choices=[('Completed', 'Completed'), ('Pending', 'Pending'), ('Failed', 'Failed')], max_length=10)
    payment_method = models.CharField(choices=[('Credit Card', 'Credit Card'), ('Bank Transfer', 'Bank Transfer'), ('PayPal', 'PayPal')], max_length=15)
    payment_note = models.TextField(null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True, blank=True)
    authorization_code = models.CharField(max_length=200, null=True, blank=True)
    payment_gateway_response = models.TextField(null=True, blank=True)
    payment_gateway_error = models.TextField(null=True, blank=True)
    payment_gateway_transaction_id = models.CharField(max_length=200, null=True, blank=True)
    payment_gateway_authorization_code = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.payment_id)
