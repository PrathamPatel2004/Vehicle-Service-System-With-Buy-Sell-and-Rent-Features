from django.db import models

# Create your models here.
class User_Details(models.Model):
    user_id = models.AutoField(primary_key=True)
    role = models.CharField(choices=[('Customer', 'Customer'), ('Mechanic', 'Mechanic'), ('Admin', 'Admin')], max_length=10)
    account_status = models.CharField(choices=[('Approved', 'Approved'), ('Pending', 'Pending'), ('Denied', 'Denied')], max_length=10, default='Pending')
    username = models.CharField(max_length=150, unique=True)
    fullname = models.CharField(max_length=150, null=True, blank=True)
    password = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    last_login_date = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False, null=True, blank=True)
    groups = models.ManyToManyField('auth.Group', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', blank=True)
    image = models.ImageField(upload_to='members/static/Images/users/', null=True, blank=True)
    identification_proof = models.FileField(upload_to='members/static/Files/identification_proofs/', null=True, blank=True)
    resume = models.FileField(upload_to='members/static/Files/resumes/', null=True, blank=True)

    def __str__(self):
        return self.username
    

