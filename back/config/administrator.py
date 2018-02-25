
"""
Contains utility functions to create a administrator into database.
"""
from datetime import datetime

from passlib.hash import sha512_crypt

from utils.user import User as UserManager
from exceptions.user import UserNotFoundError


def create_administrator(db):
    """Create a administrator."""
    # TODO: configure salt from a config file
    user_manager = UserManager(db)
    try:
        user_manager.get_one('administrator')
    except UserNotFoundError:
        administrator = {
            '_id': 'administrator',
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
