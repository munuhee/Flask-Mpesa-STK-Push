"""Functions for interacting with the M-Pesa API."""

import base64
from datetime import datetime
import requests
from app import app

def generate_access_token():
    """Generate access token for M-Pesa API authentication."""
    consumer_key = app.config['MPESA_CONSUMER_KEY']
    consumer_secret = app.config['MPESA_CONSUMER_SECRET']

    # Concatenate consumer key and consumer secret
    auth_string = consumer_key + ':' + consumer_secret

    # Encode the auth string in base64
    encoded_auth_string = base64.b64encode(auth_string.encode()).decode('utf-8')

    # Set headers for token request
    headers = {
        'Authorization': f'Basic {encoded_auth_string}'
    }

    # Make request for access token
    response = requests.get(
        'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials',
        headers=headers,
        timeout=10
        )

    # Extract access token from response
    access_token = response.json()['access_token']

    return access_token

def initiate_stk_push(phone_number, amount, reference):
    """Initiate STK push for M-Pesa payment."""
    access_token = generate_access_token()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    # Generate timestamp
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    # Concatenate Shortcode, Passkey, and Timestamp
    concat_string = f"{app.config['MPESA_SHORTCODE']}{app.config['MPESA_PASSKEY']}{timestamp}"

    # Encode the concatenated string to base64
    password = base64.b64encode(concat_string.encode()).decode()

    payload = {
        "BusinessShortCode": int(app.config['MPESA_SHORTCODE']),
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": int(app.config['MPESA_SHORTCODE']),
        "PhoneNumber": phone_number,
        "CallBackURL": "https://mydomain.com/path",
        "AccountReference": reference,
        "TransactionDesc": "Payment of X"
    }
    response = requests.request(
        "POST",
        'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
        headers = headers,
        json = payload,
        timeout = 10
        )
    print(response.text.encode('utf8'))

    return response.json()
