from flask import Flask, render_template, url_for, session, redirect
from functools import wraps
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db = SQLAlchemy(app)

# Database Models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

# Auth setup/helper methods


oauth = OAuth()
google = oauth.remote_app(
    'google',
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    consumer_key=app.config['GOOGLE_OAUTH_CLIENTID'],
    consumer_secret=app.config['GOOGLE_OAUTH_SECRET']
)


@google.tokengetter
def get_token():
    """
    get user's session token
    :return: user's session token as a string, if one is not stored return None
    """
    return session.get('google_token') if 'google_token' in session else None


def login_required(f):
    """
    decorator to add to route when a login is required for that route
    :param f: function to decorate
    :return: redirect to login if user not logged in, else the function passed in
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if get_token() is None:
            return redirect(url_for('main_page'))
        return f(*args, **kwargs)
    return decorated_function

# Routes


@app.route('/login')
def login():
    """
    send user to google oauth page
    :return: authorization results, goes to authorize endpoint next
    """
    callback_url = 'http://' + \
        app.config['SERVER_NAME'] + url_for('authorized')
    return google.authorize(callback=callback_url)


@app.route('/logout')
@login_required
def logout():
    """
    logout the user from their session
    :return: redirect to main page
    """
    session.pop('google_token')
    return redirect(url_for('main_page'))


@app.route('/authorized')
def authorized():
    """
    used by oauth to log user in
    :return: main page if login successful, login failed page otherwise
    """
    resp = google.authorized_response()
    if resp is None:
        return render_template('login_failed.html')
    session['google_token'] = (resp['access_token'], '')
    return redirect(url_for('main_page'))


@app.route('/')
def main_page():
    """
    Loads main page
    """
    return render_template('base_page.html')


@app.route('/welcome')
def welcome_page():
    """
    Loads welcome page
    """
    return render_template('welcome.html')


@app.route('/account/<username>')
def account_page(username):
    """
    Loads account page
    """
    # See if this user is the user looking
    # Check to see if a user exists with that name
    existing_user = True
    user_data = {"username": username}
    if existing_user:
        # Temp List for now
        blocked = ['BigJim', 'Jerkface420', 'GuyFerrari']
        # Obtain the user's information somehow and package it in a dictonary
        user_data.update({"blocked_users": blocked, "privacy": 'friends'})
    return render_template(
        'account_page.html',
        user_data=user_data,
        existing_user=existing_user)


if __name__ == "__main__":
    app.run()
