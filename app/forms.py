"""Module for handling Mpesa transaction forms."""
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length

class MpesaTransactionForm(FlaskForm):
    """Form class for Mpesa transaction data."""
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=50)])
    phone_number = IntegerField('Phone Number', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    reference = StringField('Reference', validators=[DataRequired()])
    submit = SubmitField('Submit')
