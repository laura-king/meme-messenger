from models.shared import db
from models.conversation import Conversation, get_conversation, add_conversation
from sqlalchemy.orm import relationship

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500))
    image = db.Column(db.String(500))
    sender = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'),
        nullable=False)
    


    def __init__(self, link, image, sender, timestamp):
        self.link = link
        self.image = image
        self.sender = sender
        self.timestamp = timestamp

    def __repr__(self):
        return '<Message %r>' % self.id

def add_message(message):
    conversation = get_conversation(message['sender'], message['receiver'])
    if not conversation:
        add_conversation(message['sender'], message['receiver'])
    conversation = get_conversation(message['sender'], message['receiver'])
    
    new_message = Message(link=message['link'], image=message['image'], sender=message['sender'], timestamp=message['timestamp'])
    conversation.messages.append(new_message)
    db.session.add(new_message)
    db.session.commit()
    return