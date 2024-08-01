""" This file contains all the routes for the kilimani project api """
import uuid
from app.models import User 
from app import db
from app import app
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.secret_key = 'secret_key'



UPLOAD_FOLDER =  'static/profile_photos'


@app.route('/')
def home():
    return 'Welcome to the kilimani project api!'

# create a function to append error list with parameters error field and error message
def add_error_to_list(errors_list, field, message):
    errors_list.append({
        "field": field,
        "message": message
    })


@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = []
    # check if user provided everythin
    if data.get('username') is None:
        add_error_to_list(errors, 'username', 'username is required')
    if data.get('email') is None:
        add_error_to_list(errors, 'email', 'email is required')
    if data.get('password') is None:
        add_error_to_list(errors, 'password', 'password is required')
    if data.get('firstname') is None:
        add_error_to_list(errors, 'firstname', 'firstname is required')
    if data.get('lastname') is None:
        add_error_to_list(errors, 'lastname', 'lastname is required')  
    if data.get('phone') is None:
        add_error_to_list(errors, 'phone', 'phone is required')


    new_user = User(
        userid=str(uuid.uuid4()),
        username=data.get('username'),
        email=data.get('email'),
        password=generate_password_hash(data.get('password')),
        firstname=data.get('firstname'),
        lastname=data.get('lastname'),
        phone=data.get('phone')
    )
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({
            "message": "User created successfully",
            "user": {
                "userid": new_user.userid,
                "username": new_user.username,
                "email": new_user.email,
                "firstname": new_user.firstname,
                "lastname": new_user.lastname,
                "phone": new_user.phone
            }
        }), 201
    except Exception as e:
        return jsonify({
            "message": "An error occurred",
            "error": str(e)
        }), 500

    return