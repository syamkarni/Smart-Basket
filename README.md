# Smart Basket: Online Grocery Store

Smart Basket is an online grocery store application that allows users to browse, search for products, add them to their shopping cart, and proceed to checkout. Admins can manage product categories and details, view sales statistics, and perform other administrative tasks.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [Accessing the Application](#accessing-the-application)
- [Contributing](#contributing)
- [License](#license)

## Overview

Smart Basket is a Flask-based web application designed to provide users with a convenient and efficient way to shop for groceries online. With features for user authentication, product management, and an intuitive shopping cart system, the application aims to streamline the online grocery shopping experience.

## Features

1. **User Authentication:**
   - Users can register, log in, and manage their profiles.

2. **Product and Category Management:**
   - Admins can add, edit, and delete products and categories.
   - Users can view and filter products by category.

3. **Shopping Cart:**
   - Users can add products to their cart and proceed to checkout.
   - Cart items are associated with user accounts.

4. **User Profile:**
   - Users have a profile page where they can view and edit their personal information.

5. **Search Functionality:**
   - Users can search for products or categories.

6. **Checkout Process:**
   - Users can proceed to checkout, and the system handles the deduction of product quantities and updates revenue based on successful transactions.

7. **Admin Dashboard:**
   - Admins can log in separately.
   - Admins have access to an admin dashboard with category management.

8. **Product Statistics:**
   - Admins can view a summary of sales and revenue statistics for both categories and individual products.

9. **Flash Messages:**
   - Flash messages provide feedback on operations, such as successful profile updates or errors during login.

10. **Logout Functionality:**
    - Both users and admins can log out.

## Installation

To run the Smart Basket application locally, follow these steps:

```bash
# Clone the repository
git clone https://github.com/syamkarni/smart-basket.git

# Navigate to the project directory
cd smart-basket

# Install dependencies
pip install -r requirements.txt



## Usage

To start the development server and run the application, use the following commands:

```bash
# Run the development server
python main.py
```

Visit [http://localhost:8080](http://localhost:8080) in your web browser to access the application.

## API Endpoints

The Smart Basket application provides the following API endpoints:

- **Users:**
  - `GET /api/users/`: Get all users.
  - `GET /api/users/<int:user_id>`: Get a specific user.
  - `POST /user/signup`: Register a new user.
  - `POST /user/login`: User login.
  - `GET /user/logout`: User logout.
  - `GET /user/profile`: Get user profile details.
  - `POST /user/edit_profile`: Edit user profile details.

- **Products:**
  - `GET /api/products/`: Get all products.
  - `GET /api/products/<int:product_id>`: Get details of a specific product.

- **Categories:**
  - `GET /api/categories/`: Get all product categories.
  - `GET /api/categories/<int:category_id>`: Get details of a specific category.

- **Cart:**
  - `GET /api/cart/<int:user_id>`: Get the shopping cart details for a specific user.
  - `POST /api/add_to_cart`: Add a product to the user's cart.
  - `POST /api/remove_from_cart/<int:cart_item_id>`: Remove a product from the user's cart.

- **Checkout:**
  - `POST /api/checkout/<int:cart_id>`: Process the checkout for a specific cart.

- **Admin:**
  - `POST /admin/login`: Admin login.
  - `GET /admin/dashboard`: Admin dashboard with category management.
  - `POST /admin/add_category`: Add a new category.
  - `POST /admin/edit_category/<int:category_id>`: Edit details of a category.
  - `POST /admin/add_product/<int:category_id>`: Add a new product to a category.
  - `POST /admin/edit_product/<int:product_id>`: Edit details of a product.
  - `POST /admin/delete_category/<int:category_id>`: Delete a category and its associated products.
  - `GET /admin/logout`: Admin logout.
  - `GET /admin/summary`: View sales and revenue statistics.

- **Search:**
  - `GET /user/search`: Search for products or categories.



## Technologies Used

- Flask
- Flask-SQLAlchemy
- Flask-RESTful
- HTML
- CSS
- Jinja2
- Bootstrap
- Git
- GitHub
- Vercel (for deployment)
- SQLAlchemy (as an ORM for interacting with the database)
- SQLite (or your preferred database management system)
- Flask-WTF (for handling web forms in Flask)
- Flask-Flash (for displaying flash messages)


## Accessing the Application

The Smart Basket application is deployed and accessible online. You can visit the application using the following link:

[Smart Basket - Online Grocery Store](https://smart-basket.vercel.app/login)

### Admin Credentials

To access the admin dashboard, use the following admin credentials:

- **Username:** admin@admin.com
- **Password:** qwerty

Please note that these credentials are for administrative purposes and provide access to features like category management, product addition, and viewing sales statistics.

### User Access

If you wish to explore the application as a regular user, you can register for a new account or use the following test credentials:

- **Username:** u@gmail.com
- **Password:** as

Feel free to explore the various features and functionalities of the Smart Basket application.



## Contributing


Contributions to Smart Basket are welcome! If you'd like to contribute, please follow the guidelines outlined in the [CONTRIBUTING.md](CONTRIBUTING.md) file.

## License

This project is licensed under the [MIT License](LICENSE).

---

