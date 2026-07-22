import requests
import base64
import datetime
from dotenv import load_dotenv
import os

load_dotenv()

consumer_key = os.getenv('MPESA_CONSUMER_KEY')
consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')
shortcode = os.getenv('MPESA_SHORTCODE')
passkey = os.getenv('MPESA_PASSKEY')

# Step A: Get access token
credentials = f"{consumer_key}:{consumer_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
token_headers = {"Authorization": f"Basic {encoded_credentials}"}
token_response = requests.get(token_url, headers=token_headers)
access_token = token_response.json()['access_token']

print("Access token retrieved successfully.")

# Step B: Build the password and timestamp
timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
password_string = f"{shortcode}{passkey}{timestamp}"
encoded_password = base64.b64encode(password_string.encode()).decode()

# Step C: Send the STK Push request
stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

stk_headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

stk_payload = {
    "BusinessShortCode": shortcode,
    "Password": encoded_password,
    "Timestamp": timestamp,
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": "254708374149",
    "PartyB": shortcode,
    "PhoneNumber": "254708374149",
    "CallBackURL": "https://mydomain.com/callback",
    "AccountReference": "ChamaTest",
    "TransactionDesc": "Test contribution payment"
}

stk_response = requests.post(stk_url, json=stk_payload, headers=stk_headers)

print("Status Code:", stk_response.status_code)
print("Response:", stk_response.json())    