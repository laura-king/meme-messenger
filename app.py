from flask import Flask, render_template, url_for, session, redirect
from functools import wraps
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.config.from_pyfile('app.cfg')

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


@app.route('/conversation')
def converse():
    # Implement socket functionality
    conversationMessages = ["Message 1", "Message 2", "Message 3", "Message 4", "Message 5", "Message 6"]
    return render_template('conversation.html', messages=conversationMessages, username="Mack Bowe")

@app.route('/')
def main_page():
    """
    Loads main page
    """
    return render_template('base_page.html')


if __name__ == "__main__":
    app.run()
