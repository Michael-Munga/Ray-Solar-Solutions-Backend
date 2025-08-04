from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from models import db, Order, OrderItem, CartItem, Product, Transaction, User
from datetime import datetime

class OrderListResource(Resource):
    @jwt_required()
    def get(self):
        """Get all orders for the current user"""
        user_id = get_jwt_identity()
        orders = Order.query.filter_by(customer_id=user_id).order_by(Order.created_at.desc()).all()
        return [order.to_dict() for order in orders], 200

    @jwt_required()
    def post(self):
        """Create a new order from the user's cart"""
        user_id = get_jwt_identity()
        
        # Get cart items for the user
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return {'message': 'Cart is empty'}, 400

        # Calculate total price
        total_price = sum(item.price * item.quantity for item in cart_items)

        # Create new order
        order = Order(
            customer_id=user_id,
            status='pending',
            created_at=datetime.now()
        )
        db.session.add(order)
        db.session.flush()  # Get order ID

        # Create order items from cart items
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                unit_price=cart_item.price,
                total_price=cart_item.price * cart_item.quantity
            )
            db.session.add(order_item)

        # Create a transaction for the order
        user = User.query.get(user_id)
        if user:
            transaction = Transaction(
                user_id=user_id,
                phone=user.phone if hasattr(user, 'phone') else '',
                amount=total_price,
                status='pending'
            )
            db.session.add(transaction)
            db.session.flush()  # Get transaction ID

        # Clear the cart
        for cart_item in cart_items:
            db.session.delete(cart_item)

        db.session.commit()

        # Return the created order with items
        db.session.refresh(order)
        return order.to_dict(), 201

class OrderResource(Resource):
    @jwt_required()
    def get(self, order_id):
        """Get a specific order for the current user"""
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, customer_id=user_id).first_or_404()
        return order.to_dict(), 200

    @jwt_required()
    def patch(self, order_id):
        """Update order status (admin only in future)"""
        user_id = get_jwt_identity()
        order = Order.query.filter_by(id=order_id, customer_id=user_id).first_or_404()
        
        data = request.get_json()
        if 'status' in data:
            order.status = data['status']
        
        db.session.commit()
        return order.to_dict(), 200
