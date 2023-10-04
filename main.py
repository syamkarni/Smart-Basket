from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
import os

current_dir = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = 'static/'

app: Flask = Flask(__name__)




app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024


db = SQLAlchemy()
db.init_app(app)
api = Api(app)
app.app_context().push()
app.secret_key=os.urandom(24)

from controller import *

from api import UserAPI, ProductAPI, CategoryAPI, CartAPI


api.add_resource(UserAPI, '/api/users/', '/api/users/<int:user_id>')
api.add_resource(ProductAPI, '/api/products/', '/api/products/<int:product_id>')
api.add_resource(CategoryAPI, '/api/categories/', '/api/categories/<int:category_id>')
api.add_resource(CartAPI, '/api/carts/', '/api/carts/<int:user_id>')

if __name__ == '__main__':

    app.run(host='0.0.0.0', port=8080, debug=True)