from main import db
from datetime import datetime

#  User table
class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String)

#  Admin table
class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(50), nullable=False)

#  Category table
class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    total_items_sold = db.Column(db.Integer, default=0)
    total_revenue = db.Column(db.Float, default=0.0)

#  Product table
class Product(db.Model):
    __tablename__ = 'product'
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)  
    manufacturing_date = db.Column(db.Date, nullable=True)
    expiring_date = db.Column(db.Date, nullable=True)
    product_image = db.Column(db.String)  
    unit = db.Column(db.String(20), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"), nullable=False)
    category = db.relationship('Category', backref='products')
    total_items_sold = db.Column(db.Integer, default=0)
    total_revenue = db.Column(db.Float, default=0.0)



#  Cart table
class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

#  Cart_Items table
class Cart_Items(db.Model):
    __tablename__ = 'cart_items'
    cart_item_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.product_id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cart = db.relationship('Cart', backref='cart_items')
    product = db.relationship('Product')
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))