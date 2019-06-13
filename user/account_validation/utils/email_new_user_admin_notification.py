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
    return Queue('new_user_admin_notification', connection=Redis(host='redis'))


def send_email():
    """Send user account validation."""
    sender = os.getenv('SENDER_EMAIL')

    notification_message = _((
        'Hola. Hay un nuevo usuario en ROAp.'
    ))

    sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(sender)
    to_email = Email(os.getenv('ROAP_ADMIN'))
    subject = _("ROAp: Notificación de nuevo usuario")
    content = Content("text/html", notification_message)
    mail = Mail(from_email, subject, to_email, content)
    sg.client.mail.send.post(request_body=mail.get())
