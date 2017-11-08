from flask import Blueprint, render_template, request, current_app, redirect, url_for

from models.user import User, db, user_exists, username_taken, get_id_from_username, get_username_from_id, update_privacy, change_username_from_id
from models.blocked import Blocked, block_user_db
from models.friendship import Friendship, add_friend_db
from views.auth import is_logged_in, get_email, get_username

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
                        db.session.add(User(username=username, email=email, privacy='everyone'))
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

    current_user = get_username()
    viewing_self = (username==current_user)
    user_data = {"username": username, "view_self": viewing_self}

    user = User.query.filter_by(username=username).first()
    if not user:
        return render_template('user_nonexistent.html')
    if viewing_self:
        blocked_group = Blocked.query.filter_by(user=user.id).all()

        blocked_names = []
        if len(blocked_group) > 1:
            for blocked_user in blocked_group:
                username = get_username_from_id(blocked_user.blocked)
                blocked_names.append(username)
        elif len(blocked_group) == 1:
            blocked_names.append(get_username_from_id(blocked_group[0].blocked))
        privacy = user.privacy

        user_data.update({"blocked_users": blocked_names, "privacy": privacy})
    return render_template(
        'account_page.html',
        user_data=user_data)

@users.route('/block/', methods=['GET', 'POST'])
def block_user():
    """
    Blocks a user submitted by form from account page
    """
    if request.method == 'POST':
        username = get_username()
        user_id = get_id_from_username(username)
        to_block = get_id_from_username(request.form['block_user'])
        if not to_block or to_block==user_id:
            #TODO: some sort of error if blockee doesn't exist
           return redirect(url_for('users.account_page', username=username))
        block_user_db(user_id, to_block)
    return redirect(url_for('users.account_page', username=username))

@users.route('/friendship', methods=['GET', 'POST'])
def add_friend():
    """
    Adds a friend submitted by form from the account page
    """
    if request.method == 'POST':
        username = get_username()
        user_id =  get_id_from_username(username)
        friend_to_add = get_id_from_username(request.form['add_user'])
        if not friend_to_add or friend_to_add==user_id:
            return redirect(url_for('users.account_page', username=username))
        add_friend_db(user_id, friend_to_add)
    return redirect(url_for('users.account_page', username=username))

@users.route('/privacy', methods=['GET', 'POST'])
def update_privacy():
    if request.method == 'POST':
        username = get_username()
        new_privacy = request.form['privacy']
        if new_privacy.lower()=="everyone" or new_privacy.lower()=="friends":
            user_id = get_id_from_username(username)
            update_privacy(user_id, privacy)
    return redirect(url_for('users.account_page', username=username))

@users.route('/changename/', methods=['GET', 'POST'])
def change_username():
    """
    Blocks a user submitted by form from account page
    """
    if request.method == 'POST':
        username = get_username()
        new_username = request.form['change_username']
        user_id = get_id_from_username(username)
        #TODO: Error handling on database writes lol
        change_username_from_id(user_id, new_username )
    return redirect(url_for('users.account_page', username=new_username))
















