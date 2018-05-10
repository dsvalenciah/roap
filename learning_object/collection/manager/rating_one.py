
"""
Contains utility functions to works with learning-object rating.
"""

from datetime import datetime
from uuid import uuid4

def rating_one(db_client, learining_object_id, rating, user):
    """Modify learning object."""

    user_role = user.get('role')
    accepted_role = ["expert", "creator"]
    accepted_rating = map(str, range(1, 6))
    if user_role in accepted_role and rating in accepted_rating:
        for rating_value in range(1, 6):
            db_client.learning_objects.find_one_and_update(
                {'_id': learining_object_id},
                {
                    "$pull": {
                        f"rating.{user_role}.{rating_value}" : {
                            "user_id": user.get('_id')
                        }
                    }
                }
            )
        db_client.learning_objects.find_one_and_update(
            {'_id': learining_object_id},
            {
                '$push': {
                    f"rating.{user_role}.{rating}": {
                        '_id': str(uuid4()),
                        'user_id': user.get('_id'),
                        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    }
                }
            }
        )
    else:
        # TODO: raise error.
        pass