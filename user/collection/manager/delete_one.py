from manager.exceptions.user import UserPermissionError, UserNotFoundError


def delete_one(db_client, user_id, auth_user):
    """Delete a user by user_id."""
    # TODO: Admin not self delete
    auth_user_role = auth_user.get('role')
    auth_user_id = auth_user.get('_id')
    _ = auth_user.get('language')
    if auth_user_role == 'administrator' and user_id != auth_user_id:
        raise UserPermissionError(
            _('User not have sufficient permissions to do this action.')
        )
    if user_id != auth_user_id:
        raise UserPermissionError(
            _('User not have sufficient permissions to do this action.')
        )

    result = db_client.users.find_one_and_delete({'_id': user_id})
    if not result.deleted_count:
        raise UserNotFoundError(_('The user is not deleted.'))
