from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from models import db, User, Product, Order, SupportTicket, Category
from sqlalchemy import func

class AdminUserResource(Resource):
    @jwt_required()
    def get(self, user_id=None):
        """Get all users or a specific user (admin only)"""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        # If user_id is provided, get specific user
        if user_id is not None:
            user = User.query.get_or_404(user_id)
            return user.to_dict(), 200
        else:
            # Get all users
            users = User.query.all()
            return [user.to_dict() for user in users], 200

    @jwt_required()
    def post(self):
        """Create a new user (admin only)"""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        data = request.get_json()
        required_fields = ['first_name', 'last_name', 'email', 'password']
        for field in required_fields:
            if field not in data:
                return {'message': f'Missing {field}'}, 400

        # Check if email already exists
        if User.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 409

        # Create new user
        new_user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            role=data.get('role', 'customer'),
            is_approved=data.get('is_approved', True)
        )
        new_user.set_password(data['password'])
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user.to_dict(), 201

    @jwt_required()
    def patch(self, user_id):
        """Update user role or approval status (admin only)"""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        user = User.query.get_or_404(user_id)
        data = request.get_json()

        if 'role' in data:
            user.role = data['role']
        if 'is_approved' in data:
            user.is_approved = data['is_approved']

        db.session.commit()
        return user.to_dict(), 200

    @jwt_required()
    def delete(self, user_id):
        """Delete a user (admin only)"""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}, 200


class AdminProductResource(Resource):
    @jwt_required()
    def get(self, product_id=None):
        """Get all products or a specific product (admin only)"""
        # Check if user is admin
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        # If product_id is provided, get specific product
        if product_id is not None:
            product = Product.query.get_or_404(product_id)
            return product.to_dict(), 200
        else:
            # Get all products
            products = Product.query.all()
            return [product.to_dict() for product in products], 200

    @jwt_required()
    def post(self):
        """Create a new product (admin only)"""
        # Check if user is admin
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        data = request.get_json()
        required_fields = ['name', 'description', 'price', 'category_id']
        for field in required_fields:
            if field not in data:
                return {'message': f'Missing {field}'}, 400

        product = Product(
            name=data['name'],
            short_description=data.get('short_description', ''),
            description=data['description'],
            image_url=data.get('image_url', ''),
            wattage=data.get('wattage', ''),
            duration=data.get('duration', ''),
            warranty_period=data.get('warranty_period', ''),
            stock=data.get('stock', 0),
            price=data['price'],
            original_price=data.get('original_price', data['price']),
            is_popular=data.get('is_popular', False),
            category_id=data['category_id'],
            provider_id=user_id  # Admin acts as provider
        )

        db.session.add(product)
        db.session.commit()
        return product.to_dict(), 201

    @jwt_required()
    def patch(self, product_id):
        """Update a product (admin only)"""
        # Check if user is admin
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        product = Product.query.get_or_404(product_id)
        data = request.get_json()

        # Update allowed fields
        updatable_fields = ['name', 'short_description', 'description', 'image_url', 
                           'wattage', 'duration', 'warranty_period', 'stock', 'price', 
                           'original_price', 'is_popular', 'category_id']
        
        for field in updatable_fields:
            if field in data:
                setattr(product, field, data[field])

        db.session.commit()
        return product.to_dict(), 200

    @jwt_required()
    def delete(self, product_id):
        """Delete a product (admin only)"""
        # Check if user is admin
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Product deleted'}, 200


class AdminOrderResource(Resource):
    @jwt_required()
    def get(self, order_id=None):
        """Get all orders or a specific order (admin only)"""
        # Check if user is admin
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        # If order_id is provided, get specific order
        if order_id is not None:
            order = Order.query.get_or_404(order_id)
            return order.to_dict(), 200
        else:
            # Get all orders
            orders = Order.query.all()
            return [order.to_dict() for order in orders], 200

    @jwt_required()
    def patch(self, order_id):
        """Update order status (admin only)"""
        # Check if user is admin
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        order = Order.query.get_or_404(order_id)
        data = request.get_json()

        if 'status' in data:
            order.status = data['status']

        db.session.commit()
        return order.to_dict(), 200


class AdminTicketResource(Resource):
    @jwt_required()
    def get(self, ticket_id=None):
        """Get all support tickets or a specific ticket (admin only)"""
        # Check if user is admin
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        # If ticket_id is provided, get specific ticket
        if ticket_id is not None:
            ticket = SupportTicket.query.get_or_404(ticket_id)
            return ticket.to_dict(), 200
        else:
            # Get all tickets
            tickets = SupportTicket.query.all()
            return [ticket.to_dict() for ticket in tickets], 200

    @jwt_required()
    def patch(self, ticket_id):
        """Respond to a support ticket (admin only)"""
        # Check if user is admin
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        ticket = SupportTicket.query.get_or_404(ticket_id)
        data = request.get_json()

        if 'response' in data:
            ticket.response = data['response']
            ticket.status = data.get('status', 'closed')

        db.session.commit()
        return ticket.to_dict(), 200


class AdminDashboardResource(Resource):
    @jwt_required()
    def get(self):
        """Get admin dashboard statistics"""
        # Check if user is admin
        user_id = get_jwt_identity()
        current_user = User.query.get(user_id)
        if not current_user or current_user.role != 'admin':
            return {'message': 'Unauthorized'}, 403

        # Get statistics
        total_users = User.query.count()
        total_products = Product.query.count()
        total_orders = Order.query.count()
        total_tickets = SupportTicket.query.count()
        
        # Get recent orders
        recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
        
        # Get pending tickets
        pending_tickets = SupportTicket.query.filter_by(status='open').count()
        
        # Get sales data (sum of all order items)
        total_revenue = db.session.query(
            func.sum(OrderItem.total_price)
        ).scalar() or 0

        return {
            'total_users': total_users,
            'total_products': total_products,
            'total_orders': total_orders,
            'total_tickets': total_tickets,
            'pending_tickets': pending_tickets,
            'total_revenue': float(total_revenue) if total_revenue else 0,
            'recent_orders': [order.to_dict() for order in recent_orders]
        }, 200
