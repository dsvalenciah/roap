
"""
Contains utility functions to create a administrator into database.
"""
from datetime import datetime

from passlib.hash import sha512_crypt

from utils.user import User as UserManager


def create_administrator(db):
    """Create a administrator."""
    # TODO: configure salt from a config file
    administrator = db.users.find_one(
        {'_id': 'ee6a11aee52b4e64b4a6a14d42ff49da'}
    )
    if not administrator:
        administrator = {
            '_id': 'ee6a11aee52b4e64b4a6a14d42ff49da',
            'name': 'administrator',
            'email': 'administrator@unal.edu.co',
            'password': sha512_crypt.hash('adminpass', salt='dqwjfdsakuyfd'),
            'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'modified': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'last_activity': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'status': 'active',
            'role': 'administrator',
        }
        db.users.insert_one(administrator)
