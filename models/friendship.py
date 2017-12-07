from models.shared import db
from models.user import get_username_from_id

class Friendship(db.Model):
    user = db.Column(db.Integer, primary_key=True)
    friend = db.Column(db.Integer, primary_key=True)

    def __init__(self, user, friend):
        self.user = user
        self.friend = friend

def add_friend_db(user_id, friend):
    """
    Adds a user to a blocked list of users

    Args:
    user_id - user ID of a user seeking to block another user
    friend - user ID of friend to be added
    """
    db.session.add(Friendship(user=user_id, friend=friend))
    db.session.commit()
    return

def get_friends_db(user_id):
    """
    Queries for a list of friends
    """
    friends = []
    results = Friendship.query.filter_by(user=user_id).all()
    for record in results:
        friend_username = get_username_from_id(record.friend)
        friends.append(friend_username)
    return friends
    