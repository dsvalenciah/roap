
"""
Contains utility functions to create a administrator into database.
"""
from datetime import datetime

from passlib.hash import sha512_crypt


def create_administrator(db):
    """Create a administrator."""
    # TODO: configure salt from a config file
    administrator = db.users.find_one(
        {'_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49da'}
    )
    dsvalenciah_expert = db.users.find_one(
        {'_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49db'}
    )
    daniel_expert = db.users.find_one(
        {'_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49dc'}
    )
    jani_creator = db.users.find_one(
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

        dsvalenciah_expert = {
            '_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49db',
            'name': 'dsvalenciah',
            'password': sha512_crypt.hash('dsvalenciah', salt='dqwjfdsakuyfd'),
            'email': 'dsvalenciah@unal.edu.co',
            'role': 'expert',
            'status': 'accepted',
            'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'modified': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'deleted': False,
            'validated': True,
            'last_activity': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        }
        db.users.insert_one(dsvalenciah_expert)

        daniel_expert = {
            '_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49dc',
            'name': 'daniel',
            'password': sha512_crypt.hash('daniel', salt='dqwjfdsakuyfd'),
            'email': 'daniel@playvox.co',
            'role': 'expert',
            'status': 'accepted',
            'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'modified': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'deleted': False,
            'validated': True,
            'last_activity': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        }
        db.users.insert_one(daniel_expert)

        jani_creator = {
            '_id': 'ee6a11ae-e52b-4e64-b4a6-a14d42ff49dd',
            'name': 'jani',
            'password': sha512_crypt.hash('jani', salt='dqwjfdsakuyfd'),
            'email': 'jani0720c@gmail.co',
            'role': 'creator',
            'status': 'accepted',
            'created': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'modified': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'deleted': False,
            'validated': True,
            'last_activity': str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
        }
        db.users.insert_one(jani_creator)
