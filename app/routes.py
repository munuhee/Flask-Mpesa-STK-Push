import requests
import base64
from app.models import Transaction
from requests.auth import HTTPBasicAuth
from datetime import datetime
from flask import render_template, request, url_for
from app import app, db

base_url = 'https://sandbox.safaricom.co.ke/mpesa'
consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'

def get_access_token():
    """
    Fetches the access token required for API authentication.

    Returns:
        str: Access token.
    """
    endpoint = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(endpoint, auth=HTTPBasicAuth(consumer_key, consumer_secret), timeout=10)
    data = response.json()
    return data.get('access_token')

def initiate_mpesa_stk_push(phone_number, amount):
    """
    Initiates an M-Pesa STK push transaction.

    Args:
        phone_number (str): Phone number of the payer.
        amount (str): Amount to be transacted.

    Returns:
        dict: JSON response of the transaction initiation.
    """
    endpoint = f"{base_url}/stkpush/v1/processrequest"
    access_token = get_access_token()
    headers = {"Authorization": f"Bearer {access_token}"}
    my_endpoint = f"{base_url}/lnmo"
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password = f"174379{consumer_secret}{timestamp}"
    password_bytes = base64.b64encode(password.encode('utf-8'))
    data = {
        "BusinessShortCode": "174379",
        "Password": password_bytes.decode('utf-8'),
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "PartyA": phone_number,
        "PartyB": "174379",
        "PhoneNumber": phone_number,
        "CallBackURL": my_endpoint,
        "AccountReference": "TestPay",
        "TransactionDesc": "HelloTest",
        "Amount": amount
    }
    response = requests.post(endpoint, json=data, headers=headers)
    return response.json()

@app.route('/')
def home():
    """
    Home route.

    Returns:
        str: Hello World message.
    """
    return 'Hello World!'

@app.route('/lnmo', methods=['POST'])
def lnmo_result():
    """
    Callback route to handle LNMO result.

    Returns:
        str: Response indicating the LNMO result is processed.
    """
    data = request.get_data()
    # Process the LNMO result
    return "LNMO Result Processed"

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Index route for initiating payments.

    Returns:
        str: Rendered HTML template for payment initiation.
    """
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        amount = request.form.get('amount')
        name = request.form.get('name')

        if not (phone_number and amount):
            return "Phone number and amount are required"

        # Initiate M-Pesa STK push
        mpesa_response = initiate_mpesa_stk_push(phone_number, amount)
        # Handle response as per your requirements
        # Avoid printing sensitive information like mpesa_response
        return "Payment initiated successfully"

    return render_template('create.html')

@app.route('/records', methods=['GET'])
def records():
    """
    Route to display transaction records.

    Returns:
        str: Rendered HTML template for displaying transaction records.
    """
    all_transactions = Transaction.query.all()
    return render_template('records.html', transactions=all_transactions
