from models.shared import db
from models.conversation import Conversation, get_conversation, add_conversation
from models.user import get_id_from_username
from sqlalchemy.orm import relationship

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500))
    image = db.Column(db.String(500))
    sender = db.Column(db.String(500), nullable=False)
    receiver = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'),
        nullable=False)
    


    def __init__(self, link, image, sender, receiver, timestamp):
        self.link = link
        self.image = image
        self.sender = sender
        self.receiver = receiver
        self.timestamp = timestamp

    def __repr__(self):
        return '<Message %r>' % self.id

def add_message(message):
    sender_id = get_id_from_username(message['sender'])
    receiver_id = get_id_from_username(message['receiver'])

    #Find conversation to add message to
    conversation = get_conversation(sender_id, receiver_id)
    if not conversation:
        add_conversation(sender_id, receiver_id)
        conversation = get_conversation(sender_id, receiver_id)

    new_message = Message(link=message['link'], image=message['image'], sender=message['sender'], receiver=message['receiver'], timestamp=message['timestamp'])
    conversation.messages.append(new_message)
    db.session.add(new_message)
    db.session.commit()
    return