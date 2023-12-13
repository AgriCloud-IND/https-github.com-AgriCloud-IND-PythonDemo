"""
Routes and views for the flask application.
"""

from datetime import datetime
import email
from flask import render_template, request
from FlaskWebProject1 import app




@app.route('/')

@app.route('/home')


def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
@app.route('/Registration')
def Registration():
    """Renders the home page."""
    return render_template(
        'Registration.html',
        title='Registration Page',
        year=datetime.now().year,
    )

import requests;
import pyodbc 

# Replace these values with your own database information
server = 'MMC\SQLEXPRESS'  # If it's a local server, you can use '(local)' or 'localhost'
database = 'MMC'
username = 'sa'
password = 'sa'

# Create a connection string
#connection_stringSA = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

# Create a connection string for Windows Authentication
connection_stringNT = f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'


def get_records(page, page_size):
    
    offset = (page - 1) * page_size
    query = f"SELECT * FROM Users ORDER BY userid OFFSET {offset} ROWS FETCH NEXT {page_size} ROWS ONLY"

    connection = pyodbc.connect(connection_stringNT)
    cursor = connection.cursor()

    try:
        cursor.execute(query)
        records = cursor.fetchall()
        return records
    finally:
        cursor.close()
        connection.close()


@app.route('/register',methods=['GET', 'POST'])
def register():
     
# Establish a connection
    
    connection = pyodbc.connect(connection_stringNT)
    
    name = request.form.get("name",'')
    email = request.form.get("email",'')

    # Set the number of records per page
    page_size = 10
     
    print(request.args)
    page = int(request.args.get('page',1))
        # Get records for the specified page

    if(request.method =='POST'):
        try:
            cursor = connection.cursor()
            print("INSERT INTO Users (name,email) VALUES ('" + name + "','" + email +"')")
            cursor.execute("INSERT INTO Users (name, email) VALUES (?, ?)", (name, email))
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

    records = get_records(page, page_size)
    
    return render_template(
        'Registration.html',
        records=records, 
        page=page,
        title='Registration Page',
        message = "your Name:" + name + " Email:" + email, 
        year=datetime.now().year,
    )    