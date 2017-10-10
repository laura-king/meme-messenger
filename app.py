import os
from werkzeug import secure_filename
from flask import Flask, render_template, request
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



@app.route('/conversation')
def converse():
    # Implement socket functionality
    conversationMessages = ["Message 1", "Message 2", "Message 3", "Message 4", "Message 5", "Message 6"]
    return render_template('conversation.html', messages=conversationMessages, username="Mack Bowe")

def allowed_type(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_type(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_MEME'], filename))
            return redirect(url_for('conversation'))

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
