
"""
Contains cli fixture funtion.
"""
import json
import os

from falcon import testing
import pytest

from app import Roap


def get_file_path(relative_path):
    """Create absulute path from a relative path."""
    root = os.path.dirname(__file__)
    return os.path.join(root, relative_path)


@pytest.fixture(scope='module')
def users_cli():
    """Create a cli to test roap users Resources."""
    roap = Roap(db_name='roap-test')
    db = roap.get_db()
    db.users.delete_many({})
    roap = Roap(db_name='roap-test')
    return testing.TestClient(roap.get_api())


@pytest.fixture(scope='module')
def learning_objects_cli():
    """Create a cli to test roap learning objects Resources."""
    roap = Roap(db_name='roap-test')
    db = roap.get_db()
    db.users.delete_many({})
    db.learning_objects.delete_many({})
    roap = Roap(db_name='roap-test')
    return testing.TestClient(roap.get_api())


@pytest.fixture(scope='module')
def one_xml_lom():
    """Create a file xml file handler with one learning object."""
    return open(get_file_path('data/one_learning_object.xml'))


@pytest.fixture(scope='module')
def many_xml_lom():
    """Create a file xml file handler with many learning objects."""
    return open(get_file_path('data/may_learning_objects.xml'))


@pytest.fixture(scope='module')
def one_json_lom():
    """Create a file json file handler with one learning object."""
    return open(get_file_path('data/one_learning_object.json'))


@pytest.fixture(scope='module')
def many_json_lom():
    """Create a file json file handler with many learning objects."""
    return open(get_file_path('data/may_learning_objects.json'))


@pytest.fixture(scope='module')
def one_dict_lom():
    """Create a dict with one learning object."""
    return json.load(
        open(get_file_path('data/one_learning_object.json'))
    )


@pytest.fixture(scope='module')
def many_dict_lom():
    """Create a list of dicts with learning objects."""
    return json.load(
        open(get_file_path('data/may_learning_objects.json'))
    )
