#!/usr/bin/env python3
from flask import Flask, request, redirect, url_for, render_template, session, jsonify
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.secret_key = 'secret_key'



UPLOAD_FOLDER =  'static/profile_photos'


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/auth/register', methods=['POST'])
def register():
        # firstName = request.form.get('firstName')
        # lastName = request.form.get('lastName')
        # phone = request.form.get('phone')
        # password = request.form.get('password')
        # username = request.form.get('username')
        # profile_photo = request.files.get('profile_photo')

        # # form validation
        # if not phone or not password or not username:
        #     return jsonify({'error': "Phone, password, and name are required"}), 400

        # # hash password
        # hashed_password = generate_password_hash(password)

        # if profile_photo:
        # 
    data = request.json 
    errors_list = []

    if not data:
        return jsonify({'error': "Invalid data"}), 400
    if not firstname or not lastname or not phone or not password or not username:
        return jsonify({'error': "First name, last name, phone, password, and username are required"}), 400
    if 
    new_user = User(
        userId = uuid.uuid4()
        firstName = firstname,
        lastName = lastname,  )