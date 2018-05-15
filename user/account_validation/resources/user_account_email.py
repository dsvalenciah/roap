from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import jwt


class UserEmail(object):
    """Deal with user validation."""

    def on_get(self, req, resp, email):
        """Send user account validation."""
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        sender = 'roap.unal.master@gmail.com'
        receiver = email
        server.login(sender, "@roap@unal@master")

        token = jwt.encode(
            {'email': receiver},
            'dsvalenciah_developer',
            algorithm='HS512'
        ).decode('utf-8')

        message = MIMEMultipart('alternative')

        message['Subject'] = "ROAp account validation"
        message['From'] = sender
        message['To'] = receiver

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
            receiver,
            message.as_string()
        )
        server.quit()