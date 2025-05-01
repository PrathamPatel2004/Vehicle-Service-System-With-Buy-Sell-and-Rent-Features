from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from User_Details.models import User_Details
from Requests.models import Rent_Requests
from .models import Rent_Vehicles, Vehicles_For_Sell
# Create your views here.

def rent_vehicle(request):
    username = request.COOKIES.get('username')
    email = request.COOKIES.get('mail')

    if username is not None and email is not None:
    # Get all vehicles
        user = User_Details.objects.get(username=username, email=email)
        vehicle_data = Rent_Vehicles.objects.all().values()
        
        # Get only available vehicles
        available_vehicles = Rent_Vehicles.objects.filter(status='Available').values()
        if user.role == 'Admin' :
            is_admin = True
        context = {
            'username': username,
            'email':email,
            'vehicle_data': vehicle_data,
            'vehicle_available': available_vehicles,
            'is_admin': is_admin,
        }
    
        return render(request, 'rent_vehicle_list.html', context)
    else:
        # This reads and clears all existing messages
        list(messages.get_messages(request))

        # Now add only the logout message
        messages.error(request, 'User Logged out. Please login again.')
        return redirect('login')

def rent_vehicle_form(request, vehicle_id):
    username = request.COOKIES.get('username')
    email = request.COOKIES.get('mail')
    vehicle = Rent_Vehicles.objects.get(vehicle_id=vehicle_id)
    if request.method == 'POST':
        rent_date = request.POST.get('rent_date')
        rent_end_date = request.POST.get('rent_end_date')
        if User_Details.objects.filter(username=username).exists():
            user = User_Details.objects.get(username=username)
            if vehicle.status == 'Available':
                s = Rent_Requests.objects.create(user=user, vehicle_details=vehicle,rent_start_date=rent_date,rent_end_date=rent_end_date,rent_payment_status='Pending')
                s.save()
                rent_request_success = "Your rent request has been submitted successfully. Please wait for the service provider's response."
                return render(request, 'dashboard.html', {'rent_request_success':rent_request_success,'username': username, 'email': email})
            else:
                rent_request_failed = "Sorry, the vehicle is not available at the moment."
                return render(request, 'rent_vehicle_list.html', {'rent_request_failed':rent_request_failed,'username': username, 'email': email})
        return render(request, 'rent_vehicle_form.html', {'vehicle':vehicle, 'username': username, 'email': email})
    return render(request, 'rent_vehicle_form.html', {'vehicle':vehicle, 'username': username, 'email': email})

def add_vehicle(request):
    if request.method == 'POST' and request.FILES.get('vehicle_image'):
        vehicle_model = request.POST.get('vehicle_model')
        vehicle_mileage = request.POST.get('vehicle_mileage')
        used_years = request.POST.get('used_years')
        fuel_type = request.POST.get('fuel_type')
        condition = request.POST.get('condition')
        location = request.POST.get('location')
        price = request.POST.get('price')
        vehicle_image = request.FILES['vehicle_image']  # Get uploaded image
        description = request.POST.get('description')

        # Validation
        if not vehicle_model or not vehicle_mileage or not used_years or not fuel_type or not condition or not location or not price or not vehicle_image:
            messages.error(request, "Please fill out all required fields.")
            return render(request, 'add_vehicle.html')

        try:
            # Save the vehicle to the database
            vehicle = Vehicles_For_Sell(
                vehicle_model=vehicle_model,
                vehicle_mileage=vehicle_mileage,
                used_years=used_years,
                fuel_type=fuel_type,
                condition=condition,
                location=location,
                price=price,
                vehicle_image=vehicle_image,
                description=description
            )
            vehicle.save()
            messages.success(request, "Vehicle added successfully.")
            return redirect('buy_vehicle_list')  # Redirect to another page after successful submission
        except Exception as e:
            messages.error(request, f"Error adding vehicle: {str(e)}")
            return render(request, 'add_vehicle.html')

    return render(request, 'add_vehicle.html')

def add_rent_vehicle(request):
    if request.method == 'POST':
            vehicle = Rent_Vehicles(
                vehicle_type=request.POST.get('vehicle_type'),
                vehicle_model=request.POST.get('vehicle_model'),
                vehicle_milage=request.POST.get('vehicle_milage'),
                vehicle_capacity=request.POST.get('vehicle_capacity'),
                vehicle_fuel_type=request.POST.get('vehicle_fuel_type'),
                vehicle_model_year=request.POST.get('vehicle_model_year'),
                vehicle_color=request.POST.get('vehicle_color'),
                vehicle_number=request.POST.get('vehicle_number'),
                vehicle_price_per_hour=request.POST.get('vehicle_price_per_hour'),
                vehicle_image=request.FILES.get('vehicle_image'),
                vehicle_proof_image=request.FILES.get('vehicle_proof_image'),
                status=request.POST.get('status')
            )
            vehicle.save()
            return redirect('rent_vehicle')  # Or wherever you want to go after saving
    return render(request, 'add_rent_vehicle.html')