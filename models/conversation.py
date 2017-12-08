from models.shared import db

class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    second_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    messages = db.relationship('Message', backref="conversation")


    def __init__(self, first_user_id, second_user_id):
        self.first_user_id = first_user_id
        self.second_user_id = second_user_id


    def __repr__(self):
        return '<Conversation %r between user %r and user %r>' % (self.id, self.first_user_id, self.second_user_id)

def get_conversation(user_id, other_user_id):
    con = Conversation.query.filter_by(first_user_id=user_id, second_user_id=other_user_id).first()
    if not con:
        con = Conversation.query.filter_by(first_user_id=other_user_id, second_user_id=user_id).first()
    return con

def get_conversations(user_id):
    results = Conversation.query.filter((Conversation.first_user_id == user_id) | (Conversation.second_user_id==user_id)).all()
    return results

def add_conversation(user_id, other_user_id):
    conversation = Conversation(first_user_id=user_id, second_user_id=other_user_id)
    db.session.add(conversation)
    db.session.commit()