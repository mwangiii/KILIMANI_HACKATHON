""" This file contains all the routes for the kilimani project api """
import uuid
import os
from flask import Flask, request, jsonify, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User, Posts


@app.route('/')
def home():
    return 'Welcome to the kilimani project api!'

# Utility function to append error messages to a list
def add_error_to_list(errors_list, field, message):
    errors_list.append({
        "field": field,
        "message": message
    })

@app.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    errors = []

    # Validate user input
    if not data.get('username'):
        add_error_to_list(errors, 'username', 'Username is required')
    if not data.get('email'):
        add_error_to_list(errors, 'email', 'Email is required')
    if not data.get('password'):
        add_error_to_list(errors, 'password', 'Password is required')
    if not data.get('firstname'):
        add_error_to_list(errors, 'firstname', 'Firstname is required')
    if not data.get('lastname'):
        add_error_to_list(errors, 'lastname', 'Lastname is required')  
    if not data.get('phone'):
        add_error_to_list(errors, 'phone', 'Phone is required')

    # Return errors if any
    if errors:
        return jsonify({"errors": errors}), 400

    # Create new user
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
        db.session.rollback()
        return jsonify({
            "message": "An error occurred",
            "error": str(e)
        }), 500

@app.route('/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()

    # Retrieve user from database
    existing_user = User.query.filter_by(email=data.get('email')).first()

    # Check if user exists
    if not existing_user:
        return jsonify({"message": "Invalid email"}), 404
    
    # Check if password is correct
    if not check_password_hash(existing_user.password, data.get('password')):
        return jsonify({"message": "Invalid password"}), 401
    
    # Prepare successful response
    response_successful = {
        "status": "success",
        "message": "User logged in successfully",
        "data": {
            "userId": existing_user.userid,
            "username": existing_user.username,
            "email": existing_user.email,
            "firstname": existing_user.firstname,
            "lastname": existing_user.lastname,
            "phone": existing_user.phone
        }
    }

    return jsonify(response_successful), 200

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Posts.query.all()
    posts_data = [{"id": post.postid, "title": post.title, "content": post.content, "author": post.author, "time": post.time} for post in posts]
    return jsonify(posts_data), 200

@app.route('/posts/category/<string:category>', methods=['GET'])
def get_posts_by_category(category):
    posts = Posts.query.filter_by(category=category).all()
    filtered_posts = [{"id": post.postid, "title": post.title, "content": post.content, "author": post.author, "time": post.time} for post in posts]
    return jsonify(filtered_posts), 200

@app.route('/admin/post', methods=['POST'])
def admin_post_issue():
    data = request.get_json()

    new_post = Posts(
        postid=str(uuid.uuid4()),
        title=data['title'],
        content=data['content'],
        author=data.get('author'),  # assuming you have a field for author
        time=datetime.utcnow()
    )
    try:
        db.session.add(new_post)
        db.session.commit()
        return jsonify({"message": "Post created successfully", "post": new_post.postid}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@app.route('/admin/remove_post/<int:post_id>', methods=['DELETE'])
def admin_remove_post(post_id):
    post = Posts.query.filter_by(postid=post_id).first()
    if not post:
        return jsonify({"message": "Post not found"}), 404

    try:
        db.session.delete(post)
        db.session.commit()
        return jsonify({"message": "Post removed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
