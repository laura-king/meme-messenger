import os
from werkzeug import secure_filename
from flask import Flask, render_template, request
import auth as auth
import users as users
from models import db, get_username_from_email
from flask import Flask, render_template

from models.shared import db
import models.blocked, models.user, models.message, models.conversation
from views import auth as auth, users as users

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
    username = models.user.get_username_from_email(auth.get_email())
    return render_template('index.html', logged_in=auth.is_logged_in(), username=username)


if __name__ == "__main__":
    app.run()
