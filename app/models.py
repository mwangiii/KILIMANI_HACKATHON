from app import db

class User(db.Model):
    __tablename__ = 'users'

    userid = db.Column(db.String, primary_key=True)
    profilepicture = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    phone = db.Column(db.String)

class Posts(db.Model):
    __tablename__ = 'posts'

    postid = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.String)
    author = db.Column(db.String, db.ForeignKey('users.userid'))
    time = db.Column(db.DateTime)

class Comments(db.Model):
    __tablename__ = 'comments'

    commentid = db.Column(db.String, primary_key=True)
    content = db.Column(db.String)
    author = db.Column(db.String, db.ForeignKey('users.userid'))
    time = db.Column(db.DateTime)


class Polls (db.Model):
    __tablename__ = 'polls'

    pollid = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    number_of_votes = db.Column(db.Integer)

class Events (db.Model):
    __tablename__ = 'events'

    eventid = db.Column(db.String, primary_key=True)
    title = db.Column(db.String)
    date = db.Column(db.DateTime)
    location = db.Column(db.String)
    description = db.Column(db.String)


class High_Alert_areas (db.Model):
    __tablename__ = 'high_alert_areas'

    areaid = db.Column(db.String, primary_key=True)
    area = db.Column(db.String)
    description = db.Column(db.String)