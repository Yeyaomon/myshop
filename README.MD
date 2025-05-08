# MyShop

## Project Overview
MyShop is a Django-based e-commerce demo application that sells laptops and PCs. It uses an open dataset of computer products to populate a catalog of ~5,000 items. Users can browse products, add items to a shopping cart, checkout selected items, and view their order history. Administrators get a dashboard with sales charts.

## Features
- Product Catalog: searchable, paginated list and detail pages  
- Shopping Cart: add, edit, delete, selective checkout  
- “Buy Now”: one-click purchase that skips the cart  
- Order History: view past orders and details  
- Admin Dashboard: Chart.js visualizations of monthly order trends and top 5 products by revenue  
- Custom Error Pages: friendly 404 and 500 templates  
- Unit Tests: automated tests covering core workflows (>80% coverage)  

## Tech Stack
- Backend: Python 3.10, Django 3.2  
- Database: SQLite (development), configurable for PostgreSQL in production  
- Frontend: Django Templates, CSS, minimal JavaScript (Chart.js, vanilla JS)  
- Deployment: PythonAnywhere or Heroku  
- Testing: Django Test Framework  

## Project Structure
myshop/
├── data/ # dataset csv.file
├── myshop/ # project settings & URL configuration
├── orders/ # cart & order app (models, views, templates)
├── products/ # product app (models, views, templates)
├── scripts/ # data generater 
├── static/ # CSS, JS, images
├── templates/ # shared templates (base, 404, 500)
├── venv # virtual environment simulate
├── db.sqlite3 #database
├── manage.py #manage tool
├── README.md # this file
├── requirements.txt # Python dependencies
└── report.pdf # one-page design & implementation summary


## Data Source
- EbayPcLaptopsAndNetbooksClean.csv: ~5,000 laptop records (brand, model, specs, price, stock)  
- Loaded via custom management command:
        python manage.py import_products

## Setup & Run Locally

1. Clone the repository  
        git clone <your-repo-url>
        cd myshop

2. Create & activate a virtual environment  
        python3.10 -m venv venv
        source venv/bin/activate
        pip install -r requirements.txt

3. Apply migrations & import product data 
        python manage.py migrate
        python manage.py import_products 

4. Collect static files (for production)  
        python manage.py collectstatic --noinput

5. Start the development server  
        python manage.py runserver
        Open your browser at http://localhost:8000

## Running Tests
        python manage.py test

## Deployment

### PythonAnywhere

1. Push your code to GitHub.  

2. Create a new web app (Django + Python 3.10).  

3. In a Bash console:
        cd ~
        git clone <your-repo-url>
        cd myshop
        mkvirtualenv venv --python=python3.10
        pip install -r requirements.txt
        python manage.py migrate
        python manage.py import_products
        python manage.py collectstatic --noinput

4. Configure settings.py for production:
        ```python
        DEBUG = False
        ALLOWED_HOSTS = ['<your-username>.pythonanywhere.com']
        handler404 = 'django.views.defaults.page_not_found'
        handler500 = 'django.views.defaults.server_error'

5.Reload the web app and verify functionality.

### Heroku (Alternative)

1.Install Heroku CLI and log in.

2.Create a new Heroku app:
    heroku create myshop-demo
    git push heroku main
    heroku run python manage.py migrate
    heroku run python manage.py import_products

3.Configure static assets (e.g., AWS S3) or disable collectstatic.

4.Open with:
    heroku open

### Demo Accounts
User:AndyWang

Username: AndyWang

Password: Wnm19980909

Admin:AndyWang

Username: Wnm19980909

Password: Wnm19980909

### Project Report
See report.pdf in the project root for ER diagrams, architecture sketches, key screenshots, and a summary of design decisions.

### Future Improvements
    Integrate real payment gateway (Stripe, PayPal)

    Add user profiles with addresses and wishlists

    Product recommendations and ratings

    Internationalization (i18n)

    Move to PostgreSQL and add caching (Redis)