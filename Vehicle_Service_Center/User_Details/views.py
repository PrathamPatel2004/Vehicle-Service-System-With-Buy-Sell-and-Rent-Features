import datetime
from random import randint
from django.db import IntegrityError
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from Vehicle_Service_Center import settings
from .models import User_Details
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.template import loader
from datetime import datetime, timedelta
import qrcode

def sign_up(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User_Details.objects.filter(username=username).exists():
            return render(request, 'sign_up.html', {'err_message': 'Username already exists'})
        if User_Details.objects.filter(email=email).exists():
            return render(request, 'sign_up.html', {'err_message': 'Email already exists'})
        
        # Generate OTP
        otp = str(randint(100000, 999999))

        # Store non-file data in session
        request.session['signup_data'] = {
            'role': role,
            'username': username,
            'email': email,
            'password': password,
            'otp': otp,
            'otp_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        # Send OTP
        send_mail(
            'Your OTP for Signup',
            f'Your OTP is: {otp}',
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )
        return render(request, 'verify_otp.html', {'email': email})
    return render(request, 'sign_up.html')

def verify_otp(request):
    if request.method == 'POST':
        user_otp = request.POST.get('otp')
        signup_data = request.session.get('signup_data')

        if not signup_data:
            return render(request, 'verify_otp.html', {'err_message': "Session expired. Please start signup again."})

        # Check OTP expiration
        otp_time = datetime.strptime(signup_data['otp_timestamp'], '%Y-%m-%d %H:%M:%S')
        if datetime.now() > otp_time + timedelta(minutes=5):
            del request.session['signup_data']
            return render(request, 'verify_otp.html', {'err_message': "OTP expired. Please signup again."})

        if user_otp != signup_data['otp']:
            return render(request, 'verify_otp.html', {'err_message': "Invalid OTP"})

        # Hash the password
        hashed_password = make_password(signup_data['password'])

        # Create user
        try:
            if signup_data['role'] == 'Mechanic':
                User_Details.objects.create(
                    role=signup_data['role'],
                    username=signup_data['username'],
                    email=signup_data['email'],
                    password=hashed_password,
                    account_status = 'Pending'
                )
                return redirect('Mechanic_Data_Form')
            else:
                User_Details.objects.create(
                    role=signup_data['role'],
                    username=signup_data['username'],
                    email=signup_data['email'],
                    password=hashed_password,
                    account_status = 'Approved'
                )
        except IntegrityError:
            return render(request, 'verify_otp.html', {'err_message': "This data already exists or was submitted."})

        return render(request, 'login.html', {'message': 'Registered successfully'})
    return render(request, 'verify_otp.html')

def resend_otp(request):
    signup_data = request.session.get('signup_data')
    
    if not signup_data:
        return redirect('signup')

    new_otp = str(randint(100000, 999999))
    signup_data['otp'] = new_otp
    signup_data['otp_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    request.session['signup_data'] = signup_data

    send_mail(
        'Resent OTP for Signup',
        f'Your new OTP is: {new_otp}',
        settings.EMAIL_HOST_USER,
        [signup_data['email']],
        fail_silently=False
    )

    return render(request, 'verify_otp.html', {
        'message': 'A new OTP has been sent to your email.',
        'email': signup_data['email']
    })

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User_Details.objects.get(username=username)
            if check_password(password, user.password):
                response = redirect('dashboard')
                response.set_cookie(
                        key='username',
                        value=user.username,
                        max_age=3600,  # 1 hour
                        httponly=True,
                        samesite='Lax'
                    )
                response.set_cookie(
                        key='mail',
                        value=user.email,
                        max_age=3600,
                        httponly=True,
                        samesite='Lax'
                    )
                return response
            else:
                return render(request, 'login.html', {'err_message': 'Invalid credentials'})
        except User_Details.DoesNotExist:
            return render(request, 'login.html', {'err_message': 'Invalid username or password'})
    return render(request, 'login.html')

def dashboard(request):
    username = request.COOKIES.get('username')
    mail = request.COOKIES.get('mail')
    if username is not None and mail is not None:
        user = User_Details.objects.get(username=username, email=mail)

        if user.role == 'Admin':
            users = User_Details.objects.all()
            return render(request, 'dashboard_admin.html', {'user': users})
        elif user.role == 'Mechanic':
            user_mechanic = User_Details.objects.get(username=username, email=mail)
            return render(request, 'dashboard.html', {'user_mechanic': user_mechanic})
        elif user.role == 'Customer':
            user_customer = User_Details.objects.get(username=username, email=mail)
            return render(request, 'dashboard.html', {'user_customer': user_customer})
        else:
            return redirect('login')
    else:
        err_message = 'User Logged out. Please login again.'
        return render(request, 'login.html', {'err_message': err_message})
    
def Mechanic_Data_Form(request):
    if request.method == 'POST':
        mechanic_name = request.POST.get('mechanic_name')
        phone_number = request.POST.get('phone_number')
        date_of_birth = request.POST.get('date_of_birth')
        address = request.POST.get('address')
        image = request.FILES.get('mechanic_image')
        idetification_proof = request.FILES.get('idetification_proof')
        resume = request.FILES.get('resume')

        try:
            User_Details.objects.update(
                fullname=mechanic_name,
                phone_number=phone_number,
                date_of_birth=date_of_birth,
                address=address,
                image=image,
                identification_proof=idetification_proof,
                resume=resume
            )
            list(messages.get_messages(request))

        # Now add only the logout message
            messages.error(request, 'User Logged out. Please login again.')
            return redirect('login')
        except IntegrityError:
            return render(request, 'Mechanic_Data_Form.html', {'err_message': "This data already exists or was submitted."})
    return render(request, 'Mechanic_Data_Form.html')

def generate_user_qr(username):
    username = username
    qr = qrcode.make(str(username))
    qr.save(f"members/static/images/qr/user_{username}.png")

def Account_Approval(request):
    if request.method == 'POST':
        username = request.COOKIES.get('username')
        mail = request.COOKIES.get('mail')
        status = request.POST.get('status')

        user = User_Details.objects.get(username=username, email=mail)
        if user.role == 'admin':
            user_id = request.POST.get('user_id')
            user_to_approve = User_Details.objects.get(id=user_id)
            user_to_approve.account_status = status
            user_to_approve.save()

            if status == 'Approved':
                generate_user_qr(user_to_approve.username)
                send_mail(
                    'Account Approval',
                    f'Your account has been approved by the admin.',
                    settings.EMAIL_HOST_USER,
                    [user_to_approve.email],
                    fail_silently=False
                )
                return redirect('Account_Approval.html')
            else:
                return redirect('Account_Approval.html')
        return redirect('Account_Approval.html')
    return redirect('Account_Approval.html')