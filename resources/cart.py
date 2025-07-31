from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from models import db, CartItem, Product

class CartResource(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        items = CartItem.query.filter_by(user_id=user_id).all()
        return [item.to_dict() for item in items], 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        data = request.get_json()
        if not data or 'product_id' not in data:
            return {'message': 'Missing product_id'}, 400

        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)

        # Validate types
        if not isinstance(product_id, int) or not isinstance(quantity, int):
            return {'message': 'product_id and quantity must be integers'}, 400

        product = Product.query.get(product_id)
        if not product:
            return {'message': 'Product not found'}, 404

        existing = CartItem.query.filter_by(user_id=user_id, product_id=product.id).first()
        if existing:
            existing.quantity += quantity
        else:
            existing = CartItem(
                user_id=user_id,
                product_id=product.id,
                quantity=quantity,
                price=product.price,
                name=product.name,
                image=product.image_url
            )
            db.session.add(existing)

        db.session.commit()
        return existing.to_dict(), 201


class CartItemResource(Resource):
    @jwt_required()
    def patch(self, item_id):
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data or 'quantity' not in data:
            return {'message': 'Missing quantity'}, 400

        quantity = data.get('quantity')
        if not isinstance(quantity, int):
            return {'message': 'Quantity must be an integer'}, 400

        item = CartItem.query.get_or_404(item_id)

        if item.user_id != user_id:
            return {'message': 'Unauthorized'}, 403

        item.quantity = quantity
        db.session.commit()
        return item.to_dict(), 200

    @jwt_required()
    def delete(self, item_id):
        user_id = get_jwt_identity()
        item = CartItem.query.get_or_404(item_id)

        if item.user_id != user_id:
            return {'message': 'Unauthorized'}, 403

        db.session.delete(item)
        db.session.commit()
        return {'message': 'Deleted'}, 204
