# import sqlachemy and create a db object
from flask import Flask
from flask_sqlalchemy import SQLAlchemy   

app = Flask(__name__)
db = SQLAlchemy()

#`import the routes
from app import routes

# import the User model
from app.models import User
