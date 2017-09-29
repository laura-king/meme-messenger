from flask import Blueprint, render_template, url_for, session, redirect
from functools import wraps
from flask_oauthlib.client import OAuth


auth = Blueprint('auth', 'auth', url_prefix='/auth')


# config for the blueprint, holds variable settings
# brought in from the app config
config = {}

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
    # configure these as 1 because they're not valid and the oauth lib will not
    # throw an error, where it would with `None` or `''`
    consumer_key=1,
    consumer_secret=1
)


def configure_oauth(client_id, client_secret, server_url):
    """
    Must be called before these endpoints are called, configures the oauth based on the config file
    :param client_id: the client id for google oauth from the config
    :param client_secret: the client secret for google oauth from the config
    :param server_url: the url that the current server is running on
    """
    google.consumer_key = client_id
    google.consumer_secret = client_secret
    config['SERVER_NAME'] = server_url


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


@auth.route('/login')
def login():
    """
    send user to google oauth page
    :return: authorization results, goes to authorize endpoint next
    """
    callback_url = 'http://' + \
        config['SERVER_NAME'] + url_for('auth.authorized')
    return google.authorize(callback=callback_url)


@auth.route('/logout')
@login_required
def logout():
    """
    logout the user from their session
    :return: redirect to main page
    """
    session.pop('google_token')
    return redirect(url_for('main_page'))


@auth.route('/authorized')
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
