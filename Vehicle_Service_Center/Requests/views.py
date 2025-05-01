from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from .models import Service_Requests, Sell_Requests, Buy_Requests, Rent_Requests
from User_Details.models import User_Details
from Payments.models import Payment_History
from django.contrib import messages

def Requests(request):
    username = request.COOKIES.get('username')
    email = request.COOKIES.get('mail')

    user = User_Details.objects.get(username=username)
    
    if user.role=="Mechanic":
        mechanic_data = Service_Requests.objects.filter(assigned_to=user)
        return render(request, 'Service_Requests.html', {'mechanic_data': mechanic_data, 'username': username, 'email': email})
    elif user.role=="Customer":
        request_data = Service_Requests.objects.filter(user=user)
        is_customer = user.role == 'Customer'
        return render(request, 'Service_Requests.html', {'request_data': request_data, 'username': username, 'email': email, 'is_customer': is_customer})
    elif user.role=="Admin":
        all_requests = Service_Requests.objects.all()
        is_admin = user.role == 'Admin'
        pending_requests = Service_Requests.objects.filter(status='Pending')
        return render(request, 'Service_Requests.html', {'pending_requests': pending_requests, 'all_requests': all_requests,'is_admin':is_admin, 'username': username, 'email': email})
    else:
        err_message = 'User Logged out. Please login again.'
        return redirect('login')
def New_Request(request):
    err_message = None
    message = None
    username = request.COOKIES.get('username')
    email = request.COOKIES.get('mail')

    if request.method == 'POST':
        vehicle_type = request.POST.get('vehicle_type')
        service_type = request.POST.get('service_type')
        vehicle_model = request.POST.get('vehicle_model')
        vehicle_number = request.POST.get('vehicle_number')
        branch = request.POST.get('branch')
        date = request.POST.get('date')
        problem_description = request.POST.get('problem_description')

        existing_request = Service_Requests.objects.filter(vehicle_number=vehicle_number, status="Pending").first()
        if existing_request:
            err_message = "Your vehicle is already in service"
            return render(request, 'new_service_request.html', {
                'err_message': err_message,
                'username': username,
                'email': email
            })
        
        try:
            user = User_Details.objects.get(username=username)
            New_Request = Service_Requests.objects.create(
                user=user,
                service_request_type=service_type,
                vehicle_type=vehicle_type,
                vehicle_model=vehicle_model,
                vehicle_number=vehicle_number,
                branch=branch,
                service_date=date,
                problem_description=problem_description,
                # status and payment_status will default to 'Pending'
            )
            New_Request.save()

            send_mail(
                f'New Service Request from {user}',
                f'{user} has requested a service for {service_type} on for vehicle {vehicle_number}',
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )

            #payment = Payment_History.objects.create(
            #    username=user,
            #    service_type = service_type,
            #    vehicle_number = vehicle_number,
            #    problem_description = problem_description,
            #    amount = 0,
            #    status = "Pending",
            #    Receipt = "Payment Pending"
            #)
            #payment.save()

            messages.success(request, "Your vehicle service request has been submitted")
            return redirect('requests')

        except Exception as e:
            err_message = f"An error occurred: {str(e)}"
            print(err_message)
            return render(request, 'new_service_request.html', {
                'err_message': err_message,
                'username': username,
                'email': email
            })

    # Render the form for GET requests
    return render(request, 'new_service_request.html', {
        'err_message': err_message,
        'username': username,
        'email': email
    })

def buy_sell_vehicle(request):
    username = request.COOKIES.get('username')
    email = request.COOKIES.get('mail')

    # Get all vehicles
    vehicle_data = Sell_Requests.objects.all().values()
    user = User_Details.objects.get(username=username)
    is_customer = user.role == 'Customer'
    
    # Get only available vehicles
    available_vehicles = Sell_Requests.objects.filter(status='Available').values()

    context = {
        'username': username,
        'email':email,
        'is_customer': is_customer,
        'vehicle_data': vehicle_data,
        'vehicle_available': available_vehicles,
    }

    return render(request, 'buy_sell_vehicle.html', context)

def Rent_Vehicle_Requests(request):
    username = request.COOKIES.get('username')
    email = request.COOKIES.get('mail')

    user = User_Details.objects.get(username=username)

    if user.role=="Admin":
        request_data = Rent_Requests.objects.all()
        is_admin = user.role == 'Admin'
        return render(request, 'rent_vehicle_requests.html', {'request_data': request_data,'is_admin':is_admin, 'username': username, 'email': email})