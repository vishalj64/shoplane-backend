# shoplane backend

### Setup

- git clone https://github.com/vishalj64/shoplane-backend
- cd django-ecommerce
- pip install -r requirements.txt
- python manage.py migrate
- python manage.py runserver

### Features Listing

- Admin adds the category and products
- Browses all the products and categories
- User can signup and login
- User can add review for the product
- Search all the products using filters
- Add products in cart
- User can checkout product

### Models and Fields Construction

1. Categories
    - name
    - slug
    - image
    - description
    - featured
    - active

2. Products
    - name
    - slug
    - image
    - brand
    - shipping
    - description
    - price
    - category
    - featured
    - active
    - created
    - modified

3. Review
    - product
    - user
    - rate
    - review
    - created

4. User
    - username
    - email
    - password
