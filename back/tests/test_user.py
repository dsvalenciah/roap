from datetime import datetime
from uuid import uuid4
import json


def test_post_without_authorization(client):
    cli, db = client
    response = cli.simulate_post('/back/user')
    assert response.status_code == 401


def test_post_with_authorization_without_valid_user(client):
    # TODO: set correct authorization header
    cli, db = client
    response = cli.simulate_post(
        '/back/user', headers={'AUTHORIZATION': 'uuid'}
    )
    assert response.status_code == 400


def test_post_with_authorization_with_valid_user(client):
    # TODO: set correct user schema
    user = {
        '_id': uuid4().hex,
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    cli, db = client

    response = cli.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201


def test_post_with_authorization_with_repeated_user(client):
    # TODO: set correct user schema
    user = {
        '_id': uuid4().hex,
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    cli, db = client

    response = cli.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    response = cli.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 400


def test_post_with_authorization_invalid_user_email(client):
    # TODO: set correct user schema
    user = {
        '_id': uuid4().hex,
        'name': 'Daniel',
        'email': 'dsvalenciah',
        'role': 'administrator',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    cli, db = client

    response = cli.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.json.get('errors').get('email') != None
    assert response.status_code == 400


def test_post_with_authorization_invalid_user_created(client):
    # TODO: set correct user schema
    user = {
        '_id': uuid4().hex,
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M')
    }

    cli, db = client

    response = cli.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.json.get('errors').get('created') != None
    assert response.status_code == 400


def test_get_with_existent_user_id(client):
    user = {
        '_id': uuid4().hex,
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    cli, db = client

    response = cli.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    response = cli.simulate_get(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'}
    )

    assert response.status_code == 200


def test_get_without_existent_user_id(client):
    cli, db = client

    response = cli.simulate_get(
        f"/back/user/{uuid4().hex}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'}
    )

    assert response.status_code == 404


def test_put_with_valid_user(client):
    user = {
        '_id': uuid4().hex,
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    cli, db = client

    response = cli.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    user['name'] = 'Orlando'
    response = cli.simulate_put(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 200


def test_put_without_invalid_user_email(client):
    user = {
        '_id': uuid4().hex,
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    cli, db = client

    response = cli.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    user['email'] = 'dsvalenciah'
    response = cli.simulate_put(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 400


def test_put_with_unmodified_user(client):
    user = {
        '_id': uuid4().hex,
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    cli, db = client

    response = cli.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    response = cli.simulate_put(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 200


def test_put_with_invalid_user_id(client):
    user = {
        '_id': uuid4().hex,
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    cli, db = client

    response = cli.simulate_put(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 404


def test_delete_user_without_authorization(client):
    cli, db = client
    response = cli.simulate_post('/back/user')
    assert response.status_code == 401


def test_delete_user_with_authorization(client):
    user = {
        '_id': uuid4().hex,
        'name': 'Daniel',
        'email': 'dsvalenciah@unal.edu.co',
        'role': 'administrator',
        'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    cli, db = client

    response = cli.simulate_post(
        '/back/user',
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'},
        body=json.dumps(user)
    )

    assert response.status_code == 201

    response = cli.simulate_delete(
        f"/back/user/{user.get('_id')}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'}
    )

    assert response.status_code == 200


def test_delete_without_existent_user(client):
    cli, db = client
    response = cli.simulate_delete(
        f"/back/user/{uuid4().hex}",
        headers={'AUTHORIZATION': 'uuid', 'Content-Type': 'application/json'}
    )

    assert response.status_code == 404
