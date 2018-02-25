
"""
Contains utility functions to works with authorization.
"""

import json

import jwt
import falcon


RESOURCES_NAME = {
    'User': 'user',
    'UserCollection': 'user',
    'LearningObject': 'learning-object',
    'LearningObjectCollection': 'learning-object',
    'LearningObjectMetadata': 'learning-object-metadata',
    'CollectionsCategory': 'collections-category'
}


def determine_action(source_uid, target_uid):
    """Compare two uid."""
    return 'self' if source_uid == target_uid else 'others'


def authorize_action(method, resource_name, role, status, uid, params):
    """Authorize action."""
    if status == 'inactive':
        return False
    authorizations = json.load(open('config/data/authorizations.json'))
    permissions = authorizations.get(role).get(resource_name).get(method)
    can_realize_action = False
    if isinstance(permissions, list):
        action = determine_action(uid, params.get('uid'))
        can_realize_action = action in permissions
    elif isinstance(permissions, bool):
        can_realize_action = permissions
    return can_realize_action


class Authorize(object):
    """Deal with the user authorization."""

    def __init__(self):
        """Init."""
        pass

    def __call__(self, req, resp, resource, params):
        """Authorize request."""
        # TODO: get secret from configuration file and fix raise errors
        authorization = req.headers.get('AUTHORIZATION')
        resource_name = RESOURCES_NAME.get(
            resource.__class__.__name__
        )
        method = req.method.lower() + (
            '_many' if 'Collection' in resource_name else ''
        )

        try:
            payload = jwt.decode(
                authorization,
                'dsvalenciah_developer',
                verify='True',
                algorithms=['HS512'],
                options={'verify_exp': True}
            )
        except jwt.ExpiredSignatureError as e:
            raise falcon.HTTPUnauthorized('Error1', str(e))
        except jwt.DecodeError as e:
            raise falcon.HTTPUnauthorized('Error1', str(e))

        role = payload.get('role')
        status = payload.get('status')
        uid = payload.get('uid')

        authorized = authorize_action(
            method, resource_name, role, status, uid, params
        )

        if not authorized:
            raise falcon.HTTPUnauthorized('Error2')
