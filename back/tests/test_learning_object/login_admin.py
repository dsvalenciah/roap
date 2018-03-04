
"""
Contain utility to manage admin session.
"""

import json


def login_admin(users_cli):
    """Login admin user."""
    admin = {
        'email': 'administrator@unal.edu.co',
        'password': 'administrator',
    }
    response = users_cli.simulate_post(
        '/back/login',
        body=json.dumps(admin)
    )
    return response.json.get('token')
