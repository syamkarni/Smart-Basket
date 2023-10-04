from flask_restful import Resource
from flask import request
from main import db
from model import *

class UserAPI(Resource):
    def get(self, user_id=None):
        if user_id:
            user = User.query.filter_by(user_id=user_id).first()
            if user:
                return {
                    'user_id': user.user_id,
                    'username': user.username,
                    'email': user.email,
                    'phone': user.phone,
                    'address': user.address
                }, 200
            else:
                return {'message': 'User not found'}, 404



    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        address = data.get('address')

        # check if user with email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return {'message': 'User with email already exists'}, 409

        # create new user
        user = User(username=username, email=email, phone=phone, password=password, address=address)
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201

    def put(self, user_id):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        phone = data.get('phone')
        password = data.get('password')
        address = data.get('address')

        # check if user exists
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            user.username = username
            user.email = email
            user.phone = phone
            user.password = password
            user.address = address
            db.session.commit()
            return {'message': 'User updated successfully'}, 201
        else:
            return {'message': 'User not found'}, 404

    def delete(self, user_id):
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'User not found'}, 404
    



# Product API for CRUD

class ProductAPI(Resource):
    def get(self, product_id=None):
        if product_id:
            product = Product.query.filter_by(product_id=product_id).first()
            if product:
                return {
                    'product_id': product.product_id,
                    'product_name': product.product_name,
                    'price': product.price,
                    'quantity': product.quantity,
                    'manufacture_date': product.manufacture_date,
                    'product_image': product.product_image,
                    'category_id': product.category_id
                }, 200
            else:
                return {'message': 'Product not found'}, 404

    def post(self):
        data = request.get_json()
        product_name = data.get('product_name')
        price = data.get('price')
        quantity = data.get('quantity')
        manufacture_date = data.get('manufacture_date')
        product_image = data.get('product_image')
        category_id = data.get('category_id')

        # create new product
        product = Product(
            product_name=product_name,
            price=price,
            quantity=quantity,
            manufacture_date=manufacture_date,
            product_image=product_image,
            category_id=category_id
        )
        db.session.add(product)
        db.session.commit()

        return {'message': 'Product created successfully'}, 201

    def put(self, product_id):
        data = request.get_json()
        product_name = data.get('product_name')
        price = data.get('price')
        quantity = data.get('quantity')
        manufacture_date = data.get('manufacture_date')
        product_image = data.get('product_image')
        category_id = data.get('category_id')

        # check if product exists
        product = Product.query.filter_by(product_id=product_id).first()
        if product:
            product.product_name = product_name
            product.price = price
            product.quantity = quantity
            product.manufacture_date = manufacture_date
            product.product_image = product_image
            product.category_id = category_id
            db.session.commit()
            return {'message': 'Product updated successfully'}, 201
        else:
            return {'message': 'Product not found'}, 404

    def delete(self, product_id):
        product = Product.query.filter_by(product_id=product_id).first()
        if product:
            db.session.delete(product)
            db.session.commit()
            return {'message': 'Product deleted successfully'}, 200
        else:
            return {'message': 'Product not found'}, 404




#Sections/ Categories API for CRUD

class CategoryAPI(Resource):
    def get(self, category_id=None):
        if category_id:
            category = Category.query.filter_by(category_id=category_id).first()
            if category:
                return {
                    'category_id': category.category_id,
                    'category_name': category.category_name,
                }, 200
            else:
                return {'message': 'Category not found'}, 404

    def post(self):
        data = request.get_json()
        category_name = data.get('category_name')

        # check if category with name already exists
        existing_category = Category.query.filter_by(category_name=category_name).first()
        if existing_category:
            return {'message': 'Category with name already exists'}, 409

        # create new category
        category = Category(category_name=category_name)
        db.session.add(category)
        db.session.commit()

        return {'message': 'Category created successfully'}, 201

    def put(self, category_id):
        data = request.get_json()
        category_name = data.get('category_name')

        # check if category exists
        category = Category.query.filter_by(category_id=category_id).first()
        if category:
            category.category_name = category_name
            db.session.commit()
            return {'message': 'Category updated successfully'}, 201
        else:
            return {'message': 'Category not found'}, 404

    def delete(self, category_id):
        category = Category.query.filter_by(category_id=category_id).first()
        if category:
            db.session.delete(category)
            db.session.commit()
            return {'message': 'Category deleted successfully'}, 200
        else:
            return {'message': 'Category not found'}, 404








# Cart API for CRUD
class CartAPI(Resource):
    def get(self, user_id=None):
        if user_id:
            cart = Cart.query.filter_by(user_id=user_id).first()
            if cart:
                cart_items = Cart_Items.query.filter_by(cart_id=cart.cart_id).all()
                items = []
                for cart_item in cart_items:
                    product = Product.query.filter_by(product_id=cart_item.product_id).first()
                    items.append({
                        'product_id': product.product_id,
                        'product_name': product.product_name,
                        'price': product.price,
                        'quantity': cart_item.quantity
                    })

                return {
                    'cart_id': cart.cart_id,
                    'user_id': cart.user_id,
                    'items': items,
                    'total_amount': cart.total_amount
                }, 200
            else:
                return {'message': 'Cart not found'}, 404

    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')

        # check if cart for user already exists
        existing_cart = Cart.query.filter_by(user_id=user_id).first()
        if existing_cart:
            return {'message': 'Cart for user already exists'}, 409

        # create new cart
        cart = Cart(user_id=user_id, total_amount=0)
        db.session.add(cart)
        db.session.commit()

        return {'message': 'Cart created successfully'}, 201

    def put(self, user_id):
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity')

        # check if cart for user exists
        cart = Cart.query.filter_by(user_id=user_id).first()
        if cart:
            # check if the product is already in the cart
            cart_item = Cart_Items.query.filter_by(cart_id=cart.cart_id, product_id=product_id).first()

            if cart_item:
                # update the quantity of the existing product in the cart
                cart_item.quantity = quantity
            else:
                # create a new cart item
                cart_item = Cart_Items(cart_id=cart.cart_id, product_id=product_id, quantity=quantity)
                db.session.add(cart_item)

            # update the total amount in the cart
            cart.total_amount = self.calculate_total_amount(cart.cart_id)
            db.session.commit()
            return {'message': 'Cart updated successfully'}, 201
        else:
            return {'message': 'Cart not found'}, 404

    def delete(self, user_id):
        cart = Cart.query.filter_by(user_id=user_id).first()
        if cart:
            # delete all cart items associated with the cart
            cart_items = Cart_Items.query.filter_by(cart_id=cart.cart_id).all()
            for cart_item in cart_items:
                db.session.delete(cart_item)

            # delete the cart
            db.session.delete(cart)
            db.session.commit()
            return {'message': 'Cart deleted successfully'}, 200
        else:
            return {'message': 'Cart not found'}, 404

    def calculate_total_amount(self, cart_id):
        cart_items = Cart_Items.query.filter_by(cart_id=cart_id).all()
        total_amount = 0
        for cart_item in cart_items:
            product = Product.query.filter_by(product_id=cart_item.product_id).first()
            total_amount += (product.price * cart_item.quantity)
        return total_amount
