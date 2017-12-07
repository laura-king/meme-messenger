from models.shared import db
from models.message import Message

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

def  generate_conversations(user_id):
    c1 = Conversation(first_user_id=user_id, second_user_id=2)
    m1 = Message(link="test", image="test", sender=user_id)
    m2 = Message(link="test", image="test", sender=user_id)
    c1.messages.extend([m1, m2])

    db.session.add(c1)
    db.session.add_all([m1, m2])
    db.session.commit()

def get_conversations(user_id):
    results = Conversation.query.filter((Conversation.first_user_id == user_id) | (Conversation.second_user_id==user_id)).all()
    return results