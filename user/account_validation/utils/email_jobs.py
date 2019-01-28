'''
Abstract tasks.
'''
import gettext
import os

import jwt
import sendgrid
from redis import Redis
from rq import Queue
from sendgrid.helpers.mail import Email, Content, Mail


def queue():
    '''
    Get ourselves a default queue.
    '''
    return Queue('account_validation', connection=Redis(host='redis'))


def send_email(receiver_email, user_lang):
    """Send user account validation."""
    _ = gettext.translation(
        'account_validation',
        '/code/locale',
        languages=[user_lang]
    ).gettext
    sender = os.getenv('SENDER_EMAIL')

    token = jwt.encode(
        {'email': receiver_email},
        os.getenv('JWT_SECRET'),
        algorithm='HS512'
    ).decode('utf-8')

    validate_message = _((
        'Hi! Please, click on this <a href="{url}/{token}">link</a> '
        'to validate your account.'
    )).format(
        url=os.getenv('ACCOUNT_VALIDATION_URL'),
        token=token
    )

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(sender)
    to_email = Email(receiver_email)
    subject = _("ROAp: account validation")
    content = Content("text/html", validate_message)
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())
