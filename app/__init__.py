# import sqlachemy and create a db object
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres.yjcwujxfuochezvwnndp:QfGmTEjjPnfnolJN@aws-0-us-east-1.pooler.supabase.com:6543/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import models
from app import routes
migrate = Migrate(app, db)
# with app.app_context():
#     db.create_all()
