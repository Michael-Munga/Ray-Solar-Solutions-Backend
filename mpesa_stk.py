
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from base64 import b64encode
from mpesa_auth import get_access_token

load_dotenv()

def lipa_na_mpesa(phone, amount):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    shortcode = os.getenv("MPESA_SHORTCODE")
    passkey = os.getenv("MPESA_PASSKEY")

    password = b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": os.getenv("MPESA_CALLBACK_URL"),
        "AccountReference": "SolarPower",
        "TransactionDesc": "Energy Payment"
    }

    url = f"{os.getenv('MPESA_BASE_URL')}/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)
    return response.json()
