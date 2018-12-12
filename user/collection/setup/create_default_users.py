
"""
Contains utility functions to create a administrator into database.
"""
from datetime import datetime

from passlib.hash import sha512_crypt


def create_default_users(db):
    """Create a administrator."""
    # TODO: configure salt from a config file
    administrator = db.users.find_one(
        {'_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49da'}
    )
    expert1 = db.users.find_one(
        {'_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49db'}
    )
    expert2 = db.users.find_one(
        {'_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49dc'}
    )
    creator = db.users.find_one(
        {'_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49dd'}
    )
    if not administrator:
        administrator = {
            '_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49da',
            'name': 'administrator',
            'password': sha512_crypt.hash('administrator', salt='dqwjfdsakuyfd'),
            'email': 'administrator@unal.edu.co',
            'role': 'administrator',
            'status': 'accepted',
            'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'modified': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'deleted': False,
            'validated': True,
            'last_activity': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        }
        db.users.insert_one(administrator)

        expert1 = {
            '_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49db',
            'name': 'expert1',
            'password': sha512_crypt.hash('expert1', salt='dqwjfdsakuyfd'),
            'email': 'ohernandezn@unal.edu.co',
            'role': 'expert',
            'status': 'accepted',
            'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'modified': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'deleted': False,
            'validated': True,
            'last_activity': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        }
        db.users.insert_one(expert1)

        expert2 = {
            '_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49dc',
            'name': 'expert2',
            'password': sha512_crypt.hash('expert2', salt='dqwjfdsakuyfd'),
            'email': 'expert2@unal.edu.co',
            'role': 'expert',
            'status': 'accepted',
            'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'modified': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'deleted': False,
            'validated': True,
            'last_activity': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        }
        db.users.insert_one(expert2)

        creator = {
            '_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49dd',
            'name': 'creator',
            'password': sha512_crypt.hash('creator', salt='dqwjfdsakuyfd'),
            'email': 'creator@unal.edu.co',
            'role': 'creator',
            'status': 'accepted',
            'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'modified': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'deleted': False,
            'validated': True,
            'last_activity': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        }
        db.users.insert_one(creator)
