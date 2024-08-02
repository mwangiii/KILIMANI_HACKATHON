""" This file contains all the routes for the kilimani project api """
import uuid
import os
from flask import Flask, request, jsonify, redirect, url_for, render_template, session
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from app.models import User, Posts, Comments, Polls,Events, HighAlertAreas
from datetime import datetime


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
    """ Register a new user """
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
        phone=data.get('phone'),
        roles=data.get('roles', 'user')
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
                "phone": new_user.phone,
                "roles": new_user.roles
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
    """ Log in a user """
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


@app.route('/user/posts', methods=['GET'])
def get_posts():
    """ Get all posts """
    posts = Posts.query.all()
    posts_data = []
    for post in posts:
        posts_data.append({
            "postid": post.postid,
            "title": post.title,
            "content": post.content,
            "author": post.author,
            "time": post.time
        })
    return jsonify(posts_data), 200

@app.route('/user/<user_id>/comment', methods=['POST'])
def user_post_comment(user_id):
    """ Post a comment """
    data = request.get_json()
    try:
        user = User.query.filter_by(userid=user_id).first()
        if not user:
            return jsonify({"message": "User not found"}), 404
        
        new_comment = Comments(
            commentid=str(uuid.uuid4()),
            content=data['content'],
            author=user.userid,  # Use the user's userid for the author field
            time=datetime.utcnow()
        )
        
        db.session.add(new_comment)
        db.session.commit()
        
        return jsonify({
            "message": "Comment created successfully",
            "comment": new_comment.commentid,
            "data": {
                "commentid": new_comment.commentid,
                "content": new_comment.content,
                "author": user.firstname + ' ' + user.lastname,  # For display purposes
                "time": new_comment.time,
                "user_name": user.firstname + ' ' + user.lastname  # Include user's name in the response
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500

@app.route('/user/comments', methods=['GET'])
def get_comments():
    """ Get all comments """
    comments = Comments.query.all()
    comments_data = []
    for comment in comments:
        comments_data.append({
            "commentid": comment.commentid,
            "content": comment.content,
            "author": comment.author,
            "time": comment.time
        })
    return jsonify(comments_data), 200

@app.route('/admin/remove_comment/<comment_id>', methods=['DELETE'])
def admin_remove_comment(comment_id):
    """" Admin removes a comment """
    comment = Comments.query.filter_by(commentid=comment_id).first()
    if not comment:
        return jsonify({"message": "Comment not found"}), 404

    try:
        db.session.delete(comment)
        db.session.commit()
        return jsonify({"message": "Comment removed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    


# get all comments by commentId
@app.route('/user/comments/<comment_id>', methods=['GET'])
def get_comment_by_id(comment_id):
    """ Get all comments by commentId """
    comment = Comments.query.filter_by(commentid=comment_id).first()
    if not comment:
        return jsonify({"message": "Comment not found"}), 404
    return jsonify({
        "commentid": comment.commentid,
        "content": comment.content,
        "author": comment.author,
        "post": comment.postid,
        "time": comment.time
    }), 200
         

@app.route('/admin/<admin_id>/post', methods=['POST'])
def admin_post_issue(admin_id):
    """ Admin posts an issue """
    data = request.get_json()
    
    # Fetch admin details from the User table
    try:
        admin = User.query.filter_by(userid=admin_id).first()
        if not admin:
            return jsonify({"message": "Admin not found"}), 404
        
        # Create a new post
        new_post = Posts(
            postid=str(uuid.uuid4()),
            title=data['title'],
            content=data['content'],
            author=admin.userid,  # Use the admin's userid for the author field
            time=datetime.utcnow()
        )
        
        db.session.add(new_post)
        db.session.commit()
        
        return jsonify({
            "message": "Post created successfully",
            "post": new_post.postid,
            "data": {
                "postid": new_post.postid,
                "title": new_post.title,
                "content": new_post.content,
                "author": admin.firstname + ' ' + admin.lastname,  # For display purposes
                "time": new_post.time,
                "admin_name": admin.firstname + ' ' + admin.lastname  # Include admin's name in the response
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500


@app.route('/admin/update_post/<post_id>', methods=['PUT'])
def admin_update_post(post_id):
    """ Admin updates a post """
    data = request.get_json()
    post = Posts.query.filter_by(postid=post_id).first()
    if not post:
        return jsonify({"message": "Post not found"}), 404

    try:
        post.title = data.get('title', post.title)
        post.content = data.get('content', post.content)
        db.session.commit()
        return jsonify({
            "message": "Post updated successfully",
            "post": {
                "postid": post.postid,
                "title": post.title,
                "content": post.content,
                "author": post.author,
                "time": post.time
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    

@app.route('/admin/remove_post/<post_id>', methods=['DELETE'])
def admin_remove_post(post_id):
    """ Admin removes a post """
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


@app.route('/user/<userid>/vote', methods=['POST'])
def vote(post_id):
    """User votes on a post"""
    post = Posts.query.filter_by(postid=post_id).first()
    if not post:
        return jsonify({"message": "Post not found"}), 404

    try:
        post.number_of_votes += 1
        db.session.commit()
        return jsonify({
            "message": "Vote received successfully",
            "post": {
                "postid": post.postid,
                "title": post.title,
                "content": post.content,
                "author": post.author,
                "time": post.time,
                "number_of_votes": post.number_of_votes
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
@app.route('/user/polls', methods=['GET'])
def get_polls():
    """ Get all polls """
    polls = Polls.query.all()
    polls_data = []
    for poll in polls:
        polls_data.append({
            "pollid": poll.pollid,
            "title": poll.title,
            "number_of_votes": poll.number_of_votes
        })
    return jsonify(polls_data), 200


@app.route('/admin/create_event', methods=['POST'])
def create_event():
    """Admin creates events"""
    data = request.get_json()
    new_event = Events(
        eventid=str(uuid.uuid4()),
        title=data['title'],
        date=data['date'],
        location=data['location'],
        description=data['description']
    )
    try:
        db.session.add(new_event)
        db.session.commit()
        return jsonify({
            "message": "Event created successfully",
            "event": {
                "eventid": new_event.eventid,
                "title": new_event.title,
                "date": new_event.date,
                "location": new_event.location,
                "description": new_event.description
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
@app.route('/admin/remove_event/<event_id>', methods=['DELETE'])
def remove_event(event_id):
    """Admin removes an event"""
    event = Events.query.filter_by(eventid=event_id).first()
    if not event:
        return jsonify({"message": "Event not found"}), 404

    try:
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event removed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
@app.route('/admin/update_event/<event_id>', methods=['PUT'])
def update_event(event_id):
    """Admin updates an event"""
    data = request.get_json()
    event = Events.query.filter_by(eventid=event_id).first()
    if not event:
        return jsonify({"message": "Event not found"}), 404

    try:
        event.title = data.get('title', event.title)
        event.date = data.get('date', event.date)
        event.location = data.get('location', event.location)
        event.description = data.get('description', event.description)
        db.session.commit()
        return jsonify({
            "message": "Event updated successfully",
            "event": {
                "eventid": event.eventid,
                "title": event.title,
                "date": event.date,
                "location": event.location,
                "description": event.description
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}),


@app.route('/user/events', methods=['GET'])
def get_events():
    """ Get all events """
    events = Events.query.all()
    events_data = []
    for event in events:
        events_data.append({
            "eventid": event.eventid,
            "title": event.title,
            "date": event.date,
            "location": event.location,
            "description": event.description
        })
    return jsonify(events_data), 200

# user can view high alert areas
@app.route('/user/high_alert_areas', methods=['GET'])
def get_high_alert_areas():
    """ Get all high alert areas """
    high_alert_areas = HighAlertAreas.query.all()
    high_alert_areas_data = []
    for area in high_alert_areas:
        high_alert_areas_data.append({
            "areaid": area.areaid,
            "area": area.area
        })
    return jsonify(high_alert_areas_data), 200

# admin can add high alert areas
@app.route('/admin/add_high_alert_area', methods=['POST'])
def add_high_alert_area():
    """"Admin adds high alert areas"""
    data = request.get_json()
    new_area = HighAlertAreas(
        areaid=str(uuid.uuid4()),
        area=data['area']
    )
    try:
        db.session.add(new_area)
        db.session.commit()
        return jsonify({
            "message": "High alert area added successfully",
            "area": {
                "areaid": new_area.areaid,
                "area": new_area.area
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
@app.route('/admin/remove_high_alert_area/<area_id>', methods=['DELETE'])
def remove_high_alert_area(area_id):
    """Admin removes a high alert area"""
    area = HighAlertAreas.query.filter_by(areaid=area_id).first()
    if not area:
        return jsonify({"message": "High alert area not found"}), 404

    try:
        db.session.delete(area)
        db.session.commit()
        return jsonify({"message": "High alert area removed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    

@app.route('/admin/update_high_alert_area/<area_id>', methods=['PUT'])
def update_high_alert_area(area_id):
    """Admin updates a high alert area"""
    data = request.get_json()
    area = HighAlertAreas.query.filter_by(areaid=area_id).first()
    if not area:
        return jsonify({"message": "High alert area not found"}), 404

    try:
        area.area = data.get('area', area.area)
        db.session.commit()
        return jsonify({
            "message": "High alert area updated successfully",
            "area": {
                "areaid": area.areaid,
                "area": area.area
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "An error occurred", "error": str(e)}), 500
    
# # user can give donation
# @app.route('/user/donate', methods=['POST'])
# def donate():
#     data = request.get_json()
#     return jsonify({
#         "message": "Donation received successfully",
#         "data": data
#     }), 200
