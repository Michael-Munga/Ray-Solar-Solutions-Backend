
import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from base64 import b64encode
from mpesa_auth import get_access_token
from models import db, Transaction

load_dotenv()

def lipa_na_mpesa(phone, amount, user_id):
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    shortcode = os.getenv("MPESA_SHORTCODE")
    passkey = os.getenv("MPESA_PASSKEY")

    password = b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

    # Generate a unique account reference
    account_reference = f"SolarPower-{user_id}-{timestamp}"

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": f"{os.getenv('BASE_URL')}/api/transactions/callback",
        "AccountReference": account_reference,
        "TransactionDesc": "Energy Payment"
    }

    url = f"{os.getenv('MPESA_BASE_URL')}/mpesa/stkpush/v1/processrequest"
    response = requests.post(url, json=payload, headers=headers)
    
    # Create a transaction record
    if response.status_code == 200:
        response_data = response.json()
        if 'CheckoutRequestID' in response_data:
            transaction = Transaction(
                phone=phone,
                amount=amount,
                checkout_request_id=response_data['CheckoutRequestID'],
                merchant_request_id=response_data.get('MerchantRequestID'),
                status='pending',
                user_id=user_id
            )
            db.session.add(transaction)
            db.session.commit()
    
    return response.json()
