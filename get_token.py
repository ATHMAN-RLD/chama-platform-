import requests
import base64
from dotenv import load_dotenv
import os

load_dotenv()

consumer_key = os.getenv('MPESA_CONSUMER_KEY')
consumer_secret = os.getenv('MPESA_CONSUMER_SECRET')

credentials = f"{consumer_key}:{consumer_secret}"
encoded_credentials = base64.b64encode(credentials.encode()).decode()

url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
headers = {
    "Authorization": f"Basic {encoded_credentials}"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)
print("Response:", response.json())   