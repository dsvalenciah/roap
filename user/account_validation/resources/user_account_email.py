from utils.email_jobs import queue

class UserEmail(object):
    """Deal with user validation."""

    def on_get(self, req, resp, email):
        """Send user account validation."""
        queue().enqueue('utils.email_jobs.send_email', email)
        resp.media = {'status': 'ok'}