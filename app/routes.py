import requests
import base64
from app.models import Transaction
from requests.auth import HTTPBasicAuth
from datetime import datetime
from flask import render_template, request, url_for
from app import app, db

base_url = 'https://sandbox.safaricom.co.ke/mpesa'
consumer_key = 'CIsPJOblN3jBHZjrvGdY9rxM7ti8D4aW9zcH3ctucLRrBCY9'
consumer_secret = 'yjD8GDfaZLKytGyfCRs7dwQvZvUAaKKscne67EutcmGR1KxCig63eGPcxXZN6AVw'

def get_access_token():
    """
    Fetches the access token required for API authentication.

    Returns:
        str: Access token.
    """
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    try:
        response = requests.request("GET", endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret), timeout=10)
        response.raise_for_status()  # Raises an error for unsuccessful requests
        data = response.json()
        return data.get('access_token')
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection error, timeout)
        print("Request failed:", e)
        return None
    except ValueError as e:
        # Handle JSON decoding error
        print("JSON decoding failed:", e)
        return None

@app.route('/home')
def home():
    """
    Route for testing purposes.
    """
    get_access_token()
    return 'Hello from Steve'

# Initiate MPESA Express Request
@app.route('/pay')
def initiate_mpesa_stk_push():
    """
    Initiates an M-Pesa STK push transaction.

    Returns:
        dict: JSON response of the transaction initiation.
    """
    amount = request.args.get('amount')
    phone = request.args.get('phone')
    if not phone or not amount:
        return "Phone number and amount are required", 400  # Return a 400 Bad Request if phone or amount is missing

    endpoint = f"{base_url}/stkpush/v1/processrequest"
    access_token = get_access_token()
    if access_token is None:
        return "Failed to fetch access token", 500  # Return a 500 Internal Server Error if access token retrieval fails

    headers = {"Authorization": f"Bearer {access_token}"}
    my_endpoint = "https://2ec9-102-135-168-102.ngrok-free.app/"  # Replace with your ngrok endpoint
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = f"174379{consumer_secret}{timestamp}"
    password_bytes = base64.b64encode(password.encode('utf-8'))
    data = {
        "BusinessShortCode": "174379",
        "Password": password_bytes.decode('utf-8'),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": phone,
        "PartyB": "174379",
        "PhoneNumber": phone,
        "CallBackURL": my_endpoint + "/lnmo-callback",
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": amount
    }
    response = requests.request("POST", endpoint, json=data, headers=headers)
    print("Response Content:", response.content)
    try:
        response.raise_for_status()  # Raise an error for unsuccessful responses
        return response.json()
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., connection error, timeout)
        print("Request failed:", e)
        return "Failed to initiate STK push", 500
    except ValueError as e:
        # Handle JSON decoding error
        print("JSON decoding failed:", e)
        return "Failed to parse response JSON", 500

@app.route('/lnmo-callback', methods=['POST'])
def incoming():
    """
    Callback endpoint for M-Pesa transaction updates.
    """
    data = request.get_json()
    print(data)
    return "OK"  # Make sure to return a string here, 'ok' should be 'OK'
