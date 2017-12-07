from models.shared import db
from sqlalchemy.orm import relationship

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500))
    image = db.Column(db.String(500))
    sender = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'),
        nullable=False)
    


    def __init__(self, link, image, sender):
        self.link = link
        self.image = image
        self.sender = sender

    def __repr__(self):
        return '<Message %r>' % self.id
