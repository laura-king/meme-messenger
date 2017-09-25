from flask import Flask, render_template, url_for, session, redirect
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.config.from_pyfile('app.cfg')

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


@app.route('/login')
def login():
    callback_url = 'http://' + \
        app.config['SERVER_NAME'] + url_for('authorized')
    return google.authorize(callback=callback_url)


@app.route('/logout')
def logout():
    session.pop('google_token')
    return redirect(url_for('main_page'))


@app.route('/authorized')
@google.authorized_handler
def authorized(resp):
    if resp is None:
        return False
    session['google_token'] = (resp['access_token'], '')
    return redirect(url_for('main_page'))


@app.route('/')
def main_page():
    """
    Loads main page
    """
    return render_template('base_page.html')


@google.tokengetter
def get_token():
    return session.get('google_token')


if __name__ == "__main__":
    app.run()
