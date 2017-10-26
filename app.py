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


@app.route('/')
def main_page():
    """
    Loads main page
    """
    username = models.user.get_username_from_email(auth.get_email())
    return render_template('index.html', logged_in=auth.is_logged_in(), username=username)


if __name__ == "__main__":
    app.run()
