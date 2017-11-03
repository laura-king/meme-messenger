from models.shared import db

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
    db.session.add(Blocked(user=user_id, friend=friend))
    db.session.commit()
    return

    