import sqlite3
from datetime import datetime

def create_database():
    conn = sqlite3.connect('database.sqlite3')
    c = conn.cursor()

    c.execute('CREATE TABLE user (user_id INTEGER PRIMARY KEY, username VARCHAR(50) NOT NULL, email VARCHAR(100) NOT NULL, phone VARCHAR NOT NULL, password VARCHAR(50) NOT NULL, address VARCHAR)')
    c.execute('CREATE TABLE admin (admin_id INTEGER PRIMARY KEY, username VARCHAR(50) NOT NULL, email VARCHAR(100) NOT NULL, password VARCHAR(50) NOT NULL)')
    c.execute('CREATE TABLE category (category_id INTEGER PRIMARY KEY, category_name VARCHAR(100) NOT NULL)')
    c.execute('CREATE TABLE product (product_id INTEGER PRIMARY KEY, product_name VARCHAR(100) NOT NULL, price FLOAT NOT NULL, quantity INTEGER NOT NULL, manufacture_date VARCHAR, product_image VARCHAR, unit VARCHAR(20) NOT NULL, category_id INTEGER NOT NULL REFERENCES category(category_id))')
    c.execute('CREATE TABLE cart (cart_id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, total_amount FLOAT NOT NULL)')
    c.execute('CREATE TABLE cart_items (cart_item_id INTEGER PRIMARY KEY, cart_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL)')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
