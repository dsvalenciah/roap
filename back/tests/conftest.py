
"""
Contains client fixture funtion.
"""

from falcon import testing
import pytest

from app import Roap


@pytest.fixture(scope='module')
def client():
    """Create a client to test roap Resources."""
    roap = Roap(db_name='roap-test')
    db = roap.get_db()
    db.users.delete_many({})
    return testing.TestClient(roap.get_api())
