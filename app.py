from flask import Flask, render_template
import auth as auth
import users as users
from models import db, get_username_from_email

# start and configure app
app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db.init_app(app)

# register blueprints
app.register_blueprint(auth.auth)
app.register_blueprint(users.users)


# configure oauth with the client id, client secret, and server url
auth.configure_oauth(
    app.config['GOOGLE_OAUTH_CLIENTID'],
    app.config['GOOGLE_OAUTH_SECRET'],
    app.config['SERVER_NAME'])

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
    username = get_username_from_email(auth.get_email())
    return render_template('index.html', logged_in=auth.is_logged_in(), username=username)


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
        # Obtain the user's information somehow and package it in a dictionary
        user_data.update({"blocked_users": blocked, "privacy": 'friends'})
    return render_template(
        'account_page.html',
        user_data=user_data,
        existing_user=existing_user)


if __name__ == "__main__":
    app.run()
