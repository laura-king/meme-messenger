from models.shared import db

class Friendship(db.Model):
    user = db.Column(db.Integer, primary_key=True)
    friend = db.Column(db.Integer, primary_key=True)

    def __init__(self, user, friend):
        self.user = user
        self.friend = friend