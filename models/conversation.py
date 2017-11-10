from models.shared import db


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    second_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    first_message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    second_message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    third_message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    fourth_message_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    fifth_message_id = db.Column(db.Integer, db.ForeignKey('message.id'))

    def __init__(self, first_user_id, second_user_id, first_message_id, second_message_id,
                 third_message_id, fourth_message_id, fifth_message_id):
        self.first_user_id = first_user_id
        self.second_user_id = second_user_id
        self.first_message_id = first_message_id
        self.second_message_id = second_message_id
        self.third_message_id = third_message_id
        self.fourth_message_id = fourth_message_id
        self.fifth_message_id = fifth_message_id

    def __repr__(self):
        return '<Conversation %r between user %r and user %r>' % (self.id, self.first_user_id, self.second_user_id)
