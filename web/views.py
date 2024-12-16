from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from . models import *
from . forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests
from django.http import HttpResponse

from django.views.generic import DetailView
from django.urls import reverse
from django_pesapal.views import PaymentRequestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import View
from decimal import Decimal
from .models import MyPayment, Room
from .forms import MyPaymentForm
from django.shortcuts import render, get_object_or_404
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.utils.timezone import now  # Import now for timezone-aware datetime


import paho.mqtt.client as mqtt

# Create your views here.
def signup(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            if MyUser.objects.filter(email=email).exists():
                messages.info(request, f"Email {email} Already Taken")
                return redirect('signup')
            elif MyUser.objects.filter(username=username).exists():
                messages.info(request, f"Username {username} Already Taken")
                return redirect('signup')
            else:
                user = MyUser.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name, password=password)
                user.save()
                # messages.info(request, 'Registered succesefull.')
                return redirect('signin')
        else:
            messages.info(request, 'The Two Passwords Not Matching')
            return redirect('signup')

    else:
        return render(request, 'web/signup.html')

def signin(request):
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            # messages.info(request, 'Loged in succesefull.')
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
            return redirect('signin')

    else:
        return render(request, 'web/signin.html')

def logout(request):
    auth.logout(request)
    # messages.info(request, 'Loged out succesefull.')
    return redirect('signin')



import paho.mqtt.client as mqtt
from django.http import HttpResponse
from django.shortcuts import render

# MQTT Broker details
mqtt_broker = "164.90.230.152"
mqtt_port = 1883

def control_esp8266(request, device_id, command):
    topic = f"home/esp8266/{device_id}/control"
    client = mqtt.Client()
    client.connect(mqtt_broker, mqtt_port, 60)
    client.publish(topic, command)
    return redirect('manual_control')
    # return HttpResponse(f"Command '{command}' sent to {device_id}")
    
def mytesting(self):
        # Fetch expired payments where the current time is >= end_date
        expired_payments = MyPayment.objects.filter(end_date__lte=now(), Payment_status='paid')

        for payment in expired_payments:
            room_number = payment.Room.Room_Number
        try:
            if room_number == "1":
                topic = f"home/esp8266/mydevicecontrol/control"
                client = mqtt.Client()
                client.connect(mqtt_broker, mqtt_port, 60)
                client.publish(topic, 'highdoorone')
            elif room_number == "2":
                    topic = f"home/esp8266/mydevicecontrol/control"
                    client = mqtt.Client()
                    client.connect(mqtt_broker, mqtt_port, 60)
                    client.publish(topic, 'highdoorone')
        except Exception as e:
            print(f"Error processing room {room_number}: {e}")




def home(request):
    return render(request, 'web/home.html')
def aboutus(request):
    return render(request, 'web/aboutus.html')
def base(request):
    return render(request, 'web/base.html')
def contactus(request):
    return render(request, 'web/contactus.html')
def contactpost(request):
    contactpost = ContactForm()
    if request.method == "POST":
        Full_Name = request.POST.get('Full_Name')
        Email = request.POST.get('Email')
        Message = request.POST.get('Message')
        Phone = request.POST.get('Phone')
        contactpost = ContactForm(request.POST, files=request.FILES)
        if contactpost.is_valid():
            contactpost.save()
            return redirect('contactpost')
    context={
        "contactpost":contactpost
    }
    return render(request, 'web/contactpost.html',context)
@login_required(login_url='signin')
def contactlist(request):
    contactlist = Contact.objects.all()
    countmessage= Contact.objects.all().count()
    context={
        "contactlist":contactlist,
        "countmessage":countmessage
    }
    return render(request, 'web/contactlist.html', context)
@login_required(login_url='signin')
def viewcontact(request, id):
    contact = Contact.objects.get(id=id)
    
    context = {"contact":contact}
    return render(request, 'web/viewcontact.html', context)
@login_required(login_url='signin')
def deletecontact(request, id):
    contact = Contact.objects.get(id=id)
    if request.method == "POST":
        contact.delete()
        return redirect('contactlist')
    
    context = {"contact":contact}
    return render(request, 'web/deletecontact.html', context)


@login_required(login_url='signin')
def dashboard(request):
    return render(request, 'web/dashboard.html')

def services(request):
    return render(request, 'web/services.html')

def house(request):
    room = Room.objects.all()
    context={
        "room":room
    }
    return render(request, 'web/house.html', context)
def houseoneroom(request):
    return render(request, 'web/houseoneroom.html')
def housetworoom(request):
    return render(request, 'web/housetworoom.html')

def faq(request):
    return render(request, 'web/faq.html')
def pricing(request):
    return render(request, 'web/pricing.html')

def privancy(request):
    return render(request, 'web/privancy.html')


def roompost(request):
    roompost = RoomForm()
    if request.method == "POST":
        roompost = RoomForm(request.POST, files=request.FILES)
        if roompost.is_valid():
            roompost.save()
            messages.info(request, 'Uploaded succesefull.')
            return redirect('roompost')
    context={
        "roompost":roompost
    }
    return render(request, 'web/roompost.html',context)

def mypayment(request):
    userpayment = MyPayment.objects.filter(user=request.user).order_by('-id')
    context={
        "userpayment":userpayment
    }
    return render(request, 'web/mypayment.html', context)

def allpayment(request):
    userpayment = MyPayment.objects.all().order_by('-id')
    context={
        "userpayment":userpayment
    }
    return render(request, 'web/allpayment.html', context)

def manual_control(request):
    return render(request, 'web/manual_control.html')


    
class viewroom(DetailView):
    model = Room
    template_name = 'web/viewroom.html'
    payment_form_class = MyPaymentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # Fetch the Room object
        payment_form = self.payment_form_class(request.POST)

        if 'payment_submit' in request.POST:  # Check for the form submission
            if payment_form.is_valid():
                userpayment = MyPayment.objects.filter(user=request.user, Payment_status="paid").last()
                # Extract form data
                Month = int(payment_form.cleaned_data['Month'])
                Cost = self.object.Cost * Month
                
                if userpayment:
                    end_date = userpayment.end_date + relativedelta(months=Month)  # Use relativedelta for accurate month addition
                else:
                    end_date = now() + relativedelta(months=Month)  # Use relativedelta for accurate month addition
                # Create a new payment record
                payment = MyPayment.objects.create(
                    user=request.user,
                    Room=self.object,
                    Room_Name=self.object.Room_Name,
                    Month=Month,
                    Cost=Cost,
                    Payment_status='pending',
                    end_date=end_date
                )

                # Store session data for the payment
                request.session['unique_code'] = str(payment.unique_code)
                request.session['Cost'] = f"{Cost:.2f}"
                request.session['product_name'] = slugify(self.object.Room_Name)
                request.session['Room_Number'] = slugify(self.object.Room_Number)

                # Redirect to the payment view with required parameters
                return redirect(reverse('payment', kwargs={'product_id': self.object.id}))
        
        # If the form is invalid, re-render the page with the form
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass payment_form to the template context
        context['payment_form'] = kwargs.get('payment_form', self.payment_form_class())
        return context


# FOR PAYMENT
class PaymentView(LoginRequiredMixin, View, PaymentRequestMixin):
    """
    Make payment view
    """
    
    template_name = "web/payment.html"
    
    def get(self, request, product_id):
        unique_code = request.session.get('unique_code')
        product_name = request.session.get('product_name')
        Room_Number = request.session.get('Room_Number')
        amount = Decimal(request.session.get('Cost', '0.00'))
        
        context = {
            'product_id': product_id,
        }

        # Store the unique_code in the session
        request.session['unique_code'] = unique_code
        request.session['product_id'] = product_id
        request.session['Room_Number'] = Room_Number

        # Generate payment order info
        order_info = {
            "amount": amount,
            "description": f"Payment for {product_name}",
            "reference": product_id,  # Use payment ID as reference
            "email": request.user.email,  # Use user's email for payment
        }

        # Generate the Pesapal payment URL
        pesapal_url = self.get_payment_url(**order_info)

        # Render the payment page template with Pesapal URL
        return render(request, self.template_name, {'pesapal_url': pesapal_url})
    
    
def payment_completed(request):
    # Assuming the transaction ID is passed as a GET parameter
    transaction_id = request.GET.get('pesapal_transaction_tracking_id')
    payment = MyPayment.objects.filter(user=request.user).last()
    unique_code = request.session.get('unique_code')
    product_id = request.session.get('product_id')
    Room_Number = request.session.get('Room_Number')
    
    if payment:
        product_id = product_id
        payment = get_object_or_404(MyPayment, unique_code=unique_code,  user=request.user)

        # Update the payment status to 'paid'
        payment.Payment_status = 'paid'
        payment.transaction_id = transaction_id
        payment.save()
        
        if Room_Number == "1":
            try:
                topic = f"home/esp8266/mydevicecontrol/control"
                client = mqtt.Client()
                client.connect(mqtt_broker, mqtt_port, 60)
                client.publish(topic, 'lowdoorone')
                return redirect(reverse('viewroom', args=[product_id]))
            except requests.exceptions.RequestException as e:
                return JsonResponse({"status": "error", "message": str(e)})

            return redirect(reverse('viewroom', args=[product_id]))
        elif Room_Number == "2":
            try:
                topic = f"home/esp8266/mydevicecontrol/control"
                client = mqtt.Client()
                client.connect(mqtt_broker, mqtt_port, 60)
                client.publish(topic, 'lowdoortwo')
                return redirect(reverse('viewroom', args=[product_id]))
            except requests.exceptions.RequestException as e:
                return JsonResponse({"status": "error", "message": str(e)})

            return redirect(reverse('viewroom', args=[product_id]))
        elif Room_Number == "3":
            try:
                topic = f"home/esp8266/mydevicecontrol/control"
                client = mqtt.Client()
                client.connect(mqtt_broker, mqtt_port, 60)
                client.publish(topic, 'lowdoorthree')
                return redirect(reverse('viewroom', args=[product_id]))
            except requests.exceptions.RequestException as e:
                return JsonResponse({"status": "error", "message": str(e)})

            return redirect(reverse('viewroom', args=[product_id]))
        elif Room_Number == "4":
            try:
                topic = f"home/esp8266/mydevicecontrol/control"
                client = mqtt.Client()
                client.connect(mqtt_broker, mqtt_port, 60)
                client.publish(topic, 'lowdoorfour')
                return redirect(reverse('viewroom', args=[product_id]))
            except requests.exceptions.RequestException as e:
                return JsonResponse({"status": "error", "message": str(e)})

            return redirect(reverse('viewroom', args=[product_id]))
        elif Room_Number == "5":
            try:
                topic = f"home/esp8266/mydevicecontrol/control"
                client = mqtt.Client()
                client.connect(mqtt_broker, mqtt_port, 60)
                client.publish(topic, 'lowdoorfive')
                return redirect(reverse('viewroom', args=[product_id]))
            except requests.exceptions.RequestException as e:
                return JsonResponse({"status": "error", "message": str(e)})

            return redirect(reverse('viewroom', args=[product_id]))
    else:
        # Handle the case where transaction_id is not found
        # For demonstration, using the latest payment for the user
        payment = MyPayment.objects.filter(user=request.user).last()
        if payment:
            product_id = payment.product_id
            return redirect(reverse('viewroom', args=[product_id]))
        else:
            # Handle the case where no payments are found for the user
            return redirect('home')  # Or any other appropriate view