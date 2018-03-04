
"""
Contain utility to test learning objects operations from creator user.
"""
from uuid import uuid4
import json

from tests.test_learning_object.login_admin import login_admin


def login_creator_user(cli, name='ctr', email='ctr@mail.com', password='ctr'):
    """Login creator user."""
    # Login administrator.
    admin_jwt_token = login_admin(cli)

    user = {
        'name': name,
        'email': email,
        'password': password
    }

    # Create a user,
    response = cli.simulate_post(
        '/back/user',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    user_id = response.json.get('_id')

    # Administrator is modifying created user's role.
    response = cli.simulate_put(
        f'/back/user/{user_id}',
        headers={
            'AUTHORIZATION': admin_jwt_token,
            'Content-Type': 'application/json'
        },
        body=json.dumps({'role': 'creator'})
    )

    # Created user login.
    response = cli.simulate_post(
        '/back/login',
        body=json.dumps({'email': email, 'password': password})
    )

    creator_jwt_token = response.json.get('token')

    # Returns user's JWT token.
    return creator_jwt_token


def test_post_with_valid_object_json(learning_objects_cli, one_dict_lom):
    """An a docstring."""
    # Create user and login it.
    creator_jwt_token = login_creator_user(learning_objects_cli)

    # Create a learning object.
    response = learning_objects_cli.simulate_post(
        '/back/object',
        headers={
            'AUTHORIZATION': creator_jwt_token,
            'Content-Type': 'application/json'
        },
        body=json.dumps(one_dict_lom)
    )

    # Assert learning object was created.
    assert response.status_code == 201

    learning_object_id = response.json.get('_id')

    response = learning_objects_cli.simulate_get(
        f'/back/object/{learning_object_id}',
        headers={
            'AUTHORIZATION': creator_jwt_token
        },
        params={'format': 'json'}
    )

    # Assert learning object exists.
    assert response.json == one_dict_lom
    assert response.status_code == 200

    # Create user b and login it.
    creatorb_jwt_token = login_creator_user(
        learning_objects_cli,
        email='ctrb@mail.com',
        name='ctrb',
        password='ctrb'
    )

    # User b checks if can access to previously created learning object.
    response = learning_objects_cli.simulate_get(
        f'/back/object/{learning_object_id}',
        headers={
            'AUTHORIZATION': creatorb_jwt_token
        },
        params={'format': 'json'}
    )

    # Assert user b cant access to created learning object.
    assert response.status_code == 401


def test_post_without_valid_object_json(learning_objects_cli):
    """An a docstring."""
    # Create user and login it.
    creator_jwt_token = login_creator_user(learning_objects_cli)

    # Create an invalid learning object.
    response = learning_objects_cli.simulate_post(
        '/back/object',
        headers={
            'AUTHORIZATION': creator_jwt_token,
            'Content-Type': 'application/json'
        },
        body=json.dumps({})
    )

    # User makes a bad request.
    assert response.status_code == 400


def test_post_with_valid_object_xml(learning_objects_cli, one_xml_lom):
    """An a docstring."""
    # Create user and login it.
    creator_jwt_token = login_creator_user(learning_objects_cli)

    # Create a learning object.
    response = learning_objects_cli.simulate_post(
        '/back/object',
        headers={
            'AUTHORIZATION': creator_jwt_token,
            'Content-Type': 'text/xml'
        },
        body=one_xml_lom
    )

    # Assert if it's not have errors.
    assert response.json.get('description') is None
    # Assert if it's already created.
    assert response.status_code == 201

    learning_object_id = response.json.get('_id')

    response = learning_objects_cli.simulate_get(
        f'/back/object/{learning_object_id}',
        headers={
            'AUTHORIZATION': creator_jwt_token
        },
        params={'format': 'xml'}
    )

    assert response.status_code == 200


def test_post_without_valid_object_xml(learning_objects_cli):
    """An a docstring."""
    creator_jwt_token = login_creator_user(learning_objects_cli)
    pass


def test_get_with_existent_object_json(learning_objects_cli):
    """An a docstring."""
    pass


def test_get_without_existent_object_json(learning_objects_cli):
    """An a docstring."""
    pass


def test_get_with_existent_object_xml(learning_objects_cli):
    """An a docstring."""
    pass


def test_get_without_existent_object_xml(learning_objects_cli):
    """An a docstring."""
    pass


def test_get_with_query_params_json(learning_objects_cli):
    """An a docstring."""
    pass


def test_get_with_query_params_xml(learning_objects_cli):
    """An a docstring."""
    pass


def test_put_without_authorization(learning_objects_cli):
    """Test put without authorization."""
    response = learning_objects_cli.simulate_put(
        f'/back/object/{uuid4().hex}'
    )
    assert response.status_code == 401


def test_put_with_valid_object_json(learning_objects_cli):
    """An a docstring."""
    pass


def test_put_without_valid_object_json(learning_objects_cli):
    """An a docstring."""
    pass


def test_put_without_existent_object_json(learning_objects_cli):
    """An a docstring."""
    pass


def test_put_with_valid_object_xml(learning_objects_cli):
    """An a docstring."""
    pass


def test_put_without_valid_object_xml(learning_objects_cli):
    """An a docstring."""
    pass


def test_put_without_existent_object_xml(learning_objects_cli):
    """An a docstring."""
    pass


def test_delete_without_authorization(learning_objects_cli):
    """Test delete without authorization."""
    response = learning_objects_cli.simulate_delete(
        f'/back/object/{uuid4().hex}'
    )
    assert response.status_code == 401


def test_delete_with_existent_object(learning_objects_cli):
    """An a docstring."""
    pass


def test_delete_without_existent_object(learning_objects_cli):
    """An a docstring."""
    pass
