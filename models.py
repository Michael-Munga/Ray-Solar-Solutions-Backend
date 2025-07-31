from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
import re

# Naming convention 
db = SQLAlchemy(metadata=MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}))

# ========================================
# 1. USER MODEL – Auth, Roles, Providers
# ========================================
class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    role = db.Column(db.String(20), nullable=False, default='customer')  # customer, provider, admin
    is_approved = db.Column(db.Boolean, default=False)  # Only matters for providers

    # Relationships
    products = db.relationship('Product', back_populates='provider', cascade="all, delete-orphan")
    orders = db.relationship('Order', back_populates='customer')
    tickets = db.relationship('SupportTicket', back_populates='user')

    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Password hashing methods
    def set_password(self, raw_password):
        from flask_bcrypt import generate_password_hash
        self.password_hash = generate_password_hash(raw_password).decode('utf-8')

    def verify_password(self, raw_password):
        from flask_bcrypt import check_password_hash
        return check_password_hash(self.password_hash, raw_password)

    # Email format validation
    @validates("email")
    def validate_email(self, _, value):
        value = value.lower().strip()
        if not re.match(r"[A-Za-z0-9._]+@[A-Za-z0-9]+\.[a-z]{2,}$", value):
            raise ValueError("Invalid email")
        return value

    # Serialization rules
    serialize_only = ("id", "first_name", "last_name", "email", "role", "is_approved")
    serialize_rules = ("-password_hash", "-products.provider", "-orders.customer", "-tickets.user")


# =========================================================
# 2. TAG MODEL – For product filtering and feature labels
# =========================================================
product_tags = db.Table(
    'product_tags',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
)

class Tag(db.Model, SerializerMixin):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    products = db.relationship('Product', secondary=product_tags, back_populates='tags')


# ==================================================
# 3. PRODUCT MODEL – Public-facing listing
# ==================================================
class Product(db.Model, SerializerMixin):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    short_description = db.Column(db.String(255))
    description = db.Column(db.Text)

    image_url = db.Column(db.String)

    # Specifications
    wattage = db.Column(db.String)
    duration = db.Column(db.String)
    warranty_period = db.Column(db.String)
    stock = db.Column(db.Integer, default=0)

    # Pricing
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float)
    rating = db.Column(db.Float, default=0)
    num_reviews = db.Column(db.Integer, default=0)
    is_popular = db.Column(db.Boolean, default=False)

    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    provider = db.relationship('User', back_populates='products')
    tags = db.relationship('Tag', secondary=product_tags, back_populates='products')
    order_items = db.relationship('OrderItem', back_populates='product')

    @property
    def provider_name(self):
        return self.provider.full_name if self.provider else "Unknown"

    # Serialization
    serialize_only = (
        "id", "name", "short_description", "description", "price", "original_price",
        "rating", "num_reviews", "image_url", "wattage", "duration", "warranty_period",
        "stock", "is_popular", "provider_id", "provider_name", "tags.name"
    )
    serialize_rules = ("-provider.products", "-order_items.product", "-tags.products")

class Purchase(db.Model):
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Float)
    status = db.Column(db.String(50), default="pending")  # e.g. pending, paid, delivered
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref='purchases')
    product = db.relationship('Product', backref='purchases')


# ================================================
# 4. ORDER MODEL – Cart + Checkout History
# ================================================
class Order(db.Model, SerializerMixin):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(50), default='pending')  # pending, paid, shipped, delivered
    created_at = db.Column(db.DateTime, default=datetime.now)

    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    customer = db.relationship('User', back_populates='orders')
    items = db.relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")

    serialize_only = ("id", "status", "created_at", "customer_id", "items")


class OrderItem(db.Model, SerializerMixin):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))

    # Relationships
    order = db.relationship('Order', back_populates='items')
    product = db.relationship('Product', back_populates='order_items')

    serialize_only = ("id", "order_id", "product_id", "quantity", "unit_price", "total_price")


# ====================================================
# 5. SUPPORT TICKET MODEL – Help Desk Messaging
# ====================================================
class SupportTicket(db.Model, SerializerMixin):
    __tablename__ = 'support_tickets'

    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text)
    status = db.Column(db.String(50), default='open')  # open, responded, closed
    created_at = db.Column(db.DateTime, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    user = db.relationship('User', back_populates='tickets')

    serialize_only = ("id", "subject", "message", "response", "status", "created_at", "user_id")

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    checkout_request_id = db.Column(db.String(100), unique=True)
    merchant_request_id = db.Column(db.String(100))
    result_code = db.Column(db.String(10))
    result_desc = db.Column(db.String(255))
    status = db.Column(db.String(20))  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)