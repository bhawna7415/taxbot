import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from db.connection import DBConnection
@pytest.fixture
def db_connection():
    return DBConnection(connection=None)

def test_connect_db(db_connection):
    db_connection.connect_db()
    assert db_connection  # Assuming that the connection object is expected to be truthy
   