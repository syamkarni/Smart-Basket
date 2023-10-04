from flask import render_template, request, redirect, url_for, session, flash
from main import app, db
from model import *
from datetime import datetime

@app.route('/', methods=['GET'])
def home():

    user_id = session.get('user_id')
    if user_id is not None:
        return redirect('/user/dashboard')
    else:
        return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email, password=password).first()
        if user:
            session['user_id'] = user.user_id
            return redirect('/user/dashboard')
        else:
            error_message = "Invalid email or password. Please try again."
            return render_template('user_signin.html', error_message=error_message)

    return render_template('user_signin.html', error_message="")


@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        address = request.form['address']
        gender = request.form['gender']

        if User.query.filter_by(email=email).first():
            error_message = "Email already registered. Please use a different email."
            return render_template('signup.html', error_message=error_message)
        new_user = User(username=name, email=email, phone=phone, password=password, address=address)
        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.user_id

        return redirect('/user/dashboard')
    return render_template('signup.html', error_message="")

@app.route('/user/dashboard', methods=['GET'])
def user_dashboard():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect('/login')
    categories = Category.query.all()

    return render_template('user_dashboard.html', categories=categories)



@app.route('/user/cart/<int:user_id>', methods=['GET'])
def user_cart(user_id):
    logged_in_user_id = session.get('user_id')
    if logged_in_user_id is None or logged_in_user_id != user_id:
        return redirect('/login')
    
    cart = Cart.query.filter_by(user_id=user_id).first()
    cart_items = Cart_Items.query.filter_by(cart_id=cart.cart_id).all()

    cart_items_with_product_info = []

    grand_total = 0

    for cart_item in cart_items:
        product = Product.query.filter_by(product_id=cart_item.product_id).first()

        if product:
            total = cart_item.quantity * product.price
            grand_total += total


            cart_item_info = {
                'cart_item_id': cart_item.cart_item_id,
                'cart_id': cart_item.cart_id,
                'product_name': product.product_name,
                'quantity': cart_item.quantity,
                'price': product.price,
                'total': total,
            }

            cart_items_with_product_info.append(cart_item_info)

    return render_template('cart.html', cart_items=cart_items_with_product_info, grand_total=grand_total)





@app.route('/user/logout', methods=['GET'])
def user_logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))  






@app.route('/user/add_to_cart', methods=['POST'])
def add_to_cart():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('user_login'))

    product_id = int(request.form['product_id'])

    product = Product.query.get(product_id)
    if not product or product.quantity == 0:
        return redirect(url_for('user_dashboard'))


    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id, total_amount=0)
        db.session.add(cart)

    cart_item = Cart_Items.query.filter_by(cart_id=cart.cart_id, product_id=product_id).first()

    if cart_item:

        cart_item.quantity += 1
    else:

        cart_item = Cart_Items(cart_id=cart.cart_id, product_id=product_id, quantity=1)
        db.session.add(cart_item)


    cart.total_amount = calculate_total_amount(cart.cart_id)


    db.session.commit()


    return redirect(url_for('user_dashboard'))

def calculate_total_amount(cart_id):

    cart_items = Cart_Items.query.filter_by(cart_id=cart_id).all()


    total_amount = 0


    for cart_item in cart_items:
        total_amount += cart_item.product.price * cart_item.quantity

    return total_amount

@app.route('/remove_from_cart/<int:cart_item_id>', methods=['GET'])
def remove_from_cart(cart_item_id):

    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('user_login'))


    cart_item = Cart_Items.query.get(cart_item_id)

    if cart_item:

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:

            db.session.delete(cart_item)
        db.session.commit()
    

    return redirect(url_for('user_cart', user_id=user_id))

@app.route('/user/profile', methods=['GET'])
def user_profile():

    user_id = session.get('user_id')
    if user_id is None:

        return redirect(url_for('user_login'))


    user = User.query.filter_by(user_id=user_id).first()

    if user:

        return render_template('profile.html', user=user)
    else:
        return "User not found"
    



@app.route('/user/edit_profile', methods=['GET', 'POST'])
def edit_profile():

    if 'user_id' not in session:
        return redirect(url_for('user_login'))  


    user_id = session['user_id']


    user = User.query.get(user_id)

    if request.method == 'POST':

        user.username = request.form['username']
        user.email = request.form['email']
        user.phone = request.form['phone']
        user.address = request.form['address']

        db.session.commit()

        flash('Profile updated successfully', 'success')
        return redirect(url_for('user_profile'))  


    return render_template('edit_profile.html', user=user)

@app.route('/user/search', methods=['GET'])
def user_search():

    query = request.args.get('query')
    search_type = request.args.get('search_type')


    if search_type == 'category':


        categories = Category.query.filter(Category.category_name.ilike(f"%{query}%")).all()



        return render_template('search_results.html', results=categories)

    elif search_type == 'product':

        products = Product.query.filter(Product.product_name.ilike(f"%{query}%")).all()

        return render_template('search_results.html', results=products)


    else:
        return "Invalid search type"
    




@app.route('/user/checkout/<int:cart_id>', methods=['POST'])
def user_checkout(cart_id):

    print('checkout is being processed....')

    user_id = session.get('user_id')
    cart = Cart.query.filter_by(user_id=user_id).first()

    if not cart:
        return "Your cart is empty."

    cart_items = Cart_Items.query.filter_by(cart_id=cart.cart_id).all()

    for cart_item in cart_items:
        product = Product.query.get(cart_item.product_id)
        category = Category.query.get(product.category_id)

        if product and category:
            if product.quantity >= cart_item.quantity:
                product.quantity -= cart_item.quantity
                product.total_items_sold += cart_item.quantity
                product.total_revenue = (product.total_revenue or 0.0) + (cart_item.quantity * product.price)

                category.total_items_sold += cart_item.quantity
                category.total_revenue = (category.total_revenue or 0.0) + (cart_item.quantity * product.price)

                db.session.delete(cart_item)
            else:
                return "Not enough quantity available for some products in your cart."

    db.session.commit()


    return redirect(url_for('user_dashboard'))





#Admin



@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        admin = Admin.query.filter_by(email=email, password=password).first()
        print(admin)
        if admin:
            print(111)
            session['admin_id'] = admin.admin_id

            return redirect('/admin/dashboard')
        else:
            error_message = "Invalid email or password. Please try again."
            return render_template('admin_signin.html', error_message=error_message)

    return render_template('admin_signin.html', error_message="")



@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():

    admin_id = session.get('admin_id')
    if admin_id is None:
        return redirect('/admin/login')
    categories = Category.query.all()

    return render_template('admin_dashboard.html', categories=categories)




@app.route('/admin/add_category', methods=['GET', 'POST'])
def add_category():
    admin_id = session.get('admin_id')
    if admin_id is None:
        return redirect('/admin/login')

    if request.method == 'POST':
        category_name = request.form['category_name']

        new_category = Category(category_name=category_name)
        db.session.add(new_category)
        db.session.commit()

        return redirect('/admin/dashboard')

    return render_template('add_category.html')


@app.route('/admin/edit_category/<int:category_id>', methods=['GET', 'POST'])
def edit_category(category_id):
    category = Category.query.get(category_id)

    if request.method == 'POST':
        new_category_name = request.form.get('new_category_name')
        
        if new_category_name:
            category.category_name = new_category_name
            db.session.commit()
        else:
            flash('Category name is required', 'error')
        for product in category.products:
            product_name = request.form.get(f'product_name_{product.product_id}')
            product_price = request.form.get(f'product_price_{product.product_id}')
            product_quantity = request.form.get(f'product_quantity_{product.product_id}')
            product_manufacturing_date = request.form.get(f'product_manufacturing_date_{product.product_id}')
            product_expiring_date = request.form.get(f'product_expiring_date_{product.product_id}') 
            

            if product_name and product_price and product_quantity:
                product.product_name = product_name
                product.price = product_price
                product.quantity = product_quantity
                product.manufacturing_date = product_manufacturing_date
                product.expiring_date = product_expiring_date
                db.session.commit()
            else:
                flash(f'Invalid data for product ID {product.product_id}', 'error')

        flash('Category and product details updated successfully', 'success')
        return redirect(url_for('admin_dashboard'))

    return render_template('edit_category.html', category=category)








# # Add product route
# @app.route('/admin/add_product/<int:category_id>', methods=['GET', 'POST'])
# def add_product(category_id):
#     # Check if the admin is logged in by verifying the admin_id in the session
#     admin_id = session.get('admin_id')
#     if admin_id is None:
#         # If admin is not logged in, redirect to the login page
#         return redirect('/admin/login')

#     if request.method == 'POST':
#         # Get the form data from the POST request
#         category_id = request.form['category_id']
#         product_name = request.form['product_name']
#         unit = request.form['unit']
#         quantity = request.form['quantity']  # Remove rate_unit from form data
#         price = request.form['price']  # Retrieve the price from the form data

#         # Create a new product object and add it to the database
#         new_product = Product(product_name=product_name, unit=unit, quantity=quantity, price=price, category_id=category_id)
#         db.session.add(new_product)
#         db.session.commit()

#         # Redirect to the category products page after adding the product
#         return redirect(url_for('cat_products', category_id=category_id))

#     # If the request method is GET, render the add_product template
#     # category_id = request.args.get('category_id')  # Get the category_id from the query parameters
#     return render_template('add_product.html', category_id=category_id)   # Pass the category_id to the template

@app.route('/admin/add_product/<int:category_id>', methods=['GET', 'POST'])
def add_product(category_id):

    admin_id = session.get('admin_id')
    if admin_id is None:

        return redirect('/admin/login')

    if request.method == 'POST':

        product_name = request.form['product_name']
        unit = request.form['unit']
        quantity = request.form['quantity']  
        price = request.form['price']  
        manufacturing_date = request.form['manufacturing_date']  
        expiring_date = request.form['expiring_date']  

        manufacturing_date = datetime.strptime(manufacturing_date, '%Y-%m-%d')
        expiring_date = datetime.strptime(expiring_date, '%Y-%m-%d')

        new_product = Product(
            product_name=product_name, unit=unit, quantity=quantity, price=price,
            category_id=category_id, manufacturing_date=manufacturing_date, expiring_date=expiring_date
        )
        db.session.add(new_product)
        db.session.commit()

        return redirect('/admin/dashboard')


    return render_template('add_product.html', category_id=category_id) 




@app.route('/admin/delete_category/<int:category_id>', methods=['POST'])
def delete_category(category_id):

    admin_id = session.get('admin_id')
    if admin_id is None:
        return redirect('/admin/login')

    category = Category.query.get(category_id)
    if not category:
        return "Category not found."

    try:
        products = Product.query.filter_by(category_id=category_id).all()
        for product in products:
            db.session.delete(product)

        db.session.delete(category)
        db.session.commit()

        return redirect('/admin/dashboard')
    except Exception as e:

        db.session.rollback() 
        return f"An error occurred: {str(e)}"



@app.route('/admin/logout', methods=['GET'])
def admin_logout():
    session.pop('admin_id', None)

    return redirect(url_for('admin_login'))



@app.route('/admin/summary', methods=['GET'])
def admin_summary():

    categories = Category.query.all()
    products = Product.query.all()


    category_statistics = []
    product_statistics = []

    for category in categories:
        total_items_sold = 0
        total_revenue = 0

        for product in category.products:
            total_items_sold += product.total_items_sold
            total_revenue += product.total_revenue

        category_statistics.append({
            'category_name': category.category_name,
            'total_items_sold': total_items_sold,
            'total_revenue': total_revenue
        })

    for product in products:
        product_statistics.append({
            'product_name': product.product_name,
            'total_items_sold': product.total_items_sold,
            'total_revenue': product.total_revenue
        })


    return render_template('admin_summary.html', category_statistics=category_statistics, product_statistics=product_statistics)


