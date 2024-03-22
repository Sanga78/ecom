from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from .credentials import MpesaAccessToken, LipanaMpesaPpassword

from django.shortcuts import render, redirect
from django.contrib import messages


def home(request):
    return render(request, 'payment/home.html')


def token(request):
    consumer_key = 'cuZ4MvJ2lZqf7MHBqWv6CTVhv1GH9HXDdqlg4lErHQiWjLQ9'
    consumer_secret = 'mgRf0ffEQEshzr8JasESJNyh6Ek8H2FBMhIlkI8Hx8W2AhfkUBHFY0p37EeH11LN'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]

    return render(request, 'payment/token.html', {"token": validated_mpesa_access_token})


def pay(request):
    if request.method == "POST":
        phone = request.POST['phone']
        amount = request.POST['amount']
        access_token = MpesaAccessToken.validated_mpesa_access_token
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
            "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
            "Password": LipanaMpesaPpassword.decode_password,
            "Timestamp": LipanaMpesaPpassword.lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,
            "PartyB": LipanaMpesaPpassword.Business_short_code,
            "PhoneNumber": phone,
            "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
            "AccountReference": "Sunfresh Groceries",
            "TransactionDesc": "Paying For Frocery items"
        }

        response = requests.post(api_url, json=request, headers=headers)
        
    return redirect('store')

def stk(request):
    return render(request, 'payment/pay.html', {'navbar': 'stk'})