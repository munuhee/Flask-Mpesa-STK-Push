from app import db

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=True)
    phone_number = db.Column(db.String(15), nullable=False)
    amount = db.Column(db.Integer, nullable=False)

    def __init__(self, phone_number, amount, name=None):
        self.name = name
        self.phone_number = phone_number
        self.amount = amount
