"""Endpoints for initiating payment and view records."""
from flask import request, jsonify, render_template
from app import app, db, services, models, forms

@app.route('/initiate_mpesa_stk_push', methods=['POST', 'GET'])
def initiate_mpesa_stk_push():
    """Initiate STK push for M-Pesa payment."""
    form = forms.MpesaTransactionForm()
    if form.validate_on_submit():
        full_name = form.full_name.data
        reference = form.reference.data
        phone_number = form.phone_number.data
        amount = form.amount.data

        # Convert phone_number and amount to integers
        try:
            phone_number = int(phone_number)
            amount = int(amount)
        except ValueError:
            return jsonify({'error': 'Phone number and amount must be integers.'}),

        # Add transaction to database
        new_transaction = models.MpesaTransaction(
            full_name=full_name,
            phone_number=phone_number,
            amount=amount,
            reference=reference
        )
        db.session.add(new_transaction)
        db.session.commit()

        # Initiate STK push
        response = services.initiate_stk_push(phone_number, amount, reference)

        # Check if STK push initiation was successful
        if 'ResponseCode' in response and response['ResponseCode'] == '0':
            return jsonify(response)

        # Handle error response
        error_message = response.get('ResponseDescription', 'Unknown error occurred.')
        return jsonify({'error': error_message}), 500
    else:
        errors = form.errors
        if errors:
            return jsonify({'error': 'Form validation failed', 'errors': errors}), 400
        return render_template('payment_form.html', form=form)


@app.route('/view_records', methods=['GET'])
def view_records():
    """View M-Pesa transaction records."""
    transactions = models.MpesaTransaction.query.all()
    print("Transaction records retrieved successfully.")
    return render_template('view_records.html', transactions=transactions)
