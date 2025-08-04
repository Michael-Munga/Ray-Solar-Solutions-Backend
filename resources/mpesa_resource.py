from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from mpesa_stk import lipa_na_mpesa
from models import db, Transaction, User

class MpesaSTKPushResource(Resource):
    @jwt_required()
    def post(self):
        """Initiate M-Pesa STK Push for payment"""
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'phone' not in data or 'amount' not in data:
            return {'message': 'Missing phone or amount'}, 400
            
        phone = data.get('phone')
        amount = data.get('amount')
        
        # Validate amount
        if not isinstance(amount, (int, float)) or amount <= 0:
            return {'message': 'Invalid amount'}, 400
            
        # Validate phone number format
        if not isinstance(phone, str) or len(phone) < 10:
            return {'message': 'Invalid phone number'}, 400
            
        try:
            # Initiate STK push
            response = lipa_na_mpesa(phone, amount, user_id)
            
            # Update transaction with merchant request ID if available
            if 'MerchantRequestID' in response:
                transaction = Transaction.query.filter_by(
                    checkout_request_id=response.get('CheckoutRequestID')
                ).first()
                
                if transaction:
                    transaction.merchant_request_id = response['MerchantRequestID']
                    db.session.commit()
            
            return response, 200
        except Exception as e:
            return {'message': f'Failed to initiate payment: {str(e)}'}, 500
