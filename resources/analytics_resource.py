from flask_restful import Resource
from flask_jwt_extended import jwt_required
from models import User, SupportTicket, Product, Order, OrderItem
from sqlalchemy import func
from models import db

class UserAnalyticsResource(Resource):
    @jwt_required()
    def get(self):
        """Get user analytics"""
        # Get total users count
        total_users = User.query.count()
        
        # Get users by role
        users_by_role = db.session.query(
            User.role, 
            func.count(User.id).label('count')
        ).group_by(User.role).all()
        
        # Get users by approval status
        users_by_approval = db.session.query(
            User.is_approved, 
            func.count(User.id).label('count')
        ).group_by(User.is_approved).all()
        
        return {
            'total_users': total_users,
            'users_by_role': [{'role': role, 'count': count} for role, count in users_by_role],
            'users_by_approval': [{'approved': approved, 'count': count} for approved, count in users_by_approval]
        }, 200

class TicketStatusAnalyticsResource(Resource):
    @jwt_required()
    def get(self):
        """Get ticket status analytics"""
        # Get tickets by status
        tickets_by_status = db.session.query(
            SupportTicket.status, 
            func.count(SupportTicket.id).label('count')
        ).group_by(SupportTicket.status).all()
        
        # Get total tickets
        total_tickets = SupportTicket.query.count()
        
        return {
            'total_tickets': total_tickets,
            'tickets_by_status': [{'status': status, 'count': count} for status, count in tickets_by_status]
        }, 200

class ProductStatusAnalyticsResource(Resource):
    @jwt_required()
    def get(self):
        """Get product status analytics"""
        # Get total products
        total_products = Product.query.count()
        
        # Get products by category
        products_by_category = db.session.query(
            Product.category_id,
            func.count(Product.id).label('count')
        ).group_by(Product.category_id).all()
        
        # Get products by popularity
        popular_products = Product.query.filter_by(is_popular=True).count()
        
        # Get products with low stock (less than 5)
        low_stock_products = Product.query.filter(Product.stock < 5).count()
        
        # Get total orders
        total_orders = Order.query.count()
        
        # Get total revenue (sum of all order items)
        total_revenue = db.session.query(
            func.sum(OrderItem.total_price)
        ).scalar() or 0
        
        return {
            'total_products': total_products,
            'total_categories': len(products_by_category),
            'popular_products': popular_products,
            'low_stock_products': low_stock_products,
            'total_orders': total_orders,
            'total_revenue': float(total_revenue) if total_revenue else 0
        }, 200
