from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from models import User, db
from flask_bcrypt import Bcrypt
import re

bcrypt = Bcrypt()
EMAIL_RE = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")

class AuthResource(Resource):
    def post(self, action):
        data = request.get_json() or {}
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()

        if not email or not password:
            return {"error": "Email and password are required"}, 400
        if not EMAIL_RE.match(email):
            return {"error": "Invalid email format"}, 400

        # ---------------------------------------
        # LOGIN
        # ---------------------------------------
        if action == "login":
            user = User.query.filter_by(email=email).first()
            if not user or not user.verify_password(password):
                return {"error": "Invalid email or password"}, 401

            token = create_access_token(identity=user.id)

            # Determine role-based redirect URL
            if user.role == "admin":
                redirect_url = "/admin/dashboard"
            elif user.role == "provider":
                redirect_url = "/provider/dashboard"
            else:
                redirect_url = "/customer/dashboard"

            return {
                "user": user.to_dict(),
                "access_token": token,
                "redirect_url": redirect_url
            }, 200

        # ---------------------------------------
        # REGISTER customers only
        # ---------------------------------------
        elif action == "register":
            if not first_name or not last_name:
                return {"error": "First and last name are required"}, 400
            if User.query.filter_by(email=email).first():
                return {"error": "Email already exists"}, 409

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password_hash=hashed_password,
                role="customer",  # default to customer
                is_approved=True 
            )

            db.session.add(new_user)
            db.session.commit()

            token = create_access_token(identity=new_user.id)

            return {
                "user": new_user.to_dict(),
                "access_token": token,
                "redirect_url": "/customer/dashboard"
            }, 201

        # ---------------------------------------
        # UNSUPPORTED ACTION
        # ---------------------------------------
        else:
            return {"error": "Unsupported auth action"}, 400
