This is a Django-based web application that allows my organisation to track IT assets and assign them to Inventory users. 
Features include asset registration, assigment to inventory users, status tracking, assignment history, and a user-friendly admin panel with role-based permissions.

You can access the deployed version here:
https://itassetmanager-y617.onrender.com/

Features:
- Secure user authentication and Django admin interface
- Each registered user (not to be confused with the Inventory System users) has a profile for editing personal information and assigning profile pictures
- CRUD operations for Inventory Assets and assigned Inventory Users
- Role-based access:
    - IT Admins – full create/edit/delete access
    - General Admins – view-only permissions
- Responsive frontend with Django bootstrap templates and custom CSS
- Filer Assets based on status
- Sort by function for Assets

Packages:
Python 3,x
Django 5.2.3
PostgreSQL (hosted on render)
HTMLS5/CSS3
Pillow (for iamge handling)
Pip

How to run locally:

git clone https://github.comqueensarahcommanderofdragons/ITAssetManager.git
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver

  - To populate with demo data:
        python manage.py loaddata db.json

This app is hosted on Render using:
- A free web service (for the Django app)
- A managed PostgreSQL database

To create an admin user:
python manage.py createsuperuser
Once inside the admin portal assign 'IT admin' group policy for full CRUD functionality.

Created by Sarah Jobling for for the Software Engineering & DevOps module.

