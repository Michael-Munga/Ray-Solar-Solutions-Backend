from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from models import db, Transaction

class TransactionResource(Resource):
    @jwt_required()
    def get(self):
        """Get all transactions for the current user"""
        user_id = get_jwt_identity()
        transactions = Transaction.query.filter_by(user_id=user_id).all()
        return [transaction.to_dict() for transaction in transactions], 200

class TransactionDetailResource(Resource):
    @jwt_required()
    def get(self, transaction_id):
        """Get a specific transaction by ID"""
        user_id = get_jwt_identity()
        transaction = Transaction.query.get_or_404(transaction_id)
        
        # Check if the transaction belongs to the current user
        if transaction.user_id != user_id:
            return {'message': 'Unauthorized'}, 403
            
        return transaction.to_dict(), 200

class TransactionCallbackResource(Resource):
    def post(self):
        """Handle M-Pesa callback"""
        data = request.get_json()
        
        # Extract relevant information from the callback
        if 'Body' in data and 'stkCallback' in data['Body']:
            callback_data = data['Body']['stkCallback']
            checkout_request_id = callback_data.get('CheckoutRequestID')
            result_code = callback_data.get('ResultCode')
            result_desc = callback_data.get('ResultDesc')
            
            # Find the transaction by checkout_request_id
            transaction = Transaction.query.filter_by(checkout_request_id=checkout_request_id).first()
            
            if transaction:
                # Update the transaction with the callback results
                transaction.result_code = str(result_code)
                transaction.result_desc = result_desc
                transaction.status = 'completed' if result_code == 0 else 'failed'
                
                db.session.commit()
                
                return {'message': 'Transaction updated successfully'}, 200
            else:
                return {'message': 'Transaction not found'}, 404
        else:
            return {'message': 'Invalid callback data'}, 400
