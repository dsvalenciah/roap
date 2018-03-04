
"""
Contain utility to test learning objects operations from creator user.
"""
from uuid import uuid4

from tests.test_learning_object.login_admin import login_admin


def login_creator_active():
    """Login ucreator user."""
    pass


def login_creator_inactive():
    """Login creatoruser."""
    pass


def test_post_with_valid_object_json(learning_objects_cli, one_dict_lom):
    """An a docstring."""
    pass


def test_post_without_valid_object_json(learning_objects_cli):
    """An a docstring."""
    pass


def test_post_with_valid_object_xml(learning_objects_cli):
    """An a docstring."""
    pass


def test_post_without_valid_object_xml(learning_objects_cli):
    """An a docstring."""
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
