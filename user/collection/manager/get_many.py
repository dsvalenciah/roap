from manager.exceptions.user import UserPermissionError


def get_many(db_client, filter_, range_, sorted_, auth_user):
    """Get users with query."""
    # TODO: fix it and remove find().
    _ = auth_user.get('language')
    if auth_user.get('role') != 'administrator':
        raise UserPermissionError(
            _('User not have sufficient permissions to do this action.')
        )

    start, end = range_
    field, order = sorted_

    cursor = db_client.users.find(filter_)

    return list(
        cursor
        .sort([(field, -1 if order == 'DESC' else 1)])
        .skip(start)
        .limit(end - start)
    ), cursor.count()
