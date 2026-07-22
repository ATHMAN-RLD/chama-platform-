import requests
import base64
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

consumer_key = os.getenv('MPESA_CONSUMER_KEY')
consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
shortcode = os.getenv('MPESA_SHORTCODE')
passkey = os.getenv('MPESA_PASSKEY')


def get_access_token():
    credentials = f"{consumer_key}:{consumer_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    headers = {"Authorization": f"Basic {encoded_credentials}"}

    response = requests.get(url, headers=headers)
    return response.json()['access_token']


def initiate_stk_push(phone_number, amount, account_reference, transaction_desc):
    access_token = get_access_token()

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password_string = f"{shortcode}{passkey}{timestamp}"
    encoded_password = base64.b64encode(password_string.encode()).decode()

    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": shortcode,
        "Password": encoded_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://mydomain.com/callback",
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()  