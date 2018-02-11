
"""
Contain utility functions to test user Resources.
"""

from datetime import datetime
from uuid import uuid4
import json


def test_post_without_authorization(client):
    """Test post without authorization."""
    response = client.simulate_post('/back/user')
    assert response.status_code == 401


def test_post_with_authorization_without_valid_user(client):
    """Test post with authorization without valid user."""
    # TODO: set correct authorization header
    response = client.simulate_post(
        '/back/user', headers={'AUTHORIZATION': 'uuid'}
    )
    assert response.status_code == 400


def test_post_with_authorization_with_valid_user(client):
    """Test post with authorization with valid user."""
    # TODO: set correct user schema
    user = {
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
    }

    response = client.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201


def test_post_with_authorization_with_repeated_user(client):
    """Test post with authorization with repeated user."""
    # TODO: set correct user schema
    user = {
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
    }

    response = client.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    response = client.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 400


def test_post_with_authorization_invalid_user_email(client):
    """Test post with authorization invalid user email."""
    # TODO: set correct user schema
    user = {
        'name': 'Daniel',
        'email': 'dsvalenciah',
        'role': 'administrator',
    }

    response = client.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.json.get('errors').get('email') is not None
    assert response.status_code == 400


def test_post_with_authorization_invalid_user_created(client):
    """Test post with authorization invalid user created."""
    # TODO: set correct user schema
    user = {
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
    }

    response = client.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.json.get('errors').get('created') is not None
    assert response.status_code == 400


def test_get_with_existent_user_id(client):
    """Test get with existent user id."""
    user = {
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
    }

    response = client.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    response = client.simulate_get(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'}
    )

    assert response.status_code == 200


def test_get_without_existent_user_id(client):
    """Test get without existent user id."""
    response = client.simulate_get(
        f"/back/user/{uuid4().hex}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'}
    )

    assert response.status_code == 404


def test_put_with_valid_user(client):
    """Test put with valid user."""
    user = {
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
    }

    response = client.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    user['name'] = 'Orlando'
    response = client.simulate_put(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 200


def test_put_without_invalid_user_email(client):
    """Test put without invalid user email."""
    user = {
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
    }

    response = client.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    user['email'] = 'dsvalenciah'
    response = client.simulate_put(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 400


def test_put_with_unmodified_user(client):
    """Test put with unmodified user."""
    user = {
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
    }

    response = client.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    response = client.simulate_put(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 200


def test_put_with_invalid_user_id(client):
    """Test put with invalid user id."""
    user = {
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
    }

    response = client.simulate_put(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 404


def test_delete_user_without_authorization(client):
    """Test delete user without authorization."""
    response = client.simulate_post('/back/user')
    assert response.status_code == 401


def test_delete_user_with_authorization(client):
    """Test delete user with authorization."""
    user = {
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
    }

    response = client.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    response = client.simulate_delete(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'}
    )

    assert response.status_code == 200


def test_delete_without_existent_user(client):
    """Test delete without existent user."""
    response = client.simulate_delete(
        f"/back/user/{uuid4().hex}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'}
    )

    assert response.status_code == 404
