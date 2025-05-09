# MyShop Django E-commerce Application

## Project Overview
MyShop is a Django-based web application that sells laptops using an open dataset. Core features include product listing, detailed view, search, shopping cart, quick purchase, order history, and an admin dashboard.

## Features
- Product list with search and pagination  
- Product detail with image carousel  
- Add to Cart & Buy Now flows  
- Shopping cart with edit and delete options  
- Checkout process for selected items  
- User authentication (admin, user, guest)  
- Order history for users  
- Admin dashboard with charts (monthly orders, top products)  
- Custom 404/500 error pages  
- Management command to bulk import products  
- Unit tests covering import, cart, checkout  

## Tech Stack
- **Backend:** Python, Django  
- **Database:** SQLite  
- **Frontend:** HTML, CSS, Django Templates, JavaScript (slider & Chart.js)  
- **Deployment:** PythonAnywhere  
- **Testing:** Django Test framework, Coverage  

## Setup & Run Locally
1. **Clone repository**  

   git clone https://github.com/Yeyaomon/myshop.git
   cd myshop

2.  Create & activate venv

    python3.10 -m venv venv
    source venv/bin/activate

3.  Install dependencies

    pip install -r requirements.txt

4.  Migrate & import data

    python manage.py migrate
    python manage.py import_products

5.  Run development server

    python manage.py runserver by 0.0.0.0.8000

## Running Tests
    coverage run --source='.' manage.py test
    coverage report

## Deployment (PythonAnywhere)
1.  Clone repo on PythonAnywhere

    git clone https://github.com/Yeyaomon/myshop.git
    cd myshop

2.  Setup virtualenv & install dependencies

    python3.10 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

3.  Migrate & collect static files

    python manage.py migrate
    python manage.py collectstatic --noinput

4.  Web app configuration

    Source code: /home/yourusername/myshop
    Virtualenv: /home/yourusername/myshop/venv
    Static files: map URL /static/ to /home/yourusername/myshop/staticfiles

5.  Reload the web app

##  Demo Accounts
    User: andywong/AndyWong
    Admin: Wnm19980909

##  Project Structure
    myshop/
    ├── products/         # Product app (models, views, templates)
    ├── orders/           # Order & cart app
    ├── static/           # Project-level static files
    ├── templates/        # Project-level templates
    ├── manage.py
    ├── report.pdf        # One-page design & deployment report
    └── README.md

##  Data Source
    Dataset: eBay PC Laptops and Netbooks (5,000 items)
    Imported via the import_products management command.

##  Project Report
    See report.pdf for a one-page summary of design, ER diagram, architecture, and screenshots.