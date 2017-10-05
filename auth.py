from flask import Blueprint, render_template, url_for, session, redirect
from functools import wraps
from flask_oauthlib.client import OAuth
from models import user_exists

# constants for accessing session
GOOGLE_TOKEN = 'google_token'
GOOGLE_EMAIL = 'google_email'

auth = Blueprint('auth', __name__, url_prefix='/auth')


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
    :return: user's session token as a string, if one is not in the session (aka user is not logged in) return None
    """
    return session.get(GOOGLE_TOKEN) if GOOGLE_TOKEN in session else None


def get_email():
    """
    get user's Google account email, stores in session for future use if not already there
    :return: user's email as a string, if the user's token is not in the session (aka user is not logged in) return None
    """
    if GOOGLE_TOKEN not in session:
        return None
    if GOOGLE_EMAIL not in session:
        session[GOOGLE_EMAIL] = google.get('userinfo').data['email'] \
            if GOOGLE_TOKEN in session else None
    return session[GOOGLE_EMAIL]


def is_logged_in():
    return get_token() is not None


def login_required(f):
    """
    decorator to add to route when a login is required for that route
    :param f: function to decorate
    :return: redirect to main page if user not logged in, create account page for user without account,
    else go to page requested
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if get_token() is None:
            return redirect(url_for('main_page'))
        # check if user exists in the system, does not use
        # user_exists in users because of circular import
        elif not user_exists(get_email()):
            return redirect(url_for('users.create_account'))
        return f(*args, **kwargs)
    return decorated_function


@auth.route('/login')
def login():
    """
    send user to google oauth page
    :return: authorization results, goes to authorize endpoint next
    """
    # if user already logged in, redirect
    if is_logged_in():
        return redirect(url_for('main_page'))
    callback_url = 'http://' + \
        config['SERVER_NAME'] + url_for('auth.authorized')
    return google.authorize(callback=callback_url)


@auth.route('/logout')
def logout():
    """
    logout the user from their session
    :return: redirect to main page
    """
    session.pop(GOOGLE_TOKEN)
    if GOOGLE_EMAIL in session:
        session.pop(GOOGLE_EMAIL)
    return redirect(url_for('main_page'))


@auth.route('/authorized')
def authorized():
    """
    used by oauth to log user in
    :return: main page if login successful, create user page if email does not exist in system, login failed page otherwise
    """
    resp = google.authorized_response()
    if resp is None:
        return render_template('login_failed.html')
    # add user's token to the session
    session[GOOGLE_TOKEN] = (resp['access_token'], '')
    if not user_exists(get_email()):
        return redirect(url_for('users.create_account'))
    return redirect(url_for('main_page'))
