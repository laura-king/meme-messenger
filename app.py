from flask import Flask, render_template
import praw

from models.shared import db
import models.blocked
import models.user
import models.friendship
from views import auth as auth, users as users
from api import random_meme

# start and configure app
app = Flask(__name__)
app.config.from_pyfile('app.cfg')
db.init_app(app)

# register blueprints
app.register_blueprint(auth.auth)
app.register_blueprint(users.users)
app.register_blueprint(random_meme.random_meme)


# configure oauth with the client id, client secret, and server url
auth.configure_oauth(
    app.config['GOOGLE_OAUTH_CLIENTID'],
    app.config['GOOGLE_OAUTH_SECRET'],
    app.config['SERVER_NAME'])

random_meme.configure_reddit(
    app.config['REDDIT_CLIENT_ID'],
    app.config['REDDIT_CLIENT_SECRET'],
    app.config['REDDIT_USERNAME']
)


@app.route('/')
def main_page():
    """
    Loads main page
    """
    username = models.user.get_username_from_email(auth.get_email())
    return render_template('index.html', logged_in=auth.is_logged_in(), username=username)


if __name__ == "__main__":
    app.run(threaded=True)
