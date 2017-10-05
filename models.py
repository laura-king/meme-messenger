from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

# helper functions for user


def user_exists(email):
    """
    function to see if user for a given email exists
    :return: true if user exists, false otherwise
    """
    return User.query.filter_by(email=email).first() is not None


def username_taken(username):
    """
    function to see if an existing user has a given username
    :return: true if username is taken, false otherwise
    """
    return User.query.filter_by(username=username).first() is not None


def get_username_from_email(email):
    user = User.query.filter_by(email=email).first()
    return user.username if user is not None else None
