from models.shared import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String(500))
    image = db.Column(db.String(500))

    def __init__(self, link, image):
        self.link = link
        self.image = image

    def __repr__(self):
        return '<Message %r>' % self.id
