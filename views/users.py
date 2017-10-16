from flask import Blueprint, render_template, request, current_app, redirect, url_for

from models import User, db, user_exists, username_taken
from views.auth import is_logged_in, get_email

users = Blueprint('users', __name__, url_prefix='/users')


@users.route('/create_account', methods=['GET', 'POST'])
def create_account():
    # only allow through if user has logged in via oauth
    if is_logged_in():
        # problem with form submission
        problem = None
        email = get_email()
        # make sure user doesn't already have an account
        if not user_exists(email):
            if request.method == 'POST':
                username = request.form['username']
                # make sure username is not already in use
                # TODO: add restrictions on what a username can be (i.e. spaces, special characters, length)
                if username is None or username == '':
                    problem = 'Invalid username'
                elif username_taken(username):
                    problem = 'Username is already taken'
                else:
                    with current_app.app_context():
                        db.session.add(User(username=username, email=email))
                        db.session.commit()
                    return redirect(url_for('main_page'))
        return render_template('create_account.html', email=email, problem=problem)
    return redirect(url_for('main_page'))


@users.route('/account/<username>')
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