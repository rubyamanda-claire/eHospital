from django.shortcuts import render,redirect,get_object_or_404
from hospitalapp.models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import requests
from requests.auth import HTTPBasicAuth
import json
from hospitalapp.credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.http import HttpResponse

# Create your views here.

def home(request):
    return render(request, 'index.html')

def starter(request):
    return render(request, 'starter-page.html')

def about(request):
    return render(request, 'about.html')

def appointment(request):

    if request.method =='POST':
        all = MyAppointment(
            name = request.POST['name'],
            email = request.POST['email'],
            phone = request.POST['phone'],
            datetime = request.POST['date'],
            department = request.POST['department'],
            doctor = request.POST['doctor'],
            message = request.POST['message']
        )
        all.save()
        messages.success(request, 'Appointment booked successfully')
        return render(request,'appointment.html')
    
    else:
        return render(request,'appointment.html')
    
   

def services(request):
    return render(request, 'services.html')
    
def departments(request):
    return render(request, 'departments.html')

def doctors(request):
    return render(request, 'doctors.html')

def contact(request):
    return render(request, 'contact.html')



def show(request):
    allappointments = MyAppointment.objects.all()
    return render(request, 'show.html', {'allappointments': allappointments})


def delete(request, id):
    myappoint = MyAppointment.objects.get(id=id)
    myappoint.delete()
    messages.success(request, 'Appointment deleted successfully')
    return redirect('/show')


def edit(request, id):
    editappointment = get_object_or_404(MyAppointment, id=id)

    if request.method == 'POST':
        editappointment.name = request.POST.get('name')
        editappointment.email = request.POST.get('email')
        editappointment.phone = request.POST.get('phone')
        editappointment.datetime = request.POST.get('date')
        editappointment.department = request.POST.get('department')
        editappointment.doctor = request.POST.get('doctor')
        editappointment.message = request.POST.get('message')
        editappointment.save()
        messages.success(request, 'Appiontment updated successfully!')
        return redirect('/show')
    
    return render(request, 'edit.html', {'editappointment': editappointment})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Check the password
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()

                # Display a message
                messages.success(request, "Account created successfully")
                return redirect('/login')
            except:
                # Display a message if the above fails
                messages.error(request, "Username already exist")
        else:
            # Display a message saying passwords don't match
            messages.error(request, "Passwords do not match")

    return render(request, 'register.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        # Check if the user exists
        if user is not None:
            # login(request, user)
            login(request,user)
            messages.success(request, "You are now logged in!")
            # Admin
            if user.is_superuser:
                return redirect('/show')

            # For Normal Users
            return redirect('/home')
        else:
            messages.error(request, "Invalid login credentials")

    return render(request, 'login.html')

#Mpesa Views

def token(request):
    consumer_key = '77bgGpmlOxlgJu6oEXhEgUgnu0j2WYxA'
    consumer_secret = 'viM8ejHgtEmtPTHd'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'token.html', {"token":validated_mpesa_access_token})

def pay(request):
     return render(request, 'pay.html')


def stk(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_data = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/callback",
            "AccountReference": "Medilab",
            "TransactionDesc": "Appointment"
        }
        response = requests.post(api_url, json=request_data, headers=headers)

        response_data = response.json()
        transaction_id = response_data.get("CheckoutRequestID", "N/A")
        result_code = response_data.get("ResponseCode", "1")  # 0 is success, 1 is failure

        if result_code == "0":
            # Only save transaction if it was successful
            transaction = Transaction(
                phone_number=phone,
                amount=amount,
                transaction_id=transaction_id,
                status="Success"
            )
            transaction.save()

            return HttpResponse(f"Transaction ID: {transaction_id}, Status: Success")
        else:
            return HttpResponse(f"Transaction Failed. Error Code: {result_code}")




def transactions_list(request):
    transactions = Transaction.objects.all().order_by('-date')
    return render(request, 'transactions.html', {'transactions': transactions})
    