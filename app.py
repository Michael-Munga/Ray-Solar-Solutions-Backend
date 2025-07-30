import os
from datetime import timedelta
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

from models import db
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

# Auth Route
api.add_resource(AuthResource, '/auth/<string:action>')

# M-Pesa Callback Endpoint
@app.route('/mpesa/callback', methods=['POST'])
def mpesa_callback():
    data = request.get_json()
    print("M-Pesa callback received:", data)
    return jsonify({'ResultCode': 0, 'ResultDesc': 'Accepted'}), 200

# Initiate M-Pesa Payment
@app.route('/api/pay', methods=['POST'])
def initiate_payment():
    data = request.json
    phone = data.get('phone')
    amount = data.get('amount')

    if not phone or not amount:
        return jsonify({'error': 'Missing phone or amount'}), 400

    response = lipa_na_mpesa(phone, amount)
    return jsonify(response)

# Run the app
if __name__ == "__main__":
    app.run(port=5555, debug=True)

