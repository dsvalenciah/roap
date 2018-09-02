'''
Abstract tasks.
'''
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import jwt

from redis import Redis
from rq import Queue

def queue():
    '''
    Get ourselves a default queue.
    '''
    return Queue(connection=Redis(host='redis'))


def send_email(receiver_email):
        """Send user account validation."""
        # TODO: add sender to config file.
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        sender = 'roap.unal.master@gmail.com'
        server.login(sender, "@roap@unal@master")

        token = jwt.encode(
            {'email': receiver_email},
            'dsvalenciah_developer',
            algorithm='HS512'
        ).decode('utf-8')

        message = MIMEMultipart('alternative')

        message['Subject'] = "ROAp account validation"
        message['From'] = sender
        message['To'] = receiver_email

        # TODO: fix host.

        html = f"""
            <html>
                <head></head>
                <body>
                    <p>
                        Hi! Please, click on this <a
                            href="http://localhost:8080/user-validate/{token}"
                        >
                            link
                        </a> to validate your account.
                    </p>
                </body>
            </html>
        """

        message.attach(MIMEText(html, 'html'))

        server.sendmail(
            sender,
            receiver_email,
            message.as_string()
        )
        server.quit()