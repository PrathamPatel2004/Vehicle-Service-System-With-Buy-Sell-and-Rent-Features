import struct
from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from User_Details.models import User_Details
from .models import Payment_History
import paypalrestsdk
from . import paypalConfig
from django.conf import settings

def payment_history(request):
    username = request.COOKIES.get('username')
    email = request.COOKIES.get('mail')

    payment = Payment_History.objects.all().values()
    for item in payment:
        amount = item.get('amount')
        if amount != None:
            byte_array = struct.pack('f', amount)
            dis_amount = struct.unpack('f', byte_array)[0]
            item['amount'] = dis_amount
    
    if username is not None and email is not None:
        user = User_Details.objects.get(username=username, email=email)
        if user.role=="Mechanic":
            mechanic_data = Payment_History.objects.filter(user_id=user)
            return render(request, 'Payment_history.html', {'mechanic_data': mechanic_data, 'username': username, 'email': email})
        elif user.role=="Customer":
            request_data = Payment_History.objects.filter(user_id=user)
            pending_data = Payment_History.objects.filter(user_id=user)
            is_customer = user.role == 'Customer'
            return render(request, 'Payment_history.html', {'pending_data': pending_data, 'request_data': request_data, 'username': username, 'email': email, 'is_customer': is_customer})
        elif user.role=="Admin":
            all_requests = Payment_History.objects.all()
            is_admin = user.role == 'Admin'
            pending_data = Payment_History.objects.filter(payment_status='Pending')
            return render(request, 'Payment_History.html', {'pending_data': pending_data, 'all_requests': all_requests, 'username': username, 'email': email, 'is_admin': is_admin})
    else:
        err_message = 'User Logged out. Please login again.'
        return render(request, 'login.html', {'err_message': err_message})
def create_payment(request, payment_id):
    payment = Payment_History.objects.get(payment_id=payment_id)
    username = payment.user_id.username
    email = payment.user_id.email
    service = str(payment.service_id.service_request_type)    
    amount = format(payment.payment_amount, '.2f')
    
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {"payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://localhost:8000/payment/execute/",
            "cancel_url": "http://localhost:8000/payment/cancelled/"
        },
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": service,
                    "sku": "12345",
                    "price": amount,
                    "currency": "USD",
                    "quantity": 1
                }]
            },
            "amount": {
                "total": amount,
                "currency": "USD"
            },
            "description": f"Payment for {service}"
        }]
    })

    if payment.create():
        for link in payment.links:
            if link.rel == "approval_url":
                return redirect(link.href)
    elif not payment.create():
        print("PayPal error:", payment.error)
        return render(request, 'InitiatePayment.html', {"error": payment.error})
    else:
        return render(request, 'InitiatePayment.html', {"error": payment.error})

def execute_payment(request):
    payment_id = request.GET.get('paymentId')
    payer_id = request.GET.get('PayerID')

    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": payer_id}):
        return render(request, 'payment/success.html', {"payment": payment})
    else:
        return render(request, 'payment/error.html', {"error": payment.error})
