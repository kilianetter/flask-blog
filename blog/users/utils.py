

from flask import url_for, current_app
from blog import mail
# mail
from flask_mail import Message

# secrets for picture upload -- why?
import secrets
import os
# image resizing
from PIL import Image

def savePicture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + file_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile', picture_fn)
    # image resizing
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def sendResetMail(user):
    token = user.getResetToken()
    msg = Message(
        'Password Reset Request', 
        sender="noreply@phobox.de",
        recipients=[user.email])
    msg.body = f'''
    To reset your password visit the following Link:
    {url_for('users.reset_token', token=token, _external=True)}
    if you did not make this requst, simply ignore this email. no changes have been made
    '''
    mail.send(msg)