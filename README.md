# Business Intelligence & Analytics Dashboard
A Django + DRF product analytics starter with a JavaScript dashboard, CSV import,
and PostgreSQL support (SQLite fallback for quick local setup).

## PROJECT BACKGROUND
This project is a recreated demonstration version of a Business Intelligence application that I previously worked on in a professional environment.
The original application was developed for business purposes. However, due to company privacy policies and confidentiality requirements, the original source code, business data, and confidential information cannot be shared publicly.
Therefore, I independently recreated the application for portfolio and learning purposes.
The recreated version follows the same general concept, architecture, and core functionality as the original application. However, the sample dataset, product information, and certain application content have been modified.
This project demonstrates my understanding of the application's development, backend architecture, database operations, API development, and business analytics.

## Quick start (Windows)
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
py manage.py makemigrations products
py manage.py migrate
py manage.py import_products data/sample_products.csv
py manage.py runserver
Open http://127.0.0.1:8000/
The included CSV is fictional demo data, not live Amazon data.
