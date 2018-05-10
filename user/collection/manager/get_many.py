from manager.exceptions.user import UserPermissionError

def get_many(db_client, auth_user, query=None):
    """Get users with query."""
    # TODO: fix it and remove find().
    if auth_user.get('role') != 'administrator':
        raise UserPermissionError(
            ['User not have sufficient permissions to do this action.']
        )

    for q_name, q_value in query.items():
        if q_value == 'false':
            query[q_name] = False
        if q_value == 'true':
            query[q_name] = True

    if query:
        users = db_client.users.find(query)
        return list(users)
    else:
        return list(db_client.users.find())