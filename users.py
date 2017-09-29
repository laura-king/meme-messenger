from flask import Blueprint, render_template, request, current_app, redirect, url_for
from auth import get_token, get_email
from models import User, db, user_exists, username_taken

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/create_account', methods=['GET', 'POST'])
def create_account():
    # only allow through if user has logged in via oauth
    if get_token() is not None:
        email = get_email()
        # make sure user doesn't already have an account
        if not user_exists(email):
            if request.method == 'POST':
                username = request.form['username']
                # make sure username is not already in use
                # TODO: add restrictions on what a username can be (i.e.
                # spaces, special characters, length)
                if not username_taken(username):
                    with current_app.app_context():
                        db.session.add(User(username=username, email=email))
                        db.session.commit()
            else:
                return render_template('create_account.html', email=email)
    return redirect(url_for('main_page'))
