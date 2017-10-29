import os

from flask import Blueprint, render_template, request, app, url_for
from werkzeug.utils import secure_filename, redirect

message = Blueprint('message', __name__, url_prefix='/message')

ALLOWED_EXTENSIONS = set('.jpg')

@message.route('/conversation')
def converse():
    # Implement socket functionality

    conversationMessages = ["Message 1", "Message 2", "Message 3", "Message 4", "Message 5", "Message 6"]
    return render_template('conversation.html', messages=conversationMessages, username="Mack Bowe")

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