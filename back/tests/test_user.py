from datetime import datetime
from uuid import uuid4
import json

from falcon import testing
import pytest

from app import Roap

@pytest.fixture(scope='module')
def client():
    roap = Roap(db_name="roap-test")
    return testing.TestClient(roap.get_api()), roap.get_db()

def test_post_user_create_from_unauthorized(client):
    cli, db = client
    result = cli.simulate_post('/back/user-create')
    assert result.status_code == 401

def test_post_user_create_from_authorized(client):
    # TODO: set correct authorization header
    cli, db = client
    result = cli.simulate_post(
        '/back/user-create', headers={"AUTHORIZATION": "uuid"}
    )
    assert result.status_code == 400

def test_post_user_create_from_authorized_correct_data(client):
    # TODO: set correct user schema
    user = {
        "_id": uuid4().hex,
        "name": "Daniel",
        "email": "dsvalenciah@unal.edu.co",
        "role": "administrator",
        "created": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    cli, db = client

    result = cli.simulate_post(
        '/back/user-create',
        headers={"AUTHORIZATION": "uuid", "Content-Type": "application/json"},
        body=json.dumps(user)
    )
    assert db.users.find_one({"_id": user.get("_id")}) == user
    assert result.status_code == 201

def test_post_user_create_from_authorized_incorrect_email(client):
    # TODO: set correct user schema
    user = {
        "_id": uuid4().hex,
        "name": "Daniel",
        "email": "dsvalenciah",
        "role": "administrator",
        "created": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

    cli, db = client

    result = cli.simulate_post(
        '/back/user-create',
        headers={"AUTHORIZATION": "uuid", "Content-Type": "application/json"},
        body=json.dumps(user)
    )

    assert result.json.get("errors").get("email") != None
    assert result.status_code == 400

def test_post_user_create_from_authorized_incorrect_created(client):
    # TODO: set correct user schema
    user = {
        "_id": uuid4().hex,
        "name": "Daniel",
        "email": "dsvalenciah",
        "role": "administrator",
        "created": datetime.now().strftime('%Y-%m-%d %H:%M')
    }

    cli, db = client

    result = cli.simulate_post(
        '/back/user-create',
        headers={"AUTHORIZATION": "uuid", "Content-Type": "application/json"},
        body=json.dumps(user)
    )

    assert result.json.get("errors").get("created") != None
    assert result.status_code == 400

def test_get_user(client):
    pass
    '''
    doc = {u'message': u'Hello world!'}
    result = client.simulate_request('/back/user')
    assert result.json == doc
    '''

def test_put_user(client):
    pass
    '''
    doc = {u'message': u'Hello world!'}
    result = client.simulate_request('/back/user/{field_id}')
    assert result.json == doc
    '''

def test_delete_user(client):
    pass
    '''
    doc = {u'message': u'Hello world!'}
    result = client.simulate_request('/back/user/{field_id}')
    assert result.json == doc
    '''