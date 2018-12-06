
"""
Contains utility functions to works with learning-object rating.
"""

from datetime import datetime
from uuid import uuid4
from manager.exceptions.learning_object import (
    InvalidUserRaterRole, InvalidRatingValue, UserCannotRate
)


def rating_one(db_client, learining_object_id, rater_role, rating, user):
    """Modify learning object."""

    user_role = user.get('role')
    user_id = user.get('_id')
    accepted_roles = ["expert", "creator"]
    accepted_rating = range(1, 6)
    _ = user.get('language')

    if user_role != rater_role:
        raise InvalidUserRaterRole(
            _('An a {user_role} cant rate this learning object (only {rater_role}).').format(
                user_role=user_role, rater_role=rater_role)
        )

    if user_role not in accepted_roles:
        raise InvalidUserRaterRole(
            _('An a {user_role} cant rate this learning object (only {accepted_roles}).').format(
                user_role=user_role, accepted_roles=accepted_roles)
        )

    if rating not in accepted_rating:
        raise InvalidRatingValue(_('Invalid ratig (only [1, 5]).'))

    learning_objects_to_update = db_client.learning_objects.find(
        {
            '_id': learining_object_id,
            'expert_ids': user_id
        }
    ).count()

    if not learning_objects_to_update:
        raise UserCannotRate(
            _('This user cant rate this learning object {user_id}.').format(
                user_id=user_id)
        )

    for rating_value in range(1, 6):
        db_client.learning_objects.find_one_and_update(
            {
                '_id': learining_object_id,
                'expert_ids': user_id
            },
            {
                "$pull": {
                    f"rating.{user_role}.{rating_value}": {
                        "creator_id": user_id
                    }
                }
            }
        )

    db_client.learning_objects.find_one_and_update(
        {
            '_id': learining_object_id,
            'expert_ids': user_id
        },
        {
            '$push': {
                f"rating.{user_role}.{rating}": {
                    '_id': str(uuid4()),
                    'creator_id': user.get('_id'),
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                }
            }
        }
    )
