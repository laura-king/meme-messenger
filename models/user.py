from models.shared import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
    # privacy should only ever be "everyone" or "friends"
    privacy = db.Column(db.String(20))

    def __init__(self, username, email, privacy):
        self.username = username
        self.email = email
        self.privacy = privacy

    def __repr__(self):
        return '<User %r>' % self.username

# helper functions for user

def toggle_privacy(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user.privacy == 'friends':
        user.privacy = 'everyone'
    else:
        user.privacy = 'friends'
    db.session.commit()
    return

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

def get_id_from_username(username):
    user = User.query.filter_by(username=username).first()
    return user.id if user is not None else None

def get_username_from_id(id):
    user = User.query.filter_by(id=id).first()
    return user.username if user is not None else None

def change_username_from_id(id, username):
    user = User.query.filter_by(id=id).first()
    user.username = username
    db.session.commit()
    return

def search_username(username):
    return User.query.filter_by(User.username.like(username)).all() is not None





