
"""
Contain utility functions to test user Resources.
"""

from uuid import uuid4
import json


def login_admin(users_cli):
    """Login admin user."""
    admin = {
        'email': 'administrator@unal.edu.co',
        'password': 'adminpass',
    }
    response = users_cli.simulate_post(
        '/back/login',
        body=json.dumps(admin)
    )
    return response.json.get('token')


def test_post_without_valid_user(users_cli):
    """Test post with authorization without valid user."""
    # TODO: set correct authorization header
    response = users_cli.simulate_post(
        '/back/user'
    )
    assert response.status_code == 400


def test_post_with_valid_user(users_cli):
    """Test post with authorization with valid user."""
    # TODO: set correct user schema
    user = {
        'name': 'UserA',
        'email': 'usera@email.com',
        'password': 'userpass'
    }

    response = users_cli.simulate_post(
        '/back/user',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201


def test_post_without_valid_user_email(users_cli):
    """Test post with authorization invalid user email."""
    # TODO: set correct user schema
    user = {
        'name': 'UserB',
        'email': 'userb',
        'password': 'userpass'
    }

    response = users_cli.simulate_post(
        '/back/user',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.json.get('errors').get('email') is not None
    assert response.status_code == 400


def test_get_with_existent_user_id(users_cli):
    """Test get with existent user id."""
    admin_jwt_token = login_admin(users_cli)

    user = {
        'name': 'UserC',
        'email': 'userc@email.com',
        'password': 'userpass'
    }

    response = users_cli.simulate_post(
        '/back/user',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.json.get('uid') is not None
    assert response.status_code == 201

    user_id = response.json.get('uid')

    # Admin activate and asign a role for UserC user.

    response = users_cli.simulate_put(
        f'/back/user/{user_id}',
        headers={
            'AUTHORIZATION': admin_jwt_token,
            'Content-Type': 'application/json'
        },
        body=json.dumps({'role': 'creator', 'status': 'active'})
    )

    assert response.status_code == 200

    # UserC login.
    response = users_cli.simulate_post(
        f'/back/login',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(
            {'email': user.get('email'), 'password': user.get('password')}
        )
    )

    assert response.status_code == 200

    user_jwt_token = response.json.get('token')

    # UserC get self information.
    response = users_cli.simulate_get(
        f"/back/user/{user_id}",
        headers={
            'AUTHORIZATION': user_jwt_token,
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 200


def test_get_without_existent_user_id(users_cli):
    """Test get without existent user id."""
    admin_jwt_token = login_admin(users_cli)

    response = users_cli.simulate_get(
        f"/back/user/{uuid4().hex}",
        headers={
            'AUTHORIZATION': admin_jwt_token,
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 404


def test_put_with_valid_user(users_cli):
    """Test put with valid user."""
    admin_jwt_token = login_admin(users_cli)

    user = {
        'name': 'UserD',
        'email': 'userd@email.com',
        'password': 'userpass'
    }

    response = users_cli.simulate_post(
        '/back/user',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.json.get('uid') is not None
    assert response.status_code == 201

    user_id = response.json.get('uid')

    # Admin activate and asign a role for UserD user.

    response = users_cli.simulate_put(
        f'/back/user/{user_id}',
        headers={
            'AUTHORIZATION': admin_jwt_token,
            'Content-Type': 'application/json'
        },
        body=json.dumps({'role': 'creator', 'status': 'active'})
    )

    assert response.status_code == 200

    # UserD login.
    response = users_cli.simulate_post(
        f'/back/login',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(
            {'email': user.get('email'), 'password': user.get('password')}
        )
    )

    assert response.status_code == 200

    user_jwt_token = response.json.get('token')

    user['name'] = 'UserD UserD'

    # UserD get self information.
    response = users_cli.simulate_put(
        f"/back/user/{user_id}",
        headers={
            'AUTHORIZATION': user_jwt_token,
            'Content-Type': 'application/json'
        },
        body=json.dumps(user)
    )

    assert response.status_code == 200


def test_put_without_valid_user_email(users_cli):
    """Test put without valid user email."""
    admin_jwt_token = login_admin(users_cli)

    user = {
        'name': 'UserE',
        'email': 'usere@email.com',
        'password': 'userpass'
    }

    response = users_cli.simulate_post(
        '/back/user',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.json.get('uid') is not None
    assert response.status_code == 201

    user_id = response.json.get('uid')

    # Admin activate and asign a role for UserE user.

    response = users_cli.simulate_put(
        f'/back/user/{user_id}',
        headers={
            'AUTHORIZATION': admin_jwt_token,
            'Content-Type': 'application/json'
        },
        body=json.dumps({'role': 'creator', 'status': 'active'})
    )

    assert response.status_code == 200

    # UserE login.
    response = users_cli.simulate_post(
        f'/back/login',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(
            {'email': user.get('email'), 'password': user.get('password')}
        )
    )

    assert response.status_code == 200

    user_jwt_token = response.json.get('token')

    user['email'] = 'userc'

    # UserE get self information.
    response = users_cli.simulate_put(
        f"/back/user/{user_id}",
        headers={
            'AUTHORIZATION': user_jwt_token,
            'Content-Type': 'application/json'
        },
        body=json.dumps(user)
    )

    assert response.status_code == 400


def test_put_with_invalid_user_id(users_cli):
    """Test put with invalid user id."""
    admin_jwt_token = login_admin(users_cli)

    user = {
        'name': 'UserF',
        'email': 'userf@email.com',
        'password': 'userpass'
    }

    response = users_cli.simulate_put(
        f"/back/user/{user.get('_id')}",
        headers={
            'AUTHORIZATION': admin_jwt_token,
            'Content-Type': 'application/json'
        },
        body=json.dumps(user)
    )

    assert response.status_code == 404


def test_delete_user_without_authorization(users_cli):
    """Test delete user without authorization."""
    response = users_cli.simulate_delete(
        f'/back/user/{uuid4().hex}'
    )
    assert response.status_code == 401


def test_delete_user_with_authorization(users_cli):
    """Test delete user with authorization."""
    admin_jwt_token = login_admin(users_cli)

    user = {
        'name': 'UserG',
        'email': 'userg@email.com',
        'password': 'userpass'
    }

    response = users_cli.simulate_post(
        '/back/user',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.json.get('uid') is not None
    assert response.status_code == 201

    user_id = response.json.get('uid')

    # Admin activate and asign a role for UserH user.

    response = users_cli.simulate_put(
        f'/back/user/{user_id}',
        headers={
            'AUTHORIZATION': admin_jwt_token,
            'Content-Type': 'application/json'
        },
        body=json.dumps({'role': 'creator', 'status': 'active'})
    )

    assert response.status_code == 200

    # UserH login.
    response = users_cli.simulate_post(
        f'/back/login',
        headers={'Content-Type': 'application/json'},
        body=json.dumps(
            {'email': user.get('email'), 'password': user.get('password')}
        )
    )

    assert response.status_code == 200

    user_jwt_token = response.json.get('token')

    # UserH get self information.
    response = users_cli.simulate_get(
        f"/back/user/{user_id}",
        headers={
            'AUTHORIZATION': user_jwt_token,
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 200


def test_delete_without_existent_user(users_cli):
    """Test delete without existent user."""
    admin_jwt_token = login_admin(users_cli)

    response = users_cli.simulate_delete(
        f"/back/user/{uuid4().hex}",
        headers={
            'AUTHORIZATION': admin_jwt_token,
            'Content-Type': 'application/json'
        }
    )

    assert response.status_code == 404
