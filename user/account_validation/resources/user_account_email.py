import falcon
from utils.email_jobs import queue


class UserEmail(object):
    """Deal with user validation."""

    def on_get(self, req, resp, email):
        """Send user account validation."""
        queue().enqueue('utils.email_jobs.send_email',
                        email, req.cookies.get('user_lang') or 'es_CO')
        resp.media = {'status': 'ok'}
