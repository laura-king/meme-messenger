from flask import session, redirect, url_for
from flask_oauthlib.client import OAuth
from flask import current_app as app


# constant for key referencing google token stored in session
GOOGLE_TOKEN = 'google_token'

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


def login(callback_url):
    return google.authorize(callback=callback_url)


def logout():
    session.pop(GOOGLE_TOKEN)
    authorized_url = url_for('authorized')
    return redirect(authorized)

@google.authorized_handler
def authorized(resp):
    # resp = google.authorized_response()
    if resp is None:
        return False
    session[GOOGLE_TOKEN] = (resp['access_token'], '')
    return url_for('main_page')


@google.tokengetter
def get_token():
    return session.get(GOOGLE_TOKEN)
