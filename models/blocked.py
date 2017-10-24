from models.shared import db

class Blocked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # ID of the user who has done the blocking
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # ID of the blocked user 
    blocked = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, user, blocked):
        self.user = user
        self.blocked = blocked


def block_user(user, to_block):
    """
    Adds a user to a blocked list of users

    Args:
    user - user ID of a user seeking to block another user
    to_block - the to be blocked userID
    """
    db.session.add(Blocked(user=user, blocked=to_block))
    db.session.commit()
    return

    