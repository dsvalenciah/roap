'''
Abstract tasks.
'''
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import gettext
import datetime
import jwt
import os

from redis import Redis
from rq import Queue


def queue():
    '''
    Get ourselves a default queue.
    '''
    return Queue('recover_password', connection=Redis(host='redis'))


def send_email(receiver_email, user_lang):
    """Send user account validation."""
    # TODO: add sender to config file.
    server = smtplib.SMTP('smtp.gmail.com:587')
    _ = gettext.translation(
        'recover_password',
        '/code/locale',
        languages=[user_lang]
    ).gettext
    server.ehlo()
    server.starttls()
    sender = os.getenv('SENDER_EMAIL')
    server.login(sender, os.getenv('PASSWORD_SENDER'))

    token = jwt.encode(
        {'email': receiver_email,
          'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        os.getenv('JWT_SECRET'),
        algorithm='HS512'
    ).decode('utf-8')

    message = MIMEMultipart('alternative')

    message['Subject'] = "ROAp recover password"
    message['From'] = sender
    message['To'] = receiver_email

    # TODO: fix host.
    recover_password_message = _((
        'Hi! Please, click on this <a href="{url}/{token}">link</a> '
        'to recover your password account.'
    )).format(
        url=os.getenv('RECOVER_PASSWORD_URL'),
        token=token
    )

    html = """
            <html>
                <head></head>
                <body>
                    <p>
                       {message}
                    </p>
                </body>
            </html>
        """.format(message=recover_password_message)

    message.attach(MIMEText(html, 'html'))

    server.sendmail(
        sender,
        receiver_email,
        message.as_string()
    )
    server.quit()
