'''
Abstract tasks.
'''
import datetime
import gettext
import os

import jwt
import sendgrid
from redis import Redis
from rq import Queue
from sendgrid.helpers.mail import Content, Email, Mail


def queue():
    '''
    Get ourselves a default queue.
    '''
    return Queue('recover_password', connection=Redis(host='redis'))


def send_email(receiver_email, user_lang):
    """Send user account validation."""
    _ = gettext.translation(
        'recover_password',
        '/code/locale',
        languages=[user_lang]
    ).gettext
    sender = os.getenv('SENDER_EMAIL')

    token = jwt.encode(
        {'email': receiver_email,
          'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        os.getenv('JWT_SECRET'),
        algorithm='HS512'
    ).decode('utf-8')

    recover_password_message = _((
        'Hi! Please, click on this <a href="{url}/{token}">link</a> '
        'to recover your password account.'
    )).format(
        url=os.getenv('RECOVER_PASSWORD_URL'),
        token=token
    )

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(sender)
    to_email = Email(receiver_email)
    subject = _("ROAp: recover password")
    content = Content("text/html", recover_password_message)
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())
