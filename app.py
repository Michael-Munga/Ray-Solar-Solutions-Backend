import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask.cli import with_appcontext
import click
from datetime import datetime
from flask_jwt_extended import jwt_required

from models import db, Transaction, Purchase  # ✅ Import Transaction and Purchase models
from resources.auth import AuthResource
from mpesa_stk import lipa_na_mpesa

# Load .env variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configurations
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)

# Initialize extensions
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)
db.init_app(app)
CORS(app)
api = Api(app)

# JWT Error Handlers
@jwt.unauthorized_loader
def missing_token(error):
    return {
        "message": "Authorization required",
        "success": False,
        "errors": ["Authorization token is required"],
    }, 401

@jwt.invalid_token_loader
def invalid_token_callback(reason):
    return {"message": "Invalid token", "reason": reason}, 422

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return {"message": "Token expired"}, 401

# ============================
#        ROUTES
# ============================

# Auth Route
api.add_resource(AuthResource, '/auth/<string:action>')

# M-Pesa Payment Initiation
@app.route('/api/pay', methods=['POST'])
def initiate_payment():
    data = request.json
    phone = data.get('phone')
    amount = data.get('amount')

    if not phone or not amount:
        return jsonify({'error': 'Missing phone or amount'}), 400

    response = lipa_na_mpesa(phone, amount)
    return jsonify(response)

# M-Pesa Callback Endpoint
@app.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    data = request.get_json()
    print("M-Pesa callback received:", data)

    try:
        callback = data['Body']['stkCallback']
        merchant_request_id = callback.get('MerchantRequestID')
        checkout_request_id = callback.get('CheckoutRequestID')
        result_code = str(callback.get('ResultCode'))
        result_desc = callback.get('ResultDesc')

        # Defaults
        phone = None
        amount = None

        # Extract metadata if successful
        if result_code == '0':
            metadata = callback.get('CallbackMetadata', {}).get('Item', [])
            for item in metadata:
                if item.get("Name") == "PhoneNumber":
                    phone = str(item.get("Value"))
                elif item.get("Name") == "Amount":
                    amount = float(item.get("Value"))

        # Save transaction
        transaction = Transaction(
            phone=phone or "unknown",
            amount=amount or 0.0,
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
            result_code=result_code,
            result_desc=result_desc,
            status="success" if result_code == '0' else "failed"
        )
        db.session.add(transaction)
        db.session.commit()

        return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'}), 200

    except Exception as e:
        print("Callback processing error:", e)
        return jsonify({'ResultCode': 1, 'ResultDesc': 'Callback failed'}), 500

# Removed Product model from app.py since it is defined in models.py

# Removed Purchase model from here since it is now in models.py



class Sale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship("Product", backref="sales")

@app.route('/api/purchase-direct', methods=['POST'])
def purchase_product_direct():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    phone = data.get('phone')

    if not product_id or not quantity or not phone:
        return jsonify({'error': 'Missing data'}), 400

    product = Product.query.get(product_id)
    if not product or product.stock < quantity:
        return jsonify({'error': 'Insufficient stock or product not found'}), 400

    total_price = product.price * quantity

    # Optionally: Trigger M-Pesa here and wait for callback

    product.stock -= quantity
    sale = Sale(product_id=product_id, quantity=quantity, phone=phone, total_price=total_price)

    db.session.add(sale)
    db.session.commit()

    return jsonify({'message': 'Purchase recorded', 'total': total_price}), 201

# Optional CLI to create DB tables
@app.cli.command("create_db")
@with_appcontext
def create_db():
    db.create_all()
    click.echo("Database tables created")
    
@app.route('/api/admin/purchases', methods=['GET'])
@jwt_required()
def admin_view_purchases():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user or user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403

    purchases = Purchase.query.join(User).join(Product).add_columns(
        User.email, Product.name.label("product_name"), Purchase.quantity, 
        Purchase.total_price, Purchase.status, Purchase.timestamp
    ).all()

    result = [
        {
            "user_email": email,
            "product_name": product_name,
            "quantity": quantity,
            "total_price": total_price,
            "status": status,
            "timestamp": timestamp.isoformat()
        }
        for email, product_name, quantity, total_price, status, timestamp in purchases
    ]
    return jsonify(result), 200

@app.route('/api/admin/purchases')
@jwt_required()
def admin_purchases():
    product_name = request.args.get('product')
    start_date = request.args.get('start')
    end_date = request.args.get('end')

    query = db.session.query(Purchase, User.email, Product.name).join(User).join(Product)

    if product_name:
        query = query.filter(Product.name.ilike(f'%{product_name}%'))
    if start_date:
        query = query.filter(Purchase.timestamp >= start_date)
    if end_date:
        query = query.filter(Purchase.timestamp <= end_date)

    results = query.all()
    purchases = []
    for purchase, user_email, product_name in results:
        purchases.append({
            "user_email": user_email,
            "product_name": product_name,
            "quantity": purchase.quantity,
            "total_price": purchase.total_price,
            "status": purchase.status,
            "timestamp": purchase.timestamp.isoformat(),
        })

    return jsonify(purchases), 200


# Run the app
if __name__ == "__main__":
    app.run(port=5555, debug=True)

