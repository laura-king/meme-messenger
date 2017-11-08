import os

from sqlalchemy import null

from models.message import Message
from models.conversation import Conversation
from models.user import get_username_from_id, get_id_from_username
from flask import Blueprint, render_template, request, app, url_for
from werkzeug.utils import secure_filename, redirect
from views.auth import is_logged_in, get_email, get_username, login

message = Blueprint('message', __name__, url_prefix='/message')

ALLOWED_EXTENSIONS = set('.jpg')

@message.route('/conversation')
def converse(messaging_user=""):
    # Implement socket functionality

    # check log in and grab user name
    if is_logged_in():

        #check log in and grab user name
        main_user = get_username()
        new_user = False

        #if no user is selected grab the most recent convo
        if messaging_user == "":
            cur_convo = Conversation.query.filter_by(first_user_id=get_id_from_username(main_user), second_user_id=get_id_from_username(main_user)).first()
            if cur_convo == None:
                new_user=True
            #messaging_user= cur_convo.second_user_id
            #conversation(main_user, messaging_user)
        else:
            conversation(main_user,messaging_user)

    else:
        #send to home screen if not logged in user
        return redirect('/auth/login')

    conversationMessages = ["Message 1", "Message 2", "Message 3", "Message 4", "Message 5", "Message 6"]
    return render_template('conversation.html', messages=conversationMessages, username=get_username(), new_user = new_user)

@message.route('/conversation/<messaging_user>')
def conversation(main_user, messaging_user):
    # grab conversation for two users
    print(messaging_user)

def allowed_type(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@message.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_type(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_MEME'], filename))
            return redirect(url_for('conversation'))